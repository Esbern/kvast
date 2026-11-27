#!/bin/sh
# QGIS 4 on macOS 27.2: workaround for the crash at start (https://github.com/qgis/QGIS/issues/67981).
# Makes a patched copy of QGIS in ~/Applications; the QGIS in /Applications is not changed.
# Usage: sh qgis-macos27-patch.sh            (uses the newest QGIS 4 in /Applications)
#        sh qgis-macos27-patch.sh /Applications/QGIS-final-4_2_3.app
set -e
SRC=${1:-$(ls -td /Applications/QGIS*.app 2>/dev/null | while read a; do
  v=$(defaults read "$a/Contents/Info.plist" CFBundleShortVersionString 2>/dev/null); case $v in 4.*) echo "$a"; break;; esac; done)}
[ -d "$SRC" ] || { echo "No QGIS 4 found in /Applications. Give its path: sh $0 /Applications/<name>.app"; exit 1; }
V=$(defaults read "$SRC/Contents/Info.plist" CFBundleShortVersionString)
DST="$HOME/Applications/QGIS-$V-patched.app"
[ -e "$DST" ] && { echo "$DST exists already. Drag it to the Trash in Finder and run again."; exit 1; }
echo "Copying QGIS $V to $DST (a few minutes) ..."
mkdir -p "$HOME/Applications"; ditto "$SRC" "$DST"

ICON="$DST/Contents/Resources/qgis/images/icons/qgis-icon-macos.png"
LIB="$DST/Contents/PlugIns/platforms/libqcocoa.dylib"
# 1. Dock icon: drop the PNG's colour chunks (sRGB, gAMA, cHRM, iCCP)
perl -e '
  local $/; open F, "<:raw", $ARGV[0] or die; $b = <F>; close F;
  $o = substr($b, 0, 8); $i = 8;
  while ($i < length $b) { $n = unpack "N", substr($b, $i, 4); $t = substr($b, $i+4, 4);
    $o .= substr($b, $i, 12+$n) unless $t =~ /^(sRGB|gAMA|cHRM|iCCP)$/; $i += 12+$n }
  open F, ">:raw", $ARGV[0] or die; print F $o; close F' "$ICON"
# 2. Cursor images inside the Cocoa plugin: rename iCCP to iCCp (ignored), fix the checksum
perl -MCompress::Zlib -e '
  local $/; open F, "<:raw", $ARGV[0] or die; $b = <F>; close F; $sig = "\x89PNG\r\n\x1a\n"; $p = 0; $c = 0;
  while (($p = index($b, $sig, $p)) >= 0) { $j = $p + 8;
    while (1) { $n = unpack "N", substr($b, $j, 4); $t = substr($b, $j+4, 4); last unless $t =~ /^[A-Za-z]{4}$/;
      if ($t eq "iCCP") { substr($b, $j+4, 4) = "iCCp"; substr($b, $j+8+$n, 4) = pack "N", crc32(substr($b, $j+4, 4+$n)); $c++ }
      $j += 12+$n; last if $t eq "IEND" }
    $p += 8 }
  open F, ">:raw", $ARGV[0] or die; print F $b; close F; print "Cursor images patched: $c\n"' "$LIB"
# 3. Remove download attributes and sign the copy for this Mac
xattr -cr "$DST"
echo "Signing (a minute or two) ..."
codesign --force --deep -s - --preserve-metadata=entitlements "$DST"
codesign --verify --deep "$DST" && echo "Done. Start QGIS from $DST"
open "$DST"
