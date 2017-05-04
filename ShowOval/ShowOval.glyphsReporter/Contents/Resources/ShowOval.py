# encoding: utf-8

###########################################################################################################
#
#
#    Reporter Plugin
#
#    Read the docs:
#    https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
#
#
###########################################################################################################


from GlyphsApp.plugins import *

class ShowOval(ReporterPlugin):

    inspectorDialogView = objc.IBOutlet()
    textFieldX = objc.IBOutlet()
    textFieldY = objc.IBOutlet()
    textFieldA = objc.IBOutlet()
    textFieldB = objc.IBOutlet()
    drawButton = objc.IBOutlet()
    clearButton = objc.IBOutlet()

    valid_pat = re.compile(r"^-?\d+$")
    x = 0
    y = 0
    a = 0
    b = 0
    valid = False

    def settings(self):
        self.menuName = Glyphs.localize({'en': u'Oval'})
        # stalt/GlyphsSDK/tree/master/Python%20Templates/Reporter
        self.loadNib("InspectorView", __file__)
        self.generalContextMenus = [
                {'view': self.inspectorDialogView},
        ]

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
    def drawButtonReceiver_(self, sender):
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

    @objc.IBAction
    def clearButtonReceiver_(self, sender):
        self.valid = False

    def is_number(self, value):
        return self.valid_pat.match(value)
