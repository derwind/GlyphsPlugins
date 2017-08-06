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
        # NSColor.colorWithCalibratedRed_green_blue_alpha_( 0, 0, 0, 0.15 ).set()
        NSColor.redColor().colorWithAlphaComponent_(.7).set()
        vertWidth = UPM
        if hasattr(layer, "vertWidth") and layer.vertWidth() >= 0:
            vertWidth = layer.vertWidth()
        bottom = layer.bounds.origin.y - layer.BSB
        rect = NSRect(
            origin = (0, bottom),
            size=(layer.width, vertWidth)
        )
        path = NSBezierPath.bezierPathWithRect_(rect)
        path.setLineWidth_(2)
        path.stroke()
