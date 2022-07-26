import wx
import math
from common.base import gsKeyCodeMap
from components.windowBase import WindowBase
keyboardLayout1 = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                   ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
                   ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
                   ['z', 'x', 'c', 'v', 'b', 'n', 'm'], ]
keyboardLayout2 = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                   ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
                   ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
                   ['Z', 'X', 'C', 'V', 'B', 'N', 'M'], ]
keyboardLayout3 = [['!', '@', '#', '$', '%', '^', '&&', '*', '(', ')'],
                   ['-', '_', '+', '=', '~', '`', '[', ']', '{', '}'],
                   ['|', '\\', ':', ';', '"', '\'', '<', '>', ',', '.'],
                   ['?', '/', 'Space'], ]

keyboardLayouts = [keyboardLayout1, keyboardLayout2, keyboardLayout3]


class Keyboard(wx.Panel):
    def __init__(self, parent: wx.Window, layout):
        super().__init__(parent, size=(320, 240))
        self.buttons = []
        self.selectedKey = [0, 0]
        self.layout = layout
        self.renderKeyboard()

    def getKey(self):
        ret = self.layout[self.selectedKey[1]][self.selectedKey[0]]
        if ret == 'Space':
            return ' '
        else:
            return ret

    def navKey(self, direction=None):
        if direction == 'Right':
            if self.selectedKey[0] == len(self.layout[self.selectedKey[1]])-1:
                self.selectedKey[0] = 0
            else:
                self.selectedKey[0] += 1
        elif direction == 'Left':
            if self.selectedKey[0] == 0:
                self.selectedKey[0] = len(
                    self.layout[self.selectedKey[1]])-1
            else:
                self.selectedKey[0] -= 1
        elif direction == 'Up':
            if self.selectedKey[1] == 0:
                yNext = len(self.layout)-1
            else:
                yNext = self.selectedKey[1]-1
            x = math.floor(
                self.selectedKey[0]/len(self.layout[self.selectedKey[1]])*len(self.layout[yNext]))
            self.selectedKey[0] = x
            self.selectedKey[1] = yNext
        elif direction == 'Down':
            if self.selectedKey[1] == len(self.layout)-1:
                yNext = 0
            else:
                yNext = self.selectedKey[1]+1
            x = math.floor(
                self.selectedKey[0]/len(self.layout[self.selectedKey[1]])*len(self.layout[yNext]))
            self.selectedKey[0] = x
            self.selectedKey[1] = yNext

        self.selectKey(self.selectedKey[0], self.selectedKey[1])

    def selectKey(self, x: int, y: int):
        def resetKey(button):
            button.SetForegroundColour('black')
            button.SetBackgroundColour(None)
        self.eachKey(resetKey)
        selectedButton = self.buttons[y][x]
        selectedButton.SetForegroundColour('white')
        selectedButton.SetBackgroundColour(wx.Colour(0, 102, 255))

    def eachKey(self, func):
        for layerIndex in range(0, len(self.layout)):
            for keyIndex in range(0, len(self.layout[layerIndex]), 1):
                func(self.buttons[layerIndex][keyIndex])

    def renderKeyboard(self):

        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        for layerIndex in range(0, len(self.layout)):
            horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
            layer = self.layout[layerIndex]
            self.buttons.append([])
            font = wx.Font(15,  wx.FONTFAMILY_DEFAULT,
                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
            for keyIndex in range(0, len(layer), 1):
                labelText = layer[keyIndex]
                button = wx.StaticText(
                    self, id=wx.ID_ANY, label=labelText, size=(len(labelText)*8+19, 25), style=wx.ALIGN_CENTRE_HORIZONTAL)

                button.SetFont(
                    font)
                horizontalSizer.Add(button, 0, wx.CENTER)
                self.buttons[layerIndex].append(button)
            verticalSizer.Add(horizontalSizer, 1, wx.CENTER)
        self.SetSizer(verticalSizer)
        wx.StaticText(self, id=wx.ID_ANY, label='⇦',
                      size=(25, 25), pos=(0, 40))
        wx.StaticText(self, id=wx.ID_ANY, label='⇨',
                      size=(25, 25), pos=(285, 40))


class InputPage(WindowBase):
    value = ''

    def init(self):
        self.verticalSizer = wx.BoxSizer(wx.VERTICAL)
        title = ''
        if 'title' in self.params:
            title = self.params['title']
        self.title = wx.StaticText(self.mainPanel, -1, title)

        self.text = wx.StaticText(self.mainPanel, -1, size=(300, 30))
        self.text.SetBackgroundColour('white')
        self.verticalSizer.Add(self.title, 0, wx.EXPAND |
                               wx.TOP | wx.LEFT | wx.RIGHT, 10)
        self.verticalSizer.Add(self.text, 0, wx.EXPAND | wx.ALL, 10)

        self.mainPanel.SetSizer(self.verticalSizer)
        self.onKey(gsKeyCodeMap['Start'], "Done", self.onDone)
        self.onKey('Nav', "Select", self.onSelect)
        self.onKey(gsKeyCodeMap['B'], "Backspace", self.backspace)
        self.onKey(gsKeyCodeMap['A'], "Enter", self.enter)
        self.selectKeyboard(keyboardLayouts[self.layoutIndex])
        self.keyboard.navKey()

    def backspace(self, event):
        self.value = self.value[:-1]
        self.text.SetLabelText(self.value)

    def enter(self, event):
        key = self.keyboard.getKey()
        self.value += key
        self.text.SetLabelText(self.value)

    def afterKeyboard(self):
        self.prekb.Destroy()
        self.mainPanel.SetFocus()

    def selectKeyboard(self, layout):
        if hasattr(self, 'keyboard'):
            self.verticalSizer.Detach(self.keyboard)
            self.prekb = self.keyboard
            wx.CallAfter(self.afterKeyboard)
        self.keyboard = Keyboard(self.mainPanel, layout)
        self.verticalSizer.Add(self.keyboard, 0, wx.EXPAND | wx.ALL, 10)
        self.Layout()
    layoutIndex = 0

    def onSelect(self, event: str):
        layoutCnt = len(keyboardLayouts)
        if event == 'Left' and self.keyboard.selectedKey[0] == 0:
            if self.layoutIndex == 0:
                self.layoutIndex = layoutCnt-1
            else:
                self.layoutIndex -= 1
            selectedKey = self.keyboard.selectedKey.copy()
            self.selectKeyboard(keyboardLayouts[self.layoutIndex])
            self.keyboard.selectedKey[1] = selectedKey[1]
            self.keyboard.navKey()
            return
        elif event == 'Right' and self.keyboard.selectedKey[0] == len(keyboardLayouts[self.layoutIndex][self.keyboard.selectedKey[1]])-1:
            if self.layoutIndex == layoutCnt-1:
                self.layoutIndex = 0
            else:
                self.layoutIndex += 1
            selectedKey = self.keyboard.selectedKey.copy()
            self.selectKeyboard(keyboardLayouts[self.layoutIndex])
            self.keyboard.selectedKey[1] = selectedKey[1]
            self.keyboard.selectedKey[0] = len(
                keyboardLayouts[self.layoutIndex][self.keyboard.selectedKey[1]])-1
            self.keyboard.navKey()
            return
        self.keyboard.navKey(event)

    def onDone(self, event):
        self.parent.pop({
            'key': self.params['key'],
            'value': self.value
        })
