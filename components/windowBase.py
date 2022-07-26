import wx
from .footerPanel import FooterPanel
from common.base import keyCodeMap, navCodeMap


class WindowBase(wx.Panel):
    mainWidth = 320

    def __init__(self, parent, params, **kwargs):
        super().__init__(parent, size=(320, 240), **kwargs)
        self.parent = parent
        self.params = params or {}
        self.keyAction = {}
        self.beforeInit(parent)
        self.init()
        self.afterInit()

    def onKey(self, key, action, handler):
        '''
        key:Nav,A,B,X,Y
        action:show action in footer
        handler:callback functions
        '''
        self.keyAction[key] = {
            "action": action, "handler": handler
        }

        self.footerPanel.updateKeyAction(self.keyAction)

    def init(self):
        pass

    def beforeInit(self, parent):
        self.dirname = ''

        self.mainPanel = wx.Panel(self, name='mainPanel')
        self.footerPanel = FooterPanel(
            self, size=(320, 20), name='footerPanel')

        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(self.mainPanel, 1, wx.EXPAND)
        topSizer.Add(self.footerPanel, 0, wx.EXPAND)
        self.SetSizer(topSizer)
        self.Bind(wx.EVT_CHAR_HOOK, self._OnKey)

    def afterInit(self):
        self.Layout()

    def onSizeChange(self, width, height):
        self.mainWidth = width
        self.minHeight = height
        self.footerPanel.setWidth(width)

    def a(self):
        pass

    def _OnKey(self, event):
        keycode = event.GetKeyCode()
        ch = event.GetRawKeyCode()
        if keycode in keyCodeMap and keyCodeMap[keycode] == 'Menu':
            wx.CallAfter(self.parent.Close)
        ret = None
        if keycode in navCodeMap:
            if "Nav" in self.keyAction:
                ret = self.keyAction["Nav"]['handler'](keyCodeMap[keycode])
        elif keycode in keyCodeMap:
            keyName = keyCodeMap[keycode]
            if keyName in self.keyAction:
                ret = self.keyAction[keyName]['handler'](keyName)
        if not ret:
            event.Skip()

    def alert(self, content: str):
        self.parent.push(
            '/alert', {'content': content})

    def confirm(self, key, content):
        self.parent.push("/confirm", {'content': content, 'key': key})
