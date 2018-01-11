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
from GlyphsApp.plugins import *

class ShowEvents(ReporterPlugin):

    def settings(self):
        self.menuName = Glyphs.localize({'en': u'Events'})

    def inactiveLayers(self, layer):
        print "inactiveLayers"

    def drawInactive(self, notification, dummy):
        print "DRAWINACTIVE"

    def tabDidOpen(self, notification):
        print "TABDIDOPEN"

    def tabWillClose(self, notification):
        print "TABWILLCLOSE"

    def mouseMoved(self, notification):
        print "MOUSEMOVED"

    def documentWasSaved(self, notification):
        print "DOCUMENTWASSAVED"

    def willActivate(self):
        Glyphs.addCallback(self.drawInactive, DRAWINACTIVE)
        Glyphs.addCallback(self.tabDidOpen, TABDIDOPEN)
        Glyphs.addCallback(self.tabWillClose, TABWILLCLOSE)
        #Glyphs.addCallback(self.mouseMoved, MOUSEMOVED)
        Glyphs.addCallback(self.documentWasSaved, DOCUMENTWASSAVED)

    def willDeactivate(self):
        Glyphs.removeCallback(self.drawInactive, DRAWINACTIVE)
        Glyphs.removeCallback(self.tabDidOpen, TABDIDOPEN)
        Glyphs.removeCallback(self.tabWillClose, TABWILLCLOSE)
        #Glyphs.removeCallback(self.mouseMoved, MOUSEMOVED)
        Glyphs.removeCallback(self.documentWasSaved, DOCUMENTWASSAVED)
