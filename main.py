import wx
import qrcode
import magic
from datetime import datetime


class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Application qrCode')
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
        charset = magic.Magic(mime_encoding=True).from_file(self.fileDialog.GetPath())

        if charset == 'binary':
            self.pathText.SetLabel(f'{self.fileDialog.GetPath()} isn\'t a text file')
            self.convertButton.Hide()
        else:
            self.pathText.SetLabel(f'{self.fileDialog.GetPath()}')
            self.convertButton.Show()
        self.reload_size()

    def on_convert(self, event):
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=100,
            border=0,
        )

        file_data = open(self.fileDialog.GetPath())
        qr.add_data(file_data.read())
        qr.make()
        img = qr.make_image(fill_color="black", back_color="transparent")

        name = f'./result/{self.fileDialog.GetFilename()}--{datetime.now().strftime("%d-%m-%Y--%H-%M-%S")}.png'

        img.save(name)

        png = wx.Image(name, wx.BITMAP_TYPE_ANY).Rescale(250, 250, wx.IMAGE_QUALITY_HIGH)
        self.imageRender.SetBitmap(png)
        self.reload_size()

    def reload_size(self):
        self.my_sizer.Fit(self)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Layout()
    app.MainLoop()