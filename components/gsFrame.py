import wx
import faulthandler


class Frame(wx.Frame):
    history = []

    def __init__(self, parent, title, routes, entry, **kwargs):
        super().__init__(parent, size=(320, 240), title=title, **kwargs)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.routes = routes
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_SIZE, self.onSizeChange)
        self.Show()
        self.push(entry['path'], entry['params'])

    def onSizeChange(self, event):
        width, height = event.GetSize()
        self.width = width
        self.height = height
        if hasattr(self, 'activePage'):
            self.activePage.onSizeChange(width, height)

        self.Layout()

    def setPage(self, page):
        if hasattr(self, 'activePage'):
            self.sizer.Detach(self.activePage)
            self.activePage.Hide()
        page.Show()
        self.activePage = page
        self.sizer.Add(page, 1, wx.EXPAND)
        if hasattr(self, 'width'):
            self.activePage.onSizeChange(self.width, self.height)
        self.activePage.SetFocus()
        self.Layout()

    def getPageClass(self, path):
        for item in self.routes:
            if item['path'] == path:
                return item['component']

    def push(self, path: str, params=None, replace=False):
        def process():
            pageClass = self.getPageClass(path)
            page = pageClass(self, params)
            record = {
                'path': path,
                'params': params,
                'page': page
            }
            if replace and len(self.history) > 0:
                removeRecord = self.history.pop()
                removeRecord["page"].Hide()

            self.history.append(record)
            page.Hide()
            self.setPage(page)
        wx.CallAfter(process)

    def pop(self,  params=None):
        def process():
            if len(self.history) <= 1:
                return
            removeRecord = self.history.pop()
            lastRecord = self.history[len(self.history)-1]
            page = lastRecord['page']
            pageToRmove = removeRecord["page"]
            self.setPage(page)
            if hasattr(page, 'onPop'):
                page.onPop(removeRecord['path'], params)
            self.sizer.Detach(pageToRmove)
            self.RemoveChild(pageToRmove)
            # wx.CallAfter(pageToRmove.Destroy)
        wx.CallAfter(process)
