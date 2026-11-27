#!/usr/bin/env python3
"""
Build the SemanticGIS book PDF from the Obsidian vault notes.

Usage:
    python3 build_book.py [manifest.yaml] [output.pdf]

Reads manifest.yaml (the book's Part > Chapter > Subsection structure and
which note file backs each node), normalises each note (strips YAML
frontmatter, converts Obsidian [[wikilinks]] to plain italic text, swaps
out a few emoji/symbols that pdfLaTeX can't typeset, shifts each file's own
heading levels so they nest correctly under the inserted Part/Chapter/
Subsection heading), concatenates everything into one master Markdown
file, then calls pandoc (via pdflatex) to typeset it as a PDF.

To add more content later: add a new part/section/subsection entry to
manifest.yaml pointing at the note file, then re-run this script. Nothing
else needs to change. If pdflatex chokes on a new emoji/symbol, add it to
SYMBOL_REPLACEMENTS below rather than editing the source note.
"""
import re
import subprocess
import sys
from pathlib import Path
import yaml

BUILD_DIR = Path(__file__).resolve().parent
VAULT_ROOT = BUILD_DIR.parent.parent  # _build/ lives inside Workflow/,
# which itself lives one level inside the consolidated vault root (40 SemanticGIS/),
# so manifest file/intro paths and embedded-asset lookups are now relative to that root.

FRONTMATTER_RE = re.compile(r'\A---\n.*?\n---\n', re.DOTALL)
HEADING_RE = re.compile(r'^(#{1,6})(\s+.*)$', re.MULTILINE)
WIKILINK_PIPE_RE = re.compile(r'(?<!!)\[\[[^\]|]+\|([^\]]+)\]\]')
WIKILINK_BARE_RE = re.compile(r'(?<!!)\[\[([^\]|]+)\]\]')
# Obsidian image embed: ![[filename]] or ![[filename|caption]]. The part
# after '|' is Obsidian's width/alt slot; we repurpose it as the figure
# caption when present, and fall back to the bare filename otherwise.
IMAGE_EMBED_RE = re.compile(r'!\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')

# pdfLaTeX (via the classic 'charter' font package) only covers standard
# Latin text + common typographic punctuation. Obsidian notes sometimes
# contain emoji that fall outside that; map the ones we hit here to plain
# text rather than letting the PDF build crash.
SYMBOL_REPLACEMENTS = {
    '✅': '',            # ✅ (heading already reads "Accept: ...")
    '❌': '',            # ❌ (heading already reads "Reject: ...")
    '🔁': '',            # 🔁 (heading already reads "Transform: ...")
    '⚠️': '[!]',        # ⚠️
    '⚠': '[!]',         # ⚠
    '\u2192': '->',      # → (right arrow)
    '\u2190': '<-',      # ← (left arrow)
    '\U0001f449': '->', # 👉
    '\U0001f539': '-',  # 🔹
}


def strip_frontmatter(text: str) -> str:
    return FRONTMATTER_RE.sub('', text, count=1)


SVG_CACHE_DIR = BUILD_DIR / "_cache" / "svg-to-png"
SVG_RASTER_DENSITY = 300  # dpi - plenty for a page-width print figure


