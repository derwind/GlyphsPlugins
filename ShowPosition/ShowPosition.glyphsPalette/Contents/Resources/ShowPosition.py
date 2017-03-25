# encoding: utf-8

###########################################################################################################
#
#
#    Palette Plugin
#
#    Read the docs:
#    https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/Palette
#
#
###########################################################################################################


from GlyphsApp.plugins import *

class ShowPosition (PalettePlugin):

    dialog = objc.IBOutlet()
    textField = objc.IBOutlet()

    def settings(self):
        self.name = Glyphs.localize({'en': u'Mouse Position'})

        # Load .nib dialog (without .extension)
        self.loadNib('IBdialog', __file__)

    def start(self):
        # Adding a callback for the 'GSUpdateInterface' event
        Glyphs.addCallback(self.update, UPDATEINTERFACE)
        Glyphs.addCallback(self.mouseDidMove, MOUSEMOVED)

    def __del__(self):
        Glyphs.removeCallback(self.update)
        Glyphs.removeCallback(self.mouseDidMove, MOUSEMOVED)

    def update( self, sender ):

        text = []

        # Extract font from sender
        font = sender.object()

        # We’re in the Edit View
        if font.currentTab:
            return

        # We’re in the Font view
        else:
            try:
                text.append("not available")
            except:
                pass

        # Send text to dialog to display
        self.textField.setStringValue_('\n'.join(text))

    def mouseDidMove(self, notification):
        text = []

        # reference: CurrentFont @ objectsGS.py
        doc = Glyphs.currentDocument
        font = doc.font
        # reference: https://forum.glyphsapp.com/t/how-do-i-see-help-of-activeeditviewcontroller/2399
        graphicView = font.parent.windowControllers()[0].activeEditViewController().graphicView()
        # reference: ShowCrossHair.glyphsReporter
        pos = graphicView.getActiveLocation_(Glyphs.currentEvent())
        text.append("X {}".format(round(pos.x, 2)))
        text.append("Y {}".format(round(pos.y, 2)))

        self.textField.setStringValue_('\n'.join(text))

    def __file__(self):
        """Please leave this method unchanged"""
        return __file__

    # Temporary Fix
    # Sort ID for compatibility with v919:
    _sortID = 0
    def setSortID_(self, id):
        try:
            self._sortID = id
        except Exception as e:
            self.logToConsole( "setSortID_: %s" % str(e) )
    def sortID(self):
        return self._sortID

