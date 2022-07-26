import wx
from common.base import gsKeyCodeMap
from components.windowBase import WindowBase


class ConfirmPage(WindowBase):
    def init(self):
        verticalSizer = wx.BoxSizer(wx.VERTICAL)

        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.msg = wx.StaticText(self.mainPanel, id=wx.ID_ANY, label=self.params["content"], size=(
            290, 80), style=wx.ALIGN_CENTRE_HORIZONTAL)

        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.NORMAL)
        horizontalSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.msg.SetFont(font)
        self.button1 = wx.Button(self.mainPanel, id=wx.ID_OK)
        self.button2 = wx.Button(
            self.mainPanel, id=wx.ID_CANCEL)
        horizontalSizer2.Add(self.button1, 0, wx.CENTER, 0)
        horizontalSizer2.Add(self.button2, 0, wx.LEFT, 30)
        verticalSizer.Add(self.msg, 0, wx.CENTER, 20)
        verticalSizer.Add(horizontalSizer2, 0, wx.CENTER, 0)
        horizontalSizer.AddStretchSpacer()
        horizontalSizer.Add(verticalSizer, 0, wx.CENTER)
        horizontalSizer.AddStretchSpacer()

        self.mainPanel.SetSizer(horizontalSizer)
        self.onKey(gsKeyCodeMap['A'], "OK", self.onConfirmEvent)
        self.onKey(gsKeyCodeMap['B'], "Cancel", self.onCancelEvent)
        self.button1.Bind(wx.EVT_BUTTON, self.onConfirmEvent)
        self.msg.Wrap(self.mainWidth-30)
        self.Layout()

    def onConfirmEvent(self, event):
        self.parent.pop({'result': True, 'key': self.params["key"]})

    def onCancelEvent(self, event):
        self.parent.pop({'result': False, 'key': self.params["key"]})
