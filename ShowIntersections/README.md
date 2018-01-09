# ShowIntersections.glyphsReporter

This is a plugin for the [Glyphs font editor](https://glyphsapp.com/) by Georg Seifert.
It displays intersections by red circles in the glyph view.

![](./Intersections.png)

### Installation

1. Install [bezier](https://pypi.python.org/pypi/bezier) library (and depending libraries: `numpy`, `enum` and `six.py`) under ~/Library/Application Support/Glyphs/Scripts. (It may be easy way to pip `bezier` in your virtualenv and copy `bezier`, `numpy`, `enum`, `six.py` to ~/Library/Application Support/Glyphs/Scripts.)
2. Download the complete ZIP file and unpack it, or clone the repository.
3. Double click the .glyphsReporter file. Confirm the dialog that appears in Glyphs.
4. Restart Glyphs

### Requirements

The plugin requires app version 2.4.4 (1075) or later, running on OS X 10.12.6 or later. (Merely I confirmed the plugin only under these conditions...)

### License

Copyright 2018 derwind

Made possible with the GlyphsSDK by Georg Seifert (@schriftgestalt) and Rainer Erich Scheichelbauer (@mekkablue).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