def rasterize_svg(svg_path: Path) -> Path:
    """pdfLaTeX cannot embed SVG directly. Convert it to a PNG once (via
    ImageMagick's `convert`), cached by source mtime, so notes can keep
    using real vector SVGs as their source of truth without a manual
    export step before every build."""
    SVG_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = SVG_CACHE_DIR / (svg_path.stem + ".png")
    if not cached.exists() or svg_path.stat().st_mtime > cached.stat().st_mtime:
        print(f"  [svg] rasterizing {svg_path.name} -> {cached.relative_to(BUILD_DIR)} "
              f"({SVG_RASTER_DENSITY} dpi)")
        result = subprocess.run(
            ['convert', '-density', str(SVG_RASTER_DENSITY), '-background', 'none',
             str(svg_path), str(cached)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Could not rasterize {svg_path.name} (is ImageMagick's 'convert' "
                f"installed?). Error:\n{result.stderr}"
            )
    return cached


def resolve_asset(filename: str) -> str:
    """Obsidian resolves a bare embed filename by searching the whole
    vault; replicate that, scoped to THIS book's own folder tree (not the
    wider Obsidian vault) so the book stays self-contained and doesn't
    silently break if an unrelated reference library elsewhere gets
    reorganised. An .svg source is auto-rasterized (see rasterize_svg);
    everything else is returned as a path relative to VAULT_ROOT, which is
    what --resource-path is told to resolve against."""
    matches = [m for m in VAULT_ROOT.rglob(filename) if SVG_CACHE_DIR not in m.parents]
    if not matches:
        raise FileNotFoundError(
            f"Embedded image '{filename}' not found under {VAULT_ROOT.name}/. "
            f"Put it in _assets/figures/ (or anywhere under the book's own "
            f"folder - not elsewhere in the Obsidian vault) and re-run."
        )
    if len(matches) > 1:
        print(f"  [warn] '{filename}' matches multiple files; using the first: {matches[0]}")
    match = matches[0]
    if match.suffix.lower() == '.svg':
        png = rasterize_svg(match)
        return str(png)  # absolute path into the build cache; fine for pandoc as-is
    return str(match.relative_to(VAULT_ROOT))


def convert_image_embeds(text: str) -> str:
    def repl(m):
        filename, caption = m.group(1), m.group(2)
        path = resolve_asset(filename.strip())
        cap = caption.strip() if caption else ''
        return f'![{cap}]({path})'
    return IMAGE_EMBED_RE.sub(repl, text)


def convert_wikilinks(text: str) -> str:
    # [[path|Display text]] -> *Display text*   (note links, not images)
    text = WIKILINK_PIPE_RE.sub(lambda m: f'*{m.group(1)}*', text)
    # [[path/to/Note]] -> *Note*  (bare wikilink, no display text given)
    text = WIKILINK_BARE_RE.sub(lambda m: f'*{m.group(1).split("/")[-1]}*', text)
    return text


def sanitize_symbols(text: str) -> str:
    for old, new in SYMBOL_REPLACEMENTS.items():
        text = text.replace(old, new)
    # collapse any double space left behind by a dropped symbol
    text = re.sub(r'[ \t]{2,}', ' ', text)
    return text


ALLOWED_UNICODE = set("–—‘’“”…§°±×÷≠≤≥†‡")


def strip_unsupported_unicode(text: str, label: str) -> str:
    """pdfLaTeX + the classic 'charter' font only reliably covers ASCII,
    Latin-1 accented letters, and a short list of typographic punctuation
    (allowed above). Anything else (emoji, exotic symbols) gets dropped so
    the build never hard-crashes on an unexpected character; a note is
    printed so it's easy to notice and, if wanted, add a nicer replacement
    to SYMBOL_REPLACEMENTS instead of losing it silently forever."""
    out = []
    stripped = set()
    for ch in text:
        if ord(ch) < 0x2000 or ch in ALLOWED_UNICODE:
            out.append(ch)
        else:
            stripped.add(ch)
    if stripped:
        print(f"  [sanitize] {label}: dropped unsupported character(s): {' '.join(stripped)}")
    return "".join(out)


def min_heading_level(text: str):
    levels = [len(m.group(1)) for m in HEADING_RE.finditer(text)]
    return min(levels) if levels else None


def shift_headings(text: str, offset: int) -> str:
    if offset == 0:
        return text

    def repl(m):
        level = max(1, min(6, len(m.group(1)) + offset))
        return '#' * level + m.group(2)

    return HEADING_RE.sub(repl, text)


# Fixed depth (in pandoc heading '#' count) that every note's own
# content is floated down to, regardless of whether it's wrapped in an
# A/B/C Section heading or sits directly under a Chapter. This must be
# deeper than secnumdepth in preamble.tex reaches, so a note's own
# hand-numbered headings ("1. Deconstructing the Brief") never collide
# with LaTeX's auto-numbering of the book's Part/Chapter/Section structure.
NOTE_BODY_LEVEL = 4


IMAGE_LINE_RE = re.compile(r'^!\[.*\]\(.*\)\s*$')


def ensure_blank_around_block_elements(text: str) -> str:
    """Obsidian's own renderer doesn't require a blank line before a
    heading or around a standalone image, so notes written there often
    don't have one. Pandoc's markdown reader DOES require it:
      - a '### Heading' right after a paragraph, with no blank line
        before it, is read as more paragraph text, not a heading, and
        silently vanishes from the structure/TOC;
      - an image with no blank line on both sides is read as an inline
        image inside the surrounding paragraph rather than a standalone
        figure, so it never gets pandoc's automatic 'Figure N:' caption
        (its alt text just gets dropped).
    Insert the missing blank lines here so notes don't need to be
    rewritten by hand to get correct headings/figures."""
    lines = text.split('\n')
    n = len(lines)
    out = []
    for i, line in enumerate(lines):
        is_heading = bool(HEADING_RE.match(line))
        is_image = bool(IMAGE_LINE_RE.match(line))
        if (is_heading or is_image) and out and out[-1].strip() != '':
            out.append('')
        out.append(line)
        if is_image:
            nxt = lines[i + 1] if i + 1 < n else ''
            if nxt.strip() != '':
                out.append('')
    return '\n'.join(out)


def load_note(rel_path: str, insertion_level: int) -> str:
    path = VAULT_ROOT / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Note not found (check manifest.yaml): {path}")
    text = path.read_text(encoding='utf-8')
    text = strip_frontmatter(text)
    text = convert_image_embeds(text)
    text = convert_wikilinks(text)
    text = sanitize_symbols(text)
    text = strip_unsupported_unicode(text, rel_path)
    text = ensure_blank_around_block_elements(text)
    min_lvl = min_heading_level(text)
    if min_lvl is not None:
        offset = NOTE_BODY_LEVEL - min_lvl
        text = shift_headings(text, offset)
    return text.strip() + '\n'


def heading(level: int, title: str) -> str:
    return f'{"#" * level} {title}\n'


def build_master(manifest: dict) -> str:
    out = []
    for part in manifest['parts']:
        out.append(heading(1, part['title']))
        if part.get('intro'):
            out.append(load_note(part['intro'], insertion_level=1))
        for section in part.get('sections', []):
            out.append(heading(2, section['title']))
            if section.get('intro'):
                out.append(load_note(section['intro'], insertion_level=2))
            if section.get('file'):
                out.append(load_note(section['file'], insertion_level=2))
            for sub in section.get('subsections', []):
                out.append(heading(3, sub['title']))
                out.append(load_note(sub['file'], insertion_level=3))
    return '\n\n'.join(out)


def main():
    args = sys.argv[1:]
    manifest_path = Path(args[0]) if len(args) > 0 else BUILD_DIR / 'manifest.yaml'
    manifest = yaml.safe_load(manifest_path.read_text(encoding='utf-8'))

    master_md = build_master(manifest)
    master_path = BUILD_DIR / '_master.md'
    master_path.write_text(master_md, encoding='utf-8')

    out_name = manifest.get('output_filename', 'SemanticGIS_Book.pdf')
    output_pdf = Path(args[1]) if len(args) > 1 else (VAULT_ROOT / out_name)

    meta_args = []
    for k, v in manifest.get('metadata', {}).items():
        meta_args += ['-M', f'{k}={v}']

    cmd = [
        'pandoc', str(master_path),
        '-o', str(output_pdf),
        '--pdf-engine=pdflatex',
        '--resource-path', str(VAULT_ROOT),
        '--top-level-division=part',
        '--toc', '--toc-depth=3',
        '-N',
        '--include-in-header', str(BUILD_DIR / 'preamble.tex'),
        '--lua-filter', str(BUILD_DIR / 'color-spans.lua'),
        '-V', 'graphics=true',
        '-V', 'documentclass=book',
        '-V', 'geometry:margin=1in',
        '-V', 'fontfamily=charter',
        '-V', 'fontsize=11pt',
        '-V', 'linkcolor=blue',
    ] + meta_args

    print('Running:', ' '.join(cmd))
    subprocess.run(cmd, check=True)
    print(f'\nBuilt: {output_pdf}')


if __name__ == '__main__':
    main()
