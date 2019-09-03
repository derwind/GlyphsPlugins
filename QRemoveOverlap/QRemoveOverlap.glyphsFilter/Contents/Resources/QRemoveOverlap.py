# encoding: utf-8

###########################################################################################################
#
#
#    Filter without dialog Plugin
#
#    Read the docs:
#    https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20without%20Dialog
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class QRemoveOverlap(FilterWithoutDialog):

    def settings(self):
        self.menuName = Glyphs.localize({'en': u'Q Remove Overlap'})
        self.keyboardShortcut = None # With Cmd+Shift

    def filter(self, layer, inEditView, customParameters):

        # Apply your filter code here

        layer.removeOverlap(checkSelection=True)
        for path in layer.paths:
            path.convertToQuadratic()
        layer.roundCoordinates()

    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
