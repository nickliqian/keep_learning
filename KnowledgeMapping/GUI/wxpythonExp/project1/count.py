import wx

# import the newly created GUI file
import demo1
import os, shutil


def resizeBitmap(image, width=100, height=100):
    bmp = image.Scale(160, 80).ConvertToBitmap()
    return bmp


class CalcFrame(demo1.Frame):
    def __init__(self, parent):
        demo1.Frame.__init__(self, parent)
        # self.img_dir_path = "C:\\Users\\Nick\\Desktop\\wxpythonCode\\FailImg0829"
        # self.img_output_path = "C:\\Users\\Nick\\Desktop\\wxpythonCode\\output"
        self.img_list = os.listdir(self.img_dir_path)
        self.img_loc = 1
        self.now_img_name = self.img_list[self.img_loc]
        self.now_img_path = os.path.join(self.img_dir_path, self.now_img_name)

        img_ori = wx.Image(self.now_img_path, wx.BITMAP_TYPE_ANY)
        self.m_bitmap3.SetBitmap(resizeBitmap(img_ori, 200, 200))

        label = self.now_img_name.split("_")[0]
        self.m_staticText2.SetLabel(label)
        self.m_textCtrl1.SetValue(label)

        if not os.path.exists(self.img_output_path):
            os.makedirs(self.img_output_path)

    # Virtual event handlers, overide them in your derived class
    def pass_image(self, event):
        self.img_loc += 1
        self.now_img_name = self.img_list[self.img_loc]
        label = self.now_img_name.split("_")[0]
        self.m_staticText2.SetLabel(label)
        self.m_textCtrl1.SetValue(label)
        img_path = os.path.join(self.img_dir_path, self.now_img_name)
        img_ori = wx.Image(img_path, wx.BITMAP_TYPE_ANY)
        self.m_bitmap3.SetBitmap(resizeBitmap(img_ori, 200, 200))

    def change_then_next(self, event):
        # 读取数值
        self.now_img_name = self.img_list[self.img_loc]
        srcfile = os.path.join(self.img_dir_path, self.now_img_name)

        text = self.m_textCtrl1.GetValue()
        label = self.now_img_name.split("_")[0]
        print("b:{} >>> a:{}".format(label, text))

        change_file = text + "_" + self.now_img_name.split("_")[1] + ".png"
        dstfile = os.path.join(self.img_output_path, change_file)

        print("【{}】 -->>-->> 【{}】".format(srcfile, dstfile))

        shutil.move(srcfile, dstfile)
        self.m_textCtrl1.Clear()
        self.pass_image(self)


app = wx.App(False)
frame = CalcFrame(None)
frame.Show(True)
# start the applications
app.MainLoop()
