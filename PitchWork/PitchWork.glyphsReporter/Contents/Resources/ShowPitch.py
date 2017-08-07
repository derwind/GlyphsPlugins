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

class ShowPitch(ReporterPlugin):

    def settings(self):
        self.menuName = Glyphs.localize({'en': u'Pitch'})

    #def willActivate(self):
    #    cur_layer = Glyphs.font.selectedLayers[0]
    #    g = cur_layer.parent
    #    print "willActivate: {}".format(g.name)

    #def willDeactivate(self):
    #    cur_layer = Glyphs.font.selectedLayers[0]
    #    g = cur_layer.parent
    #    print "willDeactivate: {}".format(g.name)

    def background(self, layer):
        cur_layer = Glyphs.font.selectedLayers[0]
        if len(cur_layer.guides) != 2:
            return

        lower_guide, upper_guide = sorted(cur_layer.guides, key=lambda guide: guide.position.y)

        # NSColor.colorWithCalibratedRed_green_blue_alpha_( 0, 0, 0, 0.15 ).set()
        NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 1, 0, .3).set()
        bottom = lower_guide.position.y
        rect = NSRect(
            origin = (0, bottom),
            size = (cur_layer.width, upper_guide.position.y - bottom)
        )
        path = NSBezierPath.bezierPathWithRect_(rect)
        #path.setLineWidth_(2)
        path.fill()

        for guide in [lower_guide, upper_guide]:
            pos = NSPoint(guide.position.x + 20, guide.position.y + 20)
            self.drawTextAtPoint("{}".format(guide.position.y), pos, fontColor=NSColor.brownColor())
