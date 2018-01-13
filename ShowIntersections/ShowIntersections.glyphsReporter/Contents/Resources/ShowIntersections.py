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


import os, sys
low_priority_path = "/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python"
sys.path.remove(low_priority_path)
sys.path.append(low_priority_path)
import numpy as np
import bezier, bezier.curve
from GlyphsApp.plugins import *
from detect_intersections import BaseDetectIntersections, DetectIntersections

class ShowIntersections(ReporterPlugin):

    def __init(self):
        # XXX: __init__ is not called?
        self.intersections = None
        self.current_glyph_name = None
        self.glyphOrder = [g.name for g in Glyphs.font.glyphs]

    def settings(self):
        self.menuName = Glyphs.localize({'en': u'Intersections'})

    def background(self, layer):
        if not hasattr(self, "intersections"):
            self.__init()
        glyph = layer.parent
        if glyph.name != self.current_glyph_name:
            self.current_glyph_name = glyph.name
            self.intersections = None
        if self.intersections is None:
            basename, ext = os.path.splitext(os.path.basename(Glyphs.font.filepath))
            if ext == ".otf" or ext == ".ttf":
                detector = DetectIntersections(Glyphs.font.filepath)
                self.intersections = detector.detect(self.get_glyph_name_in_font(glyph.name, detector))
            else:
                contours = self.layer2curves(layer)
                detector = BaseDetectIntersections()
                self.intersections = detector.detect_intersections(contours)

        r = 10
        self.draw_intersections(self.intersections, r)

    def layer2curves(self, layer, contours=None):
        if contours is None:
            contours = []
        for path in layer.paths:
            contour = []
            for segment in path.segments:
                pts = []
                if len(segment.points) == 2:
                    pt0 = self.double((segment.points[0].x, segment.points[0].y))
                    pt1 = self.double((segment.points[-1].x, segment.points[-1].y))
                    pts = [pt0, pt0, pt1, pt1]
                else:
                    pt0 = self.double((segment.points[0].x, segment.points[0].y))
                    pt1 = self.double((segment.points[1].x, segment.points[1].y))
                    pt2 = self.double((segment.points[2].x, segment.points[2].y))
                    pt3 = self.double((segment.points[3].x, segment.points[3].y))
                    pts = [pt0, pt1, pt2, pt3]
                nodes = np.asfortranarray(pts)
                curve = bezier.Curve(nodes, degree=3)
                contour.append(curve)
            contours.append(contour)

        for component in layer.components:
            contours = self.layer2curves(Glyphs.font.glyphs[component.componentName].layers[0], contours)
        return contours

    def double(self, pt):
        return (float(pt[0]), float(pt[1]))

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

    #def inactiveLayers(self, layer):
    #    self.intersections = None

    def documentWasSaved(self, notification):
        self.intersections = None

    def willActivate(self):
        Glyphs.addCallback(self.documentWasSaved, DOCUMENTWASSAVED)

    def willDeactivate(self):
        Glyphs.removeCallback(self.documentWasSaved, DOCUMENTWASSAVED)
