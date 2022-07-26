import wx
from common.base import gsKeyCodeMap
from components.windowBase import WindowBase


class AlertPage(WindowBase):
    def init(self):
        verticalSizer = wx.BoxSizer(wx.VERTICAL)

        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.msg = wx.StaticText(self.mainPanel, label=self.params["content"], id=wx.ID_ANY, size=(
            290, 80), style=wx.ALIGN_CENTRE_HORIZONTAL)
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        self.msg.SetFont(font)
        self.button = wx.Button(self.mainPanel, id=wx.ID_OK)
        verticalSizer.Add(self.msg, 0, wx.CENTER, 20)
        verticalSizer.Add(self.button, 0, wx.CENTER, 0)
        horizontalSizer.AddStretchSpacer()
        horizontalSizer.Add(verticalSizer, 0, wx.CENTER)
        horizontalSizer.AddStretchSpacer()

        self.mainPanel.SetSizer(horizontalSizer)
        self.onKey(gsKeyCodeMap['Start'], "Confirm", self.onConfirmEvent)
        self.button.Bind(wx.EVT_BUTTON, self.onConfirmEvent)
        self.msg.Wrap(self.mainWidth-30)
        self.Layout()

    def onConfirmEvent(self, event):
        self.parent.pop()
