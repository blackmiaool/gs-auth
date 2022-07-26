import wx
from common.base import ua, gsKeyCodeMap


class FooterPanel(wx.Panel):
    keyAction = {}
    width = 0

    def __init__(self, parent, size, name):
        wx.Panel.__init__(self, parent, -1, size=size, name=name)

        self.defaultColor = wx.Colour(83, 83, 83)
        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def updateKeyAction(self, keyAction):
        self.keyAction = keyAction
        self.OnPaint()

    def setWidth(self, width=320):
        self.width = width

    def setBrushColor(self, color):
        self.dc.SetBrush(wx.Brush(color))

    def setPenColor(self, color):
        self.dc.SetPen(wx.Pen(color))

    def drawButtons(self):
        dc = self.dc
        buttons = [gsKeyCodeMap['A'], gsKeyCodeMap['B'], gsKeyCodeMap['X'],
                   gsKeyCodeMap['Y'], gsKeyCodeMap['Select'], gsKeyCodeMap['Start']]
        self.setBrushColor(self.defaultColor)
        self.dc.SetPen(wx.Pen())
        sectionWidthSum = 2

        for i in range(5, -1, -1):
            buttonText = buttons[i]
            if buttonText in self.keyAction:
                buttonFuntion = self.keyAction[buttonText]["action"]
            else:
                continue
            longButton = len(buttonText) > 1
            font = wx.Font(10,  wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            self.dc.SetFont(font)
            functionWidth = dc.GetTextExtent(buttonFuntion).GetWidth()
            font = wx.Font(10,  wx.FONTFAMILY_SWISS,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
            self.dc.SetFont(font)
            buttonTextWidth = dc.GetTextExtent(buttonText).GetWidth()
            buttonWidth = 20
            if longButton:
                buttonWidth = buttonTextWidth+8
            if ua["isGS"]:
                sectionWidth = functionWidth+buttonWidth+4
            else:
                sectionWidth = functionWidth+buttonWidth+4
            sectionWidthSum += sectionWidth
            startPoint = (self.width-sectionWidthSum, 2)
            if longButton:
                dc.DrawRoundedRectangle(
                    startPoint[0], startPoint[1], buttonWidth, 16, 8)
            else:
                dc.DrawCircle(startPoint[0]+8, startPoint[1]+8, 8)

            dc.SetTextForeground((255, 255, 255))
            buttonTextBias = [3, 0]
            if ua["isGS"]:
                buttonTextBias = [3, 0]
            else:
                buttonTextBias = [4, 3]
            if buttonText == 'I':
                buttonTextBias[0] += 2
            self.dc.DrawText(
                buttonText, startPoint[0]+buttonTextBias[0], startPoint[1]+buttonTextBias[1])
            font = wx.Font(10,  wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            self.dc.SetFont(font)
            dc.SetTextForeground(self.defaultColor)
            textBias = 17
            if longButton:
                textBias = buttonWidth+1
            if ua["isGS"]:

                self.dc.DrawText(
                    buttonFuntion, startPoint[0]+textBias, startPoint[1])
            else:
                self.dc.DrawText(
                    buttonFuntion, startPoint[0]+textBias, startPoint[1]+1)

    def drawNav(self):
        dc = self.dc
        self.setBrushColor(self.defaultColor)
        self.dc.SetPen(wx.Pen())
        width = 6
        height = 5
        startPoint = (3, 2)
        # vertical
        self.dc.DrawRectangle(startPoint[0]+height,
                              startPoint[1], width, width+2*height)
        # horizontal
        self.dc.DrawRectangle(startPoint[0], startPoint[1] +
                              height, width+2*height, width)
        self.setBrushColor('white')

        topTStart = (startPoint[0]+height+1, startPoint[1]+1)
        self.dc.DrawPolygon(
            [(topTStart[0], topTStart[1]+4), (topTStart[0]+2, topTStart[1]), (topTStart[0]+4, topTStart[1]+4)])
        leftTStart = (startPoint[0]+1, startPoint[1]+width)
        self.dc.DrawPolygon(
            [(leftTStart[0], leftTStart[1]+2), (leftTStart[0]+4, leftTStart[1]), (leftTStart[0]+4, leftTStart[1]+4)])
        bottomTStart = (startPoint[0]+height+1, startPoint[1]+width+height)
        self.dc.DrawPolygon(
            [(bottomTStart[0], bottomTStart[1]), (bottomTStart[0]+2, bottomTStart[1]+4), (bottomTStart[0]+4, bottomTStart[1])])
        leftTStart = (startPoint[0]+width+height, startPoint[1]+width)
        self.dc.DrawPolygon(
            [(leftTStart[0], leftTStart[1]), (leftTStart[0]+4, leftTStart[1]+2), (leftTStart[0], leftTStart[1]+4)])

        font = wx.Font(11,  wx.FONTFAMILY_DEFAULT,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.dc.SetFont(font)
        self.setPenColor(self.defaultColor)
        self.dc.DrawText(self.keyAction['Nav']["action"], 25, 2)

    def OnPaint(self, e=None):
        if not self.width:
            return
        dc = wx.PaintDC(self)
        self.dc = dc
        brush = wx.Brush("white")
        dc.SetBackground(brush)
        # dc.Clear()
        self.setPenColor(self.defaultColor)
        dc.DrawLine((0, 0), (self.width, 0))
        if 'Nav' in self.keyAction:
            self.drawNav()
        self.drawButtons()
