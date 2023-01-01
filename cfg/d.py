from tkinter import *
from tkinter import filedialog as fd
import os
from PIL import Image


class Photoconverter:
    def init(self):
        Label_1 = Label(root, text="Browse A File", width=20, font=("bold", 15))
        Label_1.place(x=80, y=80)

        Label_3 = Label(root, text="copyright(c)2022, Alatoo International University. All rights reserved.", width=0, font=("bold", 8))
        Label_3.place(x=65, y=383)

    def jpg_to_png(self):
        filename = fd.askopenfilename()
        if filename.endswith(".jpg"):
            img = Image.open(filename)
            img.save('C:/Users/User/Desktop/IMAGES - Copy')
            print(1)
        else:
            Label_2 = Label(root, text="Error, something went wrong...", width=30, fg="blue", font=("bold", 15))
            Label_2.place(x=50, y=280)

    def jpg_to_pdf(self):
        filename = fd.askopenfilename()
        if filename.endswith(".jpg"):
            Image.open(filename).save("sample1.pdf", resolution=100.0)
        else:
            Label_2 = Label(root, text="Error, something went wrong...", width=20, fg="blue", font=("bold", 15))
            Label_2.place(x=50, y=280)

    def buttons(self):
        Button(root, text="JPG to PNG", width=20, height=2, bg="brown", fg="white", command=self.jpg_to_png).place(x=120, y=120)
        Button(root, text="JPG to PDF", width=20, height=2, bg="brown", fg="white", command=self.jpg_to_pdf).place(x=120, y=220)

    def call(self):
        self.buttons()


root = Tk()
root.geometry("400x400")
root.title("Abiy capybara's file converter")
# root.iconbitmap('D:\python img/logo.ico')

P = Photoconverter()
P.call()

root.mainloop()