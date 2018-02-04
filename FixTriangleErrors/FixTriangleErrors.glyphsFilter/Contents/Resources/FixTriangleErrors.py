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
from math2 import solve_intersection, dist, twenty_times_segment_area, Vector

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

        for path in layer.paths:
            for segment in path.segments:
                if segment.type != "curve":
                    continue
                if not self.has_triangle_error_in(segment.points):
                    continue
                self.fix_triangle_error(segment)

    def fix_triangle_error(self, segment):
        # area1 := twenty_times_segment_area([p0, p1, p2, p3])
        # area2 := twenty_times_segment_area([p0, p0+s*(p1-p0)+p0, p3+t*(p2-p3), p3])
        # area := abs(area2 - area1)
        # (Problem) Assuming that 's' is given, then solve 't' which minimizes the area.
        # (Solution) Expand given formula and set area = abs(a*s*t + b*t + c*s + d), then t = - (c*s+d)/(a*s+b).
        points = self.gsnodes2vectors(segment.points)
        p0, p1, p2, p3 = points
        candidates = self.calculate_s_t_candidates(points)
        for s, t in candidates:
            result = self.try_update_points(points, s, t)
            if result is not None:
                p1, p2 = result
                self.update_point(segment.points[1], p1)
                self.update_point(segment.points[2], p2)
                return

    def update_point(self, dst_pt, src_pt):
        dst_pt.x = src_pt.x
        dst_pt.y = src_pt.y

    def try_update_points(self, points, s, t):
        p0, p1, p2, p3 = points
        p1_ = Vector(p0.x+s*(p1.x-p0.x), p0.y+s*(p1.y-p0.y), True)
        p2_ = Vector(p3.x+t*(p2.x-p3.x), p3.y+t*(p2.y-p3.y), True)
        points = [p0, p1_, p2_, p3]
        if self.has_triangle_error_in(points):
            return None

        return p1_, p2_

    def calculate_s_t_candidates(self, points):
        p0, p1, p2, p3 = points
        area1 = twenty_times_segment_area(points)
        a = 3*((p1-p0)*(p2-p3))
        b = 6*(p2*p3+p0*(p2-p3))
        c = 6*(p0*p1+(p1-p0)*p3)
        d = 10*(p0*p3) - area1

        candidates = []
        ratios = [0.9, 0.8, 0.7]
        if dist(p0, p1) >= dist(p2, p3):
            for s in ratios:
                if a*s+b == 0:
                    continue
                t = - 1.*(c*s+d)/(a*s+b)
                candidates.append((s, t))
        else:
            for t in ratios:
                if a*t+c == 0:
                    continue
                s = - 1.*(b*t+d)/(a*t+c)
                candidates.append((s, t))
        return candidates

    def has_triangle_error_in(self, points):
        intersection = solve_intersection(points)
        if intersection is None:
            return False
        s, t = intersection
        return (0 < s < 1 and t > 1) or (s > 1 and 0 < t < 1)

    def gsnodes2vectors(self, nodes):
        return [Vector(node.x, node.y) for node in nodes]

    def generateCustomParameter( self ):
        return "{}; Dummy:{};".format(
            self.__class__.__name__,
            Glyphs.defaults['dummy_param']
        )

    def __file__(self):
        """Please leave this method unchanged"""
        return __file__

    def logToConsole( self, message ):
        """
        The variable 'message' will be passed to Console.app.
        Use self.logToConsole( "bla bla" ) for debugging.
        """
        myLog = "Filter {}:\n{}".format( self.title(), message )
        NSLog( myLog )
