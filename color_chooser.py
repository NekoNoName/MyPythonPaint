from tkinter import *
from tkinter.colorchooser import *

array_color=()

def getColor():
    color = askcolor()

    print(color)
    
    x = int(color[0][0])
    y = int(color[0][1])
    z = int(color[0][2])

    array_color=(x,y,z)
                 
    
    print (array_color)
    
Button(text='Select Color', command=getColor).pack()

mainloop()
