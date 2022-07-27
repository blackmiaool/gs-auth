
from common.auth import get_totp_token
import wx
import json
import math
import time
from components.windowBase import WindowBase
from common.base import gsKeyCodeMap, dataFileName
from common.crypto import encrypt, decrypt
from common.globalVars import globalVars


class AuthPage(WindowBase):
    prevRefreshIndex = 0
    key = ''

    def init(self):
        self.addParams = {}
        if 'addTitle' in globalVars:
            self.parent.push(
                '/input', {'title': 'Input secret', 'key': 'addSecret'})
            return
        if 'pwd' in globalVars:
            self.key = '-'.join(globalVars['pwd'])
        else:
            self.key = ''
        self.buttons = []
        self.gauges = []

        self.selectedItem = 0

        self.onKey(gsKeyCodeMap['B'], "Push", self.pushItem)
        self.onKey(gsKeyCodeMap['A'], "Add", self.add)
        self.onKey(gsKeyCodeMap['X'], "Pull", self.pullItem)
        self.onKey(gsKeyCodeMap['Y'], "Del", self.confirmDeleteItem)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer, self.timer)
        self.timer.Start(200)
        self.updateAuthList()
        self.renderList()

        self.onKey('Nav', "Select", self.onSelect)

    def confirmDeleteItem(self, event):
        self.confirm("delete", 'Delete secret ' +
                     self.decodedAuthList[self.selectedItem]['title'])

    def deleteItem(self):
        if len(self.decodedAuthList) == 0:
            return
        item = self.authList.pop(self.selectedItem)
        self.writeAuthList()
        self.updateAuthList()
        self.renderList()

    def updateAuthList(self):
        self.authList = self.readAuthList()
        if "force" in self.params:
            self.decodedAuthList = []
        else:
            try:
                self.decodedAuthList = self.decodeAuthList(self.authList)
            except:
                self.alert('Wrong password')
                self.decodedAuthList = []
                return

    def writeAuthList(self):
        jsonfile = open(dataFileName, "w")
        jsonfile.write(json.dumps(self.authList))
        jsonfile.close()

    def readAuthList(self):
        jsonfile = open(dataFileName, "r")
        data = jsonfile.read()
        jsonfile.close()
        return json.loads(data)

    def renderList(self):
        children = self.mainPanel.GetChildren()

        for i, child in enumerate(children):
            if hasattr(self, 'sizer') and self.sizer:
                if not i % 2:
                    self.sizer.Detach(self.boxSizers[round(i/2)])
            self.mainPanel.RemoveChild(child)
            child.Hide()
            wx.CallAfter(child.Destroy)
        self.sizer = wx.GridSizer(3, 10, 10)
        self.mainPanel.SetSizer(self.sizer, True)
        self.buttons = []
        self.gauges = []
        self.boxSizers = []
        for i in range(0, len(self.authList)):
            button = wx.Button(self.mainPanel, -1,
                               '', size=(100, 40))
            if self.selectedItem == i:
                button.SetForegroundColour('blue')
            else:
                button.SetForegroundColour('black')
            self.buttons.append(button)
            boxSizer = wx.BoxSizer(wx.VERTICAL)
            gauge = wx.Gauge(self.mainPanel, range=100, size=(95, 5))
            self.gauges.append(gauge)
            boxSizer.Add(button, flag=wx.ALIGN_CENTER)
            boxSizer.Add(gauge, flag=wx.ALIGN_CENTER)
            self.boxSizers.append(boxSizer)
            self.sizer.Add(boxSizer, 0, wx.EXPAND)
        self.OnTimer(True)
        self.Layout()
        self.mainPanel.SetFocus()

    def onSelect(self, event):
        cnt = len(self.decodedAuthList)
        if event == 'Left':
            self.selectedItem -= 1
        elif event == 'Right':
            self.selectedItem += 1
        elif event == 'Up':
            if self.selectedItem >= 3:
                self.selectedItem -= 3
        elif event == 'Down':
            if self.selectedItem <= cnt-4:
                self.selectedItem += 3
        if self.selectedItem < 0:
            self.selectedItem = 0
        elif self.selectedItem > cnt-1:
            self.selectedItem = cnt-1
        for i, button in enumerate(self.buttons):
            if i == self.selectedItem:
                button.SetForegroundColour('blue')
            else:
                button.SetForegroundColour('black')
        return True

    def pushItem(self, event):
        if self.selectedItem == len(self.authList)-1:
            return
        item = self.authList.pop(self.selectedItem)
        self.authList.insert(self.selectedItem+1, item)
        self.writeAuthList()
        self.updateAuthList()
        self.renderList()

    def pullItem(self, event):
        if self.selectedItem == 0:
            return
        item = self.authList.pop(self.selectedItem)
        self.authList.insert(self.selectedItem-1, item)
        self.writeAuthList()
        self.updateAuthList()
        self.renderList()

    def showItem(self, keyName):
        pass

    def OnTimer(self, event=None):
        ns = time.time_ns()
        index = ns // 1000000 // 30000
        process = math.floor(ns // 1000000 % 30000/30000*100)
        for i in range(0, len(self.gauges)):
            self.gauges[i].SetValue(process)

        force = True
        if hasattr(event, 'Timer'):
            force = False
        if self.prevRefreshIndex != index or force:
            self.prevRefreshIndex = index
            for i in range(0, len(self.decodedAuthList)):
                button = self.buttons[i]
                button.SetBackgroundColour('white')
                button.SetLabelText(
                    self.decodedAuthList[i]["title"]+"\n"+str(get_totp_token(self.decodedAuthList[i]["secret"])))
    encryptCache = {}
    decryptCache = {}

    def decrypt(self, content):
        if content in self.decryptCache:
            return self.decryptCache[content]
        ret = decrypt(self.key, content)
        self.decryptCache[content] = ret
        return ret

    def encrypt(self, content):
        if content in self.encryptCache:
            return self.encryptCache[content]
        ret = encrypt(self.key, content)
        self.encryptCache[content] = ret
        return ret

    def decodeAuthList(self, authList):
        def decode(li):
            return {
                "title": self.decrypt(li["title"]),
                "secret": self.decrypt(li["secret"])
            }
        return list(map(decode, authList))

    def onPop(self, path, params):
        if path == '/input':
            self.addParams[params['key']] = params['value']
            if params['key'] == 'addTitle':
                self.parent.push(
                    "/input", {'title': 'Input the account secret', 'key': 'addSecret'})
            elif params['key'] == 'addSecret':
                try:
                    num = get_totp_token(params['value'])
                except:
                    self.parent.push('/alert',{'content':'Invalid secret'})
                    return

                encrypedTitle = encrypt(self.key, self.addParams['addTitle'])
                encrypedSecret = encrypt(
                    self.key, self.addParams['addSecret'])
                self.authList.append(
                    {"title": encrypedTitle, 'secret': encrypedSecret})
                self.writeAuthList()
                self.parent.push('/auth', None, replace=True)

        elif path == '/confirm':
            if params['key'] == 'delete':
                self.deleteItem()

    def add(self, event):
        self.parent.push(
            "/input", {'title': 'Input the account name', 'key': 'addTitle'})
