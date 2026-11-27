-- color-spans.lua
--
-- Two ways to mark up colored text in an Obsidian note, both plain HTML
-- Obsidian already renders natively (no plugin needed):
--
--   1. A fixed vocabulary class, matching the legend used throughout the
--      book (see relational-model-colors.css for the matching Obsidian
--      CSS snippet, so the colors also show up while editing):
--
--        <span class="entity">the Venue</span>
--        <span class="property">closing time</span>
--        <span class="value">05:00</span>
--        <span class="key-primary">venue_id</span>
--        <span class="key-foreign">neighbourhood_id</span>
--
--   2. A one-off inline color, for anything outside that vocabulary:
--
--        <span style="color:#2C5F2D">elevation</span>
--
-- Pandoc's markdown reader already turns this HTML into a native Span AST
-- node; this filter teaches the LaTeX writer what to do with it (wrap the
-- content in \textcolor{}). Every other writer (html, docx, ...) is left
-- untouched, since the class/style already means the right thing to them.
--
-- Usage: pandoc ... --lua-filter=color-spans.lua
-- Requires \usepackage{xcolor} in the LaTeX preamble.

-- Keep this in sync with relational-model-colors.css.
local CLASS_COLORS = {
  entity      = "B85042", -- terracotta: a Realisation of a Cognised Existence
  property    = "1E2761", -- navy: an attribute/column
  value       = "2C5F2D", -- forest green: a concrete value in a cell
  ["key-primary"] = "B8860B", -- amber: primary key
  ["key-foreign"] = "028090", -- teal: foreign key
}

local function wrap_latex_color(hex, inlines)
  local colorname = "obscolor" .. hex
  local pre = pandoc.RawInline("latex",
    "\\definecolor{" .. colorname .. "}{HTML}{" .. hex:upper() .. "}\\textcolor{" .. colorname .. "}{")
  local post = pandoc.RawInline("latex", "}")
  local out = {pre}
  for _, inline in ipairs(inlines) do
    table.insert(out, inline)
  end
  table.insert(out, post)
  return out
end

function Span(el)
  if FORMAT ~= "latex" then
    return nil
  end

  for _, cls in ipairs(el.classes) do
    local hex = CLASS_COLORS[cls]
    if hex then
      return wrap_latex_color(hex, el.content)
    end
  end

  local style = el.attributes["style"]
  if style then
    local hex = style:match("color%s*:%s*#?(%x%x%x%x%x%x)")
    if hex then
      return wrap_latex_color(hex, el.content)
    end
  end

  return nil
end
