# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


###########################################################################
## Class Frame
###########################################################################

class Frame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"验证码识别程序", pos=wx.Point(1, 1), size=wx.Size(-1, -1),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        bSizer2.SetMinSize(wx.Size(300, 300))
        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, u"输入正确的值", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer2.Add(self.m_staticText1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, u"1111", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer2.Add(self.m_staticText2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_bitmap3 = wx.StaticBitmap(self, wx.ID_ANY, wx.NullBitmap, wx.Point(50, 50), wx.Size(160, 80), 0)
        bSizer2.Add(self.m_bitmap3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_textCtrl1.SetFont(wx.Font(25, 70, 90, 90, False, wx.EmptyString))

        bSizer2.Add(self.m_textCtrl1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button1 = wx.Button(self, wx.ID_ANY, u"下一张", wx.Point(200, 400), wx.DefaultSize, 0)
        bSizer2.Add(self.m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_button2 = wx.Button(self, wx.ID_ANY, u"正确", wx.Point(200, 400), wx.DefaultSize, 0)
        bSizer2.Add(self.m_button2, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.SetSizer(bSizer2)
        self.Layout()
        bSizer2.Fit(self)

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.change_then_next)
        self.m_button2.Bind(wx.EVT_BUTTON, self.pass_image)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def change_then_next(self, event):
        event.Skip()

    def pass_image(self, event):
        event.Skip()
