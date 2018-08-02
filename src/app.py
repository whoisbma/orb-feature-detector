import sys, os
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk 
import numpy as np
import cv2 as cv


class CV_Analyzer:
  def __init__(self):
    self.orb = cv.ORB_create()

  def processImageForCV(self, image):
    np_img = np.asarray(image)
    np_img = cv.cvtColor(np_img, cv.COLOR_RGB2BGR)
    kp1, des1 = self.orb.detectAndCompute(np_img, None)
    # print(len(kp1))
    np_img2 = cv.drawKeypoints(np_img, kp1, None, color=(0,255,0), flags=0)
    np_img2 = cv.cvtColor(np_img2, cv.COLOR_BGR2RGB)
    pil_img = Image.fromarray(np_img2)
    return (pil_img, len(kp1))



class GUI:
  def __init__(self):
    self.cva = CV_Analyzer()

    self.FONT_LARGE= ("Verdana", 24)
    self.FONT_SMALL= ("Verdana", 12)
    
    self.root = tk.Tk()
    self.root.title("CV Image Tester")

    self.titleframe = tk.Frame(self.root)
    self.imageframe = tk.Frame(self.root)
    
    self.currentImageName = ""
    
    self.resultNum = tk.StringVar()
    self.resultNum.set(str(0))
    self.resultNum.trace("w", self.callback)

    self.resultLabel = tk.Label(self.imageframe, text = "Number of detected features: %s" % self.resultNum.get(), font=self.FONT_SMALL)

    self.tkimg = ImageTk.PhotoImage(image='RGBA', size=(0,0))

    self.currImage = tk.Label(self.imageframe, image = self.tkimg)
    self.currImage.image = self.tkimg
    self.currImage.pack()

    tk.Label(self.titleframe, text="CV Image Tester", font=self.FONT_LARGE).pack(pady=10, padx=10)
    tk.Label(self.titleframe, text="load an image to check its feature robustness", font=self.FONT_SMALL).pack(pady=10, padx=10)


    self.scrollbar = tk.Scrollbar(self.root)
    self.scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    self.listbox = tk.Listbox(self.root, yscrollcommand=self.scrollbar.set)
    self.listbox.bind('<<ListboxSelect>>', self.curSelect)
    self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    button = tk.Button(self.titleframe, text="Load image", command = self.OpenFile).pack(pady=10, padx=10)

    self.titleframe.pack()
    self.imageframe.pack()
    self.resultLabel.pack(pady=10, padx=10)

    self.menu = tk.Menu(self.root)
    self.root.config(menu=self.menu)
    
    self.file = tk.Menu(self.menu)
    self.file.add_command(label = 'Open', command = self.OpenFile)
    self.file.add_command(label = 'Exit', command = lambda:sys.exit())
    self.menu.add_cascade(label = 'File', menu = self.file)

    tk.mainloop()

  def callback(self, n, m, x):
    self.resultLabel.configure(text='Number of detected features: %s' % self.resultNum.get())

  def displayImageFromPath(self, path):
    # try:
    im = Image.open(path)
    im, result = self.cva.processImageForCV(im)
    self.resultNum.set(result)
    if (im.height > 400 or im.width > 400):
      im = self.resizeForScale(im.height/im.width, im)

    self.tkimg = ImageTk.PhotoImage(im)
    self.currImage.configure(image=self.tkimg)
    self.currImage.image = self.tkimg
    self.currentImageName = path
    # except:
    #   print("Error on image load")
    #   sys.exit()

  def resizeForScale(self, ratio, image):
    w = 400
    h = int(400 * ratio)
    resized = image.resize((w, h), Image.ANTIALIAS)
    return resized

  def curSelect(self, event):
    widget = event.widget
    selection = widget.curselection()
    if not selection:
      return
    picked = widget.get(selection[0])
    if picked == self.currentImageName: 
      return

    self.displayImageFromPath(picked)

  def OpenFile(self):
    name = askopenfilename(initialdir = os.path.dirname(__file__),
                           filetypes = [("Image File",'.jpg'),("Image File",'.png')],
                           title = "Choose a file"
                          )
    if not name:
      return
    currentList = self.listbox.get(0, tk.END)
    if name in currentList:
      return
    self.displayImageFromPath(name)
    self.listbox.insert(tk.END, name)



if __name__ == "__main__":
  gui = GUI()