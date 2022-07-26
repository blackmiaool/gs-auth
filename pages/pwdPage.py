
from common.auth import get_totp_token
import wx
import json

from components.windowBase import WindowBase
from common.crypto import decrypt
from pathlib import Path
from common.base import keyCodeMap, funcKey, gsKeyCodeMap, dataFileName
from cryptography.fernet import InvalidToken
from common.globalVars import globalVars

label4state = {
    "first-input": "Input a password for your code",
    "input": "Input the password",
    "repeat": "Repeat your password"
}


class PwdPage(WindowBase):
    firstInput = False
    state = 'raw'

    def setState(self, state):
        self.state = state
        labelText = label4state[state]
        self.tips.SetLabelText(labelText)

    def getJSON(self):
        jsonFileRaw = open(dataFileName, "r")
        jsonData = json.loads(jsonFileRaw.read())
        jsonFileRaw.close()
        return jsonData

    def init(self):
        self.keyList = []
        self.keyListInit = []
        path = Path(dataFileName)
        if not path.is_file():
            self.firstInput = True
            path.touch()
            path.write_text("[]")

        jsonData = self.getJSON()

        if not len(jsonData):
            self.firstInput = True

        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.input = wx.StaticText(
            self.mainPanel, -1, '', size=(200, -1))
        self.input.SetBackgroundColour('white')
        self.count = wx.StaticText(self.mainPanel, id=wx.ID_ANY, label="0")
        self.tips = wx.StaticText(self.mainPanel, id=wx.ID_ANY,
                                  label="")
        if self.firstInput:
            self.setState('first-input')
        else:
            self.setState('input')

        horizontalSizer.Add(self.input, 0, wx.CENTER)
        horizontalSizer.Add(self.count, 0, wx.CENTER | wx.LEFT, 5)
        verticalSizer.AddStretchSpacer()
        verticalSizer.Add(self.tips, 0, wx.CENTER | wx.BOTTOM, 5)
        verticalSizer.Add(horizontalSizer, 0, wx.CENTER)
        verticalSizer.AddStretchSpacer()
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKey)
        self.mainPanel.SetSizer(verticalSizer)
        self.onKey(gsKeyCodeMap['Start'], "Confirm", self.onConfirm)
        self.onKey(gsKeyCodeMap['Select'], "Clear", self.onClear)

    def onClear(self, keyName=""):
        self.keyList = []
        self.onUpdate()

    def verifyPassword(self):
        jsonData = self.getJSON()
        try:
            self.decodeAuthList(jsonData)
            return True
        except InvalidToken:
            return False

    def decodeAuthList(self, authList):
        def decode(li):
            return {
                "title": decrypt(self.key, li["title"]),
                "secret": decrypt(self.key, li["secret"])
            }
        result = map(decode, authList)
        return list(result)

    def onConfirm(self, keyName):
        if self.state == 'first-input':
            self.setState('repeat')
            self.keyListInit = self.keyList.copy()
        elif self.state == 'repeat':
            if self.keyList == self.keyListInit:

                globalVars['pwd'] = self.keyList.copy()
                self.parent.push('/auth', {'pwd': self.keyList.copy()})
            else:
                self.setState('first-input')
                self.parent.push(
                    '/alert', {'content': "Password doesn't match"})
        elif self.state == 'input':
            self.key = '-'.join(self.keyList)
            if self.verifyPassword():
                globalVars['pwd'] = self.keyList.copy()
                self.parent.push('/auth')
            else:
                self.parent.push(
                    '/alert', {'content': "Wrong password"})
        self.onClear()

    def onUpdate(self):
        self.input.SetLabelText('·' * len(self.keyList))
        self.count.SetLabelText(str(len(self.keyList)))
        self.Layout()

    def OnKey(self, event):
        keyCode = event.GetKeyCode()
        if keyCode in keyCodeMap:
            keyName = keyCodeMap[keyCode]
            if keyName in funcKey:
                event.Skip()
                return
        self.keyList.append(str(keyCode % 256))
        self.onUpdate()
