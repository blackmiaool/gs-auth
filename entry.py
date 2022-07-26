import wx
import faulthandler
from components.gsFrame import Frame
from pages.inputPage import InputPage
from pages.alertPage import AlertPage
from pages.authPage import AuthPage
from pages.pwdPage import PwdPage
from pages.confirmPage import ConfirmPage
from common.globalVars import globalVars

faulthandler.enable()
app = wx.App(False)
routes = [
    {'path': '/input', 'component': InputPage},
    {'path': '/alert', 'component': AlertPage},
    {'path': '/auth', 'component': AuthPage},
    {'path': '/pwd', 'component': PwdPage},
    {'path': '/confirm', 'component': ConfirmPage},
]

Frame(None, 'Gameshell Auth', routes, {
    'path': '/pwd',
    'params': {}
})

app.MainLoop()
