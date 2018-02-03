# encoding: utf-8

###########################################################################################################
#
#
#    Filter with dialog Plugin
#
#    Read the docs:
#    https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Filter%20with%20Dialog
#
#    For help on the use of Interface Builder:
#    https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates
#
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *

class FixTriangleErrors(FilterWithDialog):

    # Definitions of IBOutlets
    dialog = objc.IBOutlet()
    maximumSizeField = objc.IBOutlet()

    def settings(self):
        self.menuName = Glyphs.localize({
            'en': u'Fix Triangle Errors',
        })

        self.actionButtonLabel = Glyphs.localize({
            'en': u'Fix',
        })

        # Load dialog from .nib (without .extension)
        self.loadNib('IBdialog', __file__)

    # On dialog show
    def start(self):
        # Set default setting if not present
        Glyphs.registerDefault('dummy_param', 0)
        # Set value of text field
        self.maximumSizeField.setStringValue_(Glyphs.defaults['dummy_param'])
        # Set focus to text field
        self.maximumSizeField.becomeFirstResponder()

    # Action triggered by UI
    @objc.IBAction
    def setDummy_( self, sender ):
        # Store dummy coming in from dialog
        Glyphs.defaults['dummy_param'] = sender.floatValue()
        # Trigger redraw
        self.update()

    # Actual filter
    def filter(self, layer, inEditView, customParameters):
        if inEditView:
            # Called through UI
            pass
        else:
            # Called on font export
            pass

    def generateCustomParameter( self ):
        return "%s; Dummy:%s;" % (
            self.__class__.__name__,
            Glyphs.defaults['dummy_param']
        )

    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
