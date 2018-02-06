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

class Mode(object):
    FAST, MEDIUM, SLOW = range(3)

fix_mode = Mode.SLOW

def createRemoveOverlapFilter():
    font = Glyphs.font
    thisFilter = NSClassFromString("GlyphsFilterRemoveOverlap").alloc().init()
    thisFilter.setController_(font.currentTab)
    return thisFilter

def create_path(points):
    new_path = GSPath()
    for pt in points:
        pt2 = GSNode(type=pt.type, x=pt.x, y=pt.y)
        new_path.points.append(pt2)
    new_path.setClosePath_(True)
    return new_path

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
            fixable_intersections_pathtimes = set()
            for segment in path.segments:
                if segment.type != "curve":
                    continue
                s_t = self.triangle_error_of(segment.points)
                if s_t is None:
                    if fix_mode > Mode.MEDIUM:
                        if self.triangle_error_of(segment.points, proper=True) is not None:
                            if self.can_fix_intersection(segment):
                                # record segments' end point's index
                                fixable_intersections_pathtimes.add(path.points.index(segment.points[-1]))
                    continue
                self.fix_triangle_error(segment, s_t)
            for pathtime in sorted(fixable_intersections_pathtimes, reverse=True):
                path.insertNodeWithPathTime_(pathtime + .5)

    def fix_triangle_error(self, segment, s_t):
        #removeOverlapFilter = createRemoveOverlapFilter()

        # area1 := twenty_times_segment_area([p0, p1, p2, p3])
        # area2 := twenty_times_segment_area([p0, p0+s*(p1-p0)+p0, p3+t*(p2-p3), p3])
        # area := abs(area2 - area1)
        # (Problem) Assuming that 's' is given, then solve 't' which minimizes the area.
        # (Solution) Expand given formula and set area = abs(a*s*t + b*t + c*s + d), then t = - (c*s+d)/(a*s+b).
        points = self.gsnodes2vectors(segment.points)
        p0, p1, p2, p3 = points
        candidates = self.calculate_s_t_candidates(points, s_t)
        area2points = {}
        for s, t in candidates:
            result = self.try_update_points(points, s, t)
            if result is not None:
                p1, p2 = result
                if fix_mode == Mode.FAST:
                    self.update_point(segment.points[1], p1)
                    self.update_point(segment.points[2], p2)
                    return
                area = self.calculate_area_of_original_and_perturbed_segments(segment.points, p1, p2)
                area2points[area] = (p1, p2)
        if area2points:
            # pick points according to the minimal area
            p1, p2 = sorted(area2points.items())[0][1]
            self.update_point(segment.points[1], p1)
            self.update_point(segment.points[2], p2)

    def can_fix_intersection(self, segment):
        u"""
        check that the intersection can be fixed by the segment is splitted at the half point
        """

        points = [segment.points[1], segment.points[2], segment.points[3], segment.points[2], segment.points[1], segment.points[0]]
        path = create_path(points)
        layer = GSLayer()
        layer.paths.append(path)
        if layer.paths[0].insertNodeWithPathTime_(2.5) is None:
            return False
        for segment in layer.paths[0].segments[:-1]:
            if len(segment.points) == 4 and self.triangle_error_of(segment.points, easy_only=False, do_round=True) is not None:
                return False
        return True

    def update_point(self, dst_pt, src_pt):
        dst_pt.x = src_pt.x
        dst_pt.y = src_pt.y

    def calculate_area_of_original_and_perturbed_segments(self, points, p1, p2):
        u"""
        :param list_of_GSNode points: original points belonging to original segment
        :param Vector p1: perturbed point of points[1]
        :param Vector p2: perturbed point of points[2]
        """

        p1_ = GSNode(type=points[1].type, x=p1.x, y=p2.y)
        p2_ = GSNode(type=points[2].type, x=p1.x, y=p2.y)
        points = [points[1], points[2], points[3], p2_, p1_, points[0]]
        path = create_path(points)
        layer = GSLayer()
        layer.paths.append(path)
        #removeOverlapFilter.runFilterWithLayer_error_(layer, None)
        layer.removeOverlap()
        total_area = 0
        for path in layer.paths:
            area = 0
            for segment in path.segments:
                area += twenty_times_segment_area(segment.points)
            total_area += abs(area)
        return total_area

    def try_update_points(self, points, s, t):
        p0, p1, p2, p3 = points
        p1_ = Vector(p0.x+s*(p1.x-p0.x), p0.y+s*(p1.y-p0.y), True)
        p2_ = Vector(p3.x+t*(p2.x-p3.x), p3.y+t*(p2.y-p3.y), True)
        perturbed_points = [p0, p1_, p2_, p3]
        if self.triangle_error_of(perturbed_points, easy_only=False) is not None:
            return None

        return p1_, p2_

    def calculate_s_t_candidates(self, points, s_t):
        p0, p1, p2, p3 = points
        area1 = twenty_times_segment_area(points)
        a = 3*((p1-p0)*(p2-p3))
        b = 6*(p2*p3+p0*(p2-p3))
        c = 6*(p0*p1+(p1-p0)*p3)
        d = 10*(p0*p3) - area1

        candidates = []
        ratios = [1.5, 1.4, 1.3, 1.2, 1.1, .9, .8, .7, .6, .5,]
        # the intersetion is on the handle of p0 and p1
        if 0 <= s_t[0] <= 1:
            # shorten the handle of p0 and p1
            for s in ratios:
                if a*s+b == 0:
                    continue
                t = - 1.*(c*s+d)/(a*s+b)
                if t > 0:
                    candidates.append((s, t))
        else:
            for t in ratios:
                if a*t+c == 0:
                    continue
                s = - 1.*(b*t+d)/(a*t+c)
                if s > 0:
                    candidates.append((s, t))
        return candidates

    def triangle_error_of(self, points, easy_only=True, proper=False, do_round=False):
        u"""
        detect triangle errors

        :param list points: points belonging to a curve
        :param boolean easy_only: detect only relatively easy case
        :param boolean proper: detect proper intersections
        :return: two bezier parameters
        :rtype: tuple of int
        """

        if do_round:
            points = [GSNode(type=pt.type, x=int(round(pt.x)), y=int(round(pt.y))) for pt in points]

        intersection = solve_intersection(points)
        if intersection is None:
            return None
        s, t = intersection
        if proper:
            # proper intersection case
            if 0 < s < 1 and 0 < t < 1:
                return s,t
        else:
            if easy_only:
                # relatively easy case
                if (0 <= s <= 1 and t >= 1) or (s >= 1 and 0 <= t <= 1):
                    return s, t
            else:
                # all cases
                if 0 <= s <= 1 or 0 <= t <= 1:
                    return s,t
        return None

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
