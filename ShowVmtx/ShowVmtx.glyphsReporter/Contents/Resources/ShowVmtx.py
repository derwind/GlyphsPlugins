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

UPM = 1000
ASCENDER = 880
DESCENDER = -120

class ShowVmtx(ReporterPlugin):

    def settings(self):
        self.menuName = Glyphs.localize({'en': u'Vmtx'})

    def background(self, layer):
        # top of body for CJK fonts
        ascender = Glyphs.font.masters[0].ascender

        # NSColor.colorWithCalibratedRed_green_blue_alpha_( 0, 0, 0, 0.15 ).set()
        NSColor.redColor().colorWithAlphaComponent_(.7).set()
        vertOriginY = ascender
        if hasattr(layer, "vertOrigin"):
            vertOriginY -= layer.vertOrigin()
        vertOriginY = int(round(vertOriginY))

        vertWidth = UPM
        if hasattr(layer, "vertWidth") and layer.vertWidth() >= 0:
            vertWidth = layer.vertWidth()
        vertWidth = int(round(vertWidth))

        bottom = vertOriginY - vertWidth
        rect = NSRect(
            origin = (0, bottom),
            size=(layer.width, vertWidth)
        )
        path = NSBezierPath.bezierPathWithRect_(rect)
        path.setLineWidth_(2)
        path.stroke()

        pos = NSPoint(layer.width + 20, bottom + vertWidth + 20)
        self.drawTextAtPoint("VertOriginY={}".format(vertOriginY), pos, fontColor=NSColor.brownColor())
        pos = NSPoint(layer.width + 20, bottom + 20)
        self.drawTextAtPoint("VertAdvanceY={}".format(vertWidth), pos, fontColor=NSColor.brownColor())
