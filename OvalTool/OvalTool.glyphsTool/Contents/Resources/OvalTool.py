# encoding: utf-8

###########################################################################################################
#
#
#    Select Tool Plugin
#
#    Read the docs:
#    https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/SelectTool
#
#
###########################################################################################################


import re
from GlyphsApp.plugins import *

class OvalTool(SelectTool):

    inspectorDialogView = objc.IBOutlet()
    textFieldX = objc.IBOutlet()
    textFieldY = objc.IBOutlet()
    textFieldA = objc.IBOutlet()
    textFieldB = objc.IBOutlet()
    drawButton = objc.IBOutlet()

    valid_pat = re.compile(r"^-?\d+$")
    x = 0
    y = 0
    a = 0
    b = 0
    valid = False

    def settings(self):
        self.name = Glyphs.localize({'en': u'OvalTool'})
        #self.generalContextMenus = [
        #    {'name': Glyphs.localize({'en': u'Oval'}), 'action': self.printInfo},
        #]
        self.keyboardShortcut = 'o'

        self.toolbarPosition = 300

        source_image = os.path.join(os.path.dirname(__file__), 'toolbar.pdf')
        self.image = NSImage.alloc().initByReferencingFile_(source_image)
        self.image.setTemplate_(True)

        # Load .nib file from package (without .extension)
        self.loadNib("InspectorView", __file__)

    def inspectorViewControllers(self):
        # override default inspectorViewControllers and show only my customized controller
        # also see SelectTool.inspectorViewControllers @ GlyphsSDK/ObjectWrapper/GlyphsApp/plugins.py
        return [self]

    def background(self, layer):

        if not self.valid:
            return
        NSColor.redColor().colorWithAlphaComponent_(.3).set()
        rect = NSMakeRect(self.x-self.a, self.y-self.b, self.a*2, self.b*2)
        path = NSBezierPath.alloc().init()
        path.appendBezierPathWithOvalInRect_(rect)
        path.setLineWidth_(2)
        path.stroke()

    @objc.IBAction
    def drawButtonReceiver_( self, sender ):
        if self.is_number(self.textFieldX.stringValue()) and self.is_number(self.textFieldY.stringValue()) and self.is_number(self.textFieldA.stringValue()) and self.is_number(self.textFieldB.stringValue()):
            x = int(self.textFieldX.stringValue())
            y = int(self.textFieldY.stringValue())
            a = int(self.textFieldA.stringValue())
            b = int(self.textFieldB.stringValue())
            if a != 0 and b != 0:
                self.x = x
                self.y = y
                self.a = a
                self.b = b
                self.valid = True
                return
        self.valid = False

    def is_number(self, value):
        return self.valid_pat.match(value)

    def __file__(self):
        """Please leave this method unchanged"""
        return __file__

    def toolBarIcon(self):
        return self.image
