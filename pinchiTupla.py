import math
from tkinter import *
from tkinter.colorchooser import askcolor
import math
import copy
from PIL import Image, ImageTk

root=Tk()
canvas=Canvas(root)
canvas.grid(row=0, columnspan=10)
paper=Image.new("RGB", (1024,720), "white")
usePaper = ImageTk.PhotoImage(paper)

canvas.img=usePaper
canvas.create_image(0,0, image=canvas.img)

tup=int(round(200)),int(round(200))
for x in range (400):
    paper.putpixel((x,x),1)


print(tup)
