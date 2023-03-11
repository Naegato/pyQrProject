import wx
from os.path import exists
import qrcode

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Application qrCode')
        self.data = None
        self.panel = wx.Panel(self)
        self.my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.dialogButton = wx.Button(parent=self.panel, label="Put File")
        self.dialogButton.Bind(wx.EVT_BUTTON, self.on_press)
        self.fileDialog = wx.FileDialog(self)
        self.pathText = wx.StaticText(parent=self.panel, label="filePath", style=wx.ALIGN_CENTER)
        self.convertButton = wx.Button(parent=self.panel, label="Convert")
        self.convertButton.Bind(wx.EVT_BUTTON, self.on_convert)
        self.imageRender = wx.StaticBitmap(self.panel)
        self.my_sizer.Add(self.pathText, 0, wx.ALL | wx.EXPAND, 5)
        self.my_sizer.Add(self.dialogButton, 0, wx.ALL | wx.CENTER, 5)
        self.my_sizer.Add(self.convertButton, 0, wx.ALL | wx.CENTER, 5)
        self.my_sizer.Add(self.imageRender, 0, wx.ALL | wx.EXPAND, 5)
        self.convertButton.Hide()
        self.panel.SetSizer(self.my_sizer)
        self.panel.Layout()
        self.Show()

    def on_press(self, event):
        self.fileDialog.ShowModal()
        self.pathText.SetLabel(self.fileDialog.GetPath())
        open_file_data = open(self.fileDialog.GetPath())
        self.data = open_file_data.read()
        if self.data:
            self.convertButton.Show()
            print('data received')
        else:
            print('error no data')
            self.convertButton.Hide()
        self.reload_size()

    def on_convert(self, event):
        data_hash = hash(self.data)
        if exists(f'./result/{data_hash}.png'):
            print('already exist')
        else:
            print('convert')
            img = qrcode.make(self.data)
            img.save(f'./result/{data_hash}.png')
        png = wx.Image(f'./result/{data_hash}.png', wx.BITMAP_TYPE_ANY).Rescale(250, 250, wx.IMAGE_QUALITY_HIGH)
        self.imageRender.SetBitmap(png)
        self.reload_size()

    def scale_bitmap(bitmap, width, height):
        image = wx.ImageFromBitmap(bitmap)
        image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        result = wx.BitmapFromImage(image)
        return result

    def reload_size(self):
        self.my_sizer.Fit(self)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Layout()
    app.MainLoop()

#
# data = open('2@MI.vcf')
# print(data.read())
#
# # img = qrcode.make(data)
# # type(img)  # qrcode.image.pil.PilImage
# # img.save("some_file.png")