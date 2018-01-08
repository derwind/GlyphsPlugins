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


import sys
low_priority_path = "/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python"
sys.path.remove(low_priority_path)
sys.path.append(low_priority_path)
from GlyphsApp.plugins import *
from detect_intersections import DetectIntersections

class ShowIntersections(ReporterPlugin):

    def __init(self):
        # XXX: __init__ is not called?
        self.intersections = None
        self.glyphOrder = [g.name for g in Glyphs.font.glyphs]

    def settings(self):
        self.menuName = Glyphs.localize({'en': u'Intersections'})

    def background(self, layer):
        if not hasattr(self, "intersections"):
            self.__init()
        if self.intersections is None:
            detector = DetectIntersections(Glyphs.font.filepath)
            glyph = layer.parent
            self.intersections = detector.detect(self.get_glyph_name_in_font(glyph.name, detector))

        r = 10
        self.draw_intersections(self.intersections, r)

    def draw_intersections(self, intersections, r):
        #NSColor.redColor().colorWithAlphaComponent_(.3).set()
        NSColor.redColor().colorWithAlphaComponent_(1.).set()
        for pt in intersections:
            rect = NSMakeRect(pt[0]-r, pt[1]-r, r*2, r*2)
            path = NSBezierPath.alloc().init()
            path.appendBezierPathWithOvalInRect_(rect)
            path.setLineWidth_(5)
            path.stroke()

    def get_glyph_name_in_font(self, name, detector):
        if detector._is_cjk:
            gid = self.glyphOrder.index(name)
            return detector.gid2name(gid)
        else:
            return name

    def inactiveLayers(self, layer):
        self.intersections = None
