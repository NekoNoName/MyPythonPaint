import math
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog
import copy
from PIL import Image, ImageTk, ImageDraw, ImageColor


class Paint(object):
    #Declaracion de directorio de los iconos
    DDAIcon='./icon/lineaDDA.png'
    BreseIcon='./icon/lineaBre.png'
    LapizIcon='./icon/edit.png'
    CircleIcon='./icon/circle-outline.png'
    ElipseIcon='./icon/elipse.png'
    TriaIcon='./icon/triangle.png'
    RectIcon='./icon/rectangle.png'
    FillIcon='./icon/fill.png'
    TransIcon='./icon/translate.png'
    ScaleIcon='./icon/scale.png'
    RotateIcon='./icon/rotation.png'
    EraserIcon='./icon/eraser.png'
    ColorIcon='./icon/pantone.png'
    ClearIcon='./icon/whitePage.png'

    dark = (0,0,0)
    white = (255,255, 255)
    
    colors=dark 
    bc=white   

    #Variable utilizadas dentro del entorno
    x=0
    y=0
    scale=False
    rotate=False
    traslate=False
    pixelList=[]
    points=[]
    clicks=0
    paperWidht=1024
    paperHeight=720
    def __init__(self):
        #La ventana
        self.root = Tk()
        #Titulo de la ventana
        self.root.title("Algoritmos")
        
        #Menu desplegable
        menubar = Menu(self.root)
        fileMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="New", command=self.clearCanvas)
        fileMenu.add_command(label="Open", command=self.callOpenImage)
        fileMenu.add_command(label="Save", command=self.callSaveImage)
        fileMenu.add_command(label="Save as...", command=self.callSaveAsImage)
        fileMenu.add_command(label="Exit", command=self.root.quit)
        self.root.config(menu=menubar)
        
        #Creacion de iconos para poner en los botones
        self.iconDDA=PhotoImage(file=self.DDAIcon)
        self.iconBre=PhotoImage(file=self.BreseIcon)
        self.iconPencil=PhotoImage(file=self.LapizIcon)
        self.iconCircle=PhotoImage(file=self.CircleIcon)
        self.iconElipse=PhotoImage(file=self.ElipseIcon)
        self.iconTria=PhotoImage(file=self.TriaIcon)
        self.iconRect=PhotoImage(file=self.RectIcon)
        self.iconFill=PhotoImage(file=self.FillIcon)
        self.iconTrans=PhotoImage(file=self.TransIcon)
        self.iconScale=PhotoImage(file=self.ScaleIcon)
        self.iconRotate=PhotoImage(file=self.RotateIcon)
        self.iconEraser=PhotoImage(file=self.EraserIcon)
        self.iconColor=PhotoImage(file=self.ColorIcon)
        self.iconClear=PhotoImage(file=self.ClearIcon)

        #Los botones
        
        #Botones de la primera fila
        #Boton Limpiar Canvas
        self.clear_button = Button(self.root, text='Limpiar', image=self.iconClear, width="30", height="30",command=self.clearCanvas)
        self.clear_button.grid(row=1, column=10)


         #Resto de botones que vinieron con el codigo
        self.color_button = Button(self.root, text='color', image=self.iconColor, width="30", height="30", command=self.choose_color)
        self.color_button.grid(row=1, column=9)

        
        self.eraser_button = Button(self.root, text='eraser', image=self.iconEraser,width="30", height="30",command=self.use_eraser)
        self.eraser_button.grid(row=1, column=11)



        self.choose_size_button = Scale(self.root, from_=1, to=100, orient=HORIZONTAL)
        self.choose_size_button.grid(row=1, column=12)

        #Botones de la segunda fila

        #Boton Lapiz, vino de base.
        self.pen_button = Button(self.root, text='lapiz', image=self.iconPencil,width="30", height="30",command=self.use_pen)
        self.pen_button.grid(row=1, column=0)

        #Boton DDA
        self.brush_button = Button(self.root, text='DDA', image=self.iconDDA,width="30", height="30", command=self.dda)
        self.brush_button.grid(row=1, column=1)

        #Boton Bresenham
        self.Bresenham_button = Button(self.root, text='Bresenham',image=self.iconBre,width="30", height="30", command=self.Bresenham)
        self.Bresenham_button.grid(row=1, column=2)
        

        #Boton Triangulo
        self.triang_button = Button(self.root, text='Triangulo', image=self.iconTria,width="30", height="30",command=self.triangulo)
        self.triang_button.grid(row=1, column=3)

        #Boton box
        self.Box_button = Button(self.root, text = 'Box', image=self.iconRect,width="30", height="30", command= self.box)
        self.Box_button.grid(row=1, column=4)

        #Boton Circulo
        self.circulo_button = Button(self.root, text="Circulo", image=self.iconCircle,width="30", height="30", command= self.circulo)
        self.circulo_button.grid(row= 1, column= 5)

        #Boton Elipse
        self.elipse_button = Button(self.root, text="Elipse", image=self.iconElipse,width="30", height="30",command= self.elipse)
        self.elipse_button.grid(row=1, column=6) 

        #Boton Relleno
        self.fill_button = Button (self.root, text="Relleno", image=self.iconFill,width="30", height="30",command=self.fill)
        self.fill_button.grid(row=1, column=20)

        #Boton Translacion
        self.transi_button = Button (self.root, text="Translacion",image=self.iconTrans,width="30", height="30", command=self.transitionTool)
        self.transi_button.grid(row=1, column=21)

        #Boton Escala
        self.scale_button = Button(self.root, text='Escalado', image=self.iconScale,width="30", height="30", command=self.scalingTool)
        self.scale_button.grid(row=1, column=22)

        

        #Boton Rotacion
        self.rotate_button = Button(self.root, text='Rotacion', image=self.iconRotate, width="30", height="30", command=self.rotationTool)
        self.rotate_button.grid(row=1, column=23)


       


        #El Canvas
        self.c = Canvas(self.root, bg='white', width=self.paperWidht, height=self.paperHeight)
        self.c.grid(row=8, columnspan=24)


       

    

        self.bgcolor="white"

        #Creando la Imagen que sera usado como el papel
        self.paper = Image.new("RGB", (self.paperWidht,self.paperHeight), self.bgcolor)
        self.usePaper = ImageTk.PhotoImage(self.paper)
        self.c.img = self.usePaper
        self.c.create_image(0, 0, image=self.c.img)

        self.setup()
        #Parte del codigo de la ventana grafica.
        self.root.mainloop()

    def setup(self):
        self.eraser_on = False
        self.lapiz_on=True
        self.line=False
        self.line_DDA=True
        self.circle=False
        self.c.configure(cursor="crosshair")
        self.active_button = self.pen_button
        self.activate_button(self.pen_button)
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onPencilDraw)
        self.c.bind("<ButtonRelease-1>", self.onPencilDraw)
        self.c.bind("<Motion>", self.canxy)


    #Funcion para iniciar datos, vino con el codigo base pero decidi aprovecharlo
    def callOpenImage(self):
        self.fOpenName = filedialog.askopenfilename(filetypes=(("Supported Image Files", "*.jpg; *.jpeg; *.png; *.bmp; *.ico"),
                                        ("All files", "*.*") )) 
        if not self.fOpenName:
            return
        self.c.delete("all")

        self.paper = Image.open(self.fOpenName).resize((self.paperWidht,self.paperHeight))
        self.usePaper = ImageTk.PhotoImage(self.paper)

        self.c.img = self.usePaper
        self.c.create_image(self.paperWidht/2, self.paperHeight/2 , image=self.c.img)

    def callSaveImage(self):
        if self.fOpenName != None:
            self.paper.save(self.fOpenName)
            return

        fname = filedialog.asksaveasfilename(defaultextension=".png")
        if not fname: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        self.paper.save(fname)

    def callSaveAsImage(self):
        fname = filedialog.asksaveasfilename(defaultextension=".png")
        if not fname: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        self.paper.save(fname)
    

    
    def clearCanvas(self):
        self.c.delete("all")
        self.paper = Image.new("RGB", (self.paperWidht,self.paperHeight), self.bgcolor)

    #GUarda la coordenada del click
    def onClickPress(self, event):
        self.x, self.y = event.x, event.y
    #Crea las lineas mientras se mueve, no es permanente
    def onMotionLine(self, event):
        x1,y1 =self.x, self.y
        x2, y2 = event.x, event.y
        paper=copy.copy(self.paper)
        if self.line_DDA:
            self.lineImg=self.drawDDA(x1,y1,x2,y2, paper)
        else:
            self.lineImg=self.drawBresenham(x1,y1,x2,y2,paper)
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=self.lineImg)
    #Crea la linea final
    def onReleaseLine(self, event):
        x1,y1 =self.x, self.y
        x2, y2 = event.x, event.y
        if self.line_DDA:
            self.lineImg=self.drawDDA(x1,y1,x2,y2, self.paper)
        else:
            self.lineImg=self.drawBresenham(x1,y1,x2,y2,self.paper)
       
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=self.lineImg)
    #Crea el circulo o elipse temporal
    def onMotionCircle(self, event):
        x1,y1 =self.x, self.y
        x2, y2 = event.x, event.y
        paper=copy.copy(self.paper)
        #Si es circulo
        if self.circle:    
            #Obtengo Radio de la distancia media de la mitad de x a x2 
            radio= int(abs((x2+x1)/2-x2))
            cx=int((x2+x1)/2)
            cy=int((y2+y1)/2)
            self.circleImg=self.drawCircleDDA(radio, cx, cy, paper)
        else:
            radioX= int(abs((x2+x1)/2-x2))  
            radioY= int(abs((y2+y1)/2-y2))
            cx=int((x2+x1)/2)
            cy=int((y2+y1)/2)
            self.circleImg=self.drawElipse(cx, cy, radioX, radioY, self.colors, paper)
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=self.circleImg)

    def onReleaseCircle(self, event):
        x1,y1 =self.x, self.y
        x2, y2 = event.x, event.y
        if self.circle:    
            radio= int(abs((x2+x1)/2-x2))
            cx=int((x2+x1)/2)
            cy=int((y2+y1)/2)
            self.circleImg=self.drawCircleDDA(radio, cx, cy, self.paper)
        else:
            radioX= int(abs((x2+x1)/2-x2))  
            radioY= int(abs((y2+y1)/2-y2))
            cx=int((x2+x1)/2)
            cy=int((y2+y1)/2)
            self.circleImg=self.drawElipse(cx, cy, radioX, radioY, self.colors, self.paper)
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=self.circleImg)


    #Corre Algoritmo DDA
    def dda(self):
        self.line_DDA=True
        self.activate_button(self.brush_button)
        self.c.configure(cursor="crosshair")
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onMotionLine)
        self.c.bind("<ButtonRelease-1>", self.onReleaseLine)
        #self.label1.config(text="DDA")
  
 
    #Algoritmo Bresenham
    def Bresenham(self):
     
        self.line_DDA=False
        #self.label1.config(text="Bresenham")
        self.c.configure(cursor="crosshair")
        self.activate_button(self.Bresenham_button)
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onMotionLine)
        self.c.bind("<ButtonRelease-1>", self.onReleaseLine)
    

    #Funcion Circulo
    def circulo(self):
        self.activate_button(self.circulo_button)
        self.c.configure(cursor="crosshair")
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onMotionCircle)
        self.c.bind("<ButtonRelease-1>", self.onReleaseCircle)
        self.circle=True
        
       
    #Funcion elipse
    def elipse(self):
        self.activate_button(self.elipse_button)
        self.c.configure(cursor="crosshair")
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onMotionCircle)
        self.c.bind("<ButtonRelease-1>", self.onReleaseCircle)
        self.circle=False
        
        


    #Funcion Triangulo
    def triangulo(self):
        self.activate_button(self.triang_button)
        self.c.configure(cursor="crosshair")
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onTrianguloMotion)
        self.c.bind("<ButtonRelease-1>", self.onTrianguloRelease)
        
    def drawTriangulo(self, x1,y1,x2,y2,x3,y3, img):    
        self.lineImg=self.drawDDA(x1,y1,x2,y2,img)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)
        self.lineImg2=self.drawDDA(x2,y2,x3,y3, img)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg2)
        self.lineImg3=self.drawDDA(x1,y1,x3,y3, img)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg3)
    
    def onTrianguloMotion(self, event):
        x1,y1=int(self.x), int(event.y)  
        x2,y2=int(event.x), int(event.y)
        x3=int((x2+x1)/2)
        y3=int(self.y) 
        paper=copy.copy(self.paper)
        self.drawTriangulo(x1,y1,x2,y2,x3,y3,paper)
    
    def onTrianguloRelease(self, event):
        x1,y1=int(self.x), int(event.y)  
        x2,y2=int(event.x), int(event.y)
        x3=int((x2+x1)/2)
        y3=int(self.y) 
        self.drawTriangulo(x1,y1,x2,y2,x3,y3,self.paper)
        

    def box(self):
        self.activate_button(self.Box_button)
        self.c.configure(cursor="crosshair")
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onBoxMotion)
        self.c.bind("<ButtonRelease-1>", self.onBoxRelease)
        

    def onBoxMotion(self, event):
        x1,y1=self.x, self.y
        x2,y2=event.x, event.y
        paper=copy.copy(self.paper)
        self.drawBox(x1,y1,x2,y2,paper)

    def onBoxRelease(self, event):
        x1,y1=self.x, self.y
        x2,y2=event.x, event.y
        self.drawBox(x1,y1,x2,y2,self.paper)   


    #Funcion Box
    def drawBox(self,x1,y1,x2,y2, img):
        
        self.lineImg=self.drawDDA(x1,y1,x1,y2, img)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)
        self.lineImg=self.drawDDA(x1,y1,x2,y1, img)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)
        self.lineImg=self.drawDDA(x1,y2,x2,y2, img)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)
        self.lineImg=self.drawDDA(x2,y1,x2,y2, img)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)

    #Funcion relleno
    def fill(self):
        self.activate_button(self.fill_button)
        self.c.configure(cursor="spraycan")
        self.c.bind("<ButtonPress-1>", self.fillColors)
        self.c.bind("<B1-Motion>", self.nothing)
        self.c.bind("<ButtonRelease-1>", self.release)

    def release(self, event):
        pass    

    def transitionTool(self):
        self.activate_button(self.transi_button)
        self.traslate=True
        self.rotate=False
        self.scale=False
        self.c.configure(cursor="crosshair")
        self.c.config(cursor="crosshair")
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onChoosingMotion)
        self.c.bind("<ButtonRelease-1>", self.onChoosingRelease)


    def rotationTool(self):
        print ("Rotate tool")
        self.activate_button(self.rotate_button)
        self.rotate=True
        self.traslate=False
        self.scale=False
        self.c.configure(cursor="crosshair")
        self.c.config(cursor="crosshair")
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onChoosingMotion)
        self.c.bind("<ButtonRelease-1>", self.onChoosingRelease)
 
    def scalingTool(self):
        self.activate_button(self.scale_button)
        self.scale=True
        self.rotate=False
        self.traslate=False
        self.c.configure(cursor="crosshair")
        self.c.config(cursor="crosshair")
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onChoosingMotion)
        self.c.bind("<ButtonRelease-1>", self.onChoosingRelease)


    def onChoosingMotion(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)
        paper = copy.copy(self.paper)
        self.drawBox(x0,y0, x1, y1, paper)

    def onChoosingRelease(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)
        self.transitionPlace = ((x0, y0), (x1, y1))
        self.c.config(cursor="crosshair")
        if self.traslate:
            self.c.bind("<ButtonPress-1>", self.onClickPress)
            self.c.bind("<B1-Motion>", self.onTransitionMotion)
            self.c.bind("<ButtonRelease-1>", self.onTransitionRelease)
        if self.scale:
            self.c.bind("<ButtonPress-1>", self.onClickPress)
            self.c.bind("<B1-Motion>", self.onScaleMotion)
            self.c.bind("<ButtonRelease-1>", self.onScaleRelease)    
        if self.rotate:
            self.c.bind("<ButtonPress-1>", self.onClickPress)
            self.c.bind("<B1-Motion>", self.onRotateMotion)
            self.c.bind("<ButtonRelease-1>", self.onRotateRelease)


    def onTransitionMotion(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)

        paper = copy.copy(self.paper)
        bg=(255,255,255)
        if not self.pixelList:
            self.pixelList = self.cropping(self.transitionPlace[0], self.transitionPlace[1], bg, paper)

        self.transitImg = self.moveTransition(self.pixelList, (x1, y1), bg, paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.transitImg)

    def onTransitionRelease(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)
        bg=(255,255,255)
        if self.pixelList:
            self.eraseSelectedCropping(self.pixelList, bg, self.paper)

        self.transitImg = self.moveTransition(self.pixelList, (x1, y1), bg, self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.transitImg)

        self.pixelList = None
        self.transitionTool()

    def onRotateMotion(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)

        paper = copy.copy(self.paper)

        if x1 > x0:
            alpha = math.atan((y0-y1) / float(x0-x1))
        else:
            alpha = math.pi + math.atan((y0-y1) / float(x0-x1))

        print (alpha)

        if not self.pixelList:
            self.pixelList = self.cropping(self.transitionPlace[0], self.transitionPlace[1], self.bc, paper)

        self.rotateImg = self.moveRotation(self.pixelList, (x0, y0), alpha, self.bc, paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.rotateImg)

    def onRotateRelease(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)
        alpha = math.atan(y1 / float(x1))

        if x1 > x0:
            alpha = math.atan((y0-y1) / float(x0-x1))
        else:
            alpha = math.pi + math.atan((y0-y1) / float(x0-x1))

        if self.pixelList:
            self.eraseSelectedCropping(self.pixelList, self.bc, self.paper)

        self.rotateImg = self.moveRotation(self.pixelList, (x0, y0), alpha, self.bc, self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.rotateImg)

        self.rotationTool()
        self.pixelList = None


    def onScaleMotion(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)

        paper = copy.copy(self.paper)
        scaleX = x1/float(x0)
        scaleY = y1/float(y0)

        if not self.pixelList:
            self.pixelList = self.cropping(self.transitionPlace[0], self.transitionPlace[1], self.bc, paper)

        self.scaleImg = self.scalling(self.pixelList, (x0, y0), (scaleX, scaleY), paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.scaleImg)

    def onScaleRelease(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)

        scaleX = x1/float(x0)
        scaleY = y1/float(y0)

        if self.pixelList:
            self.eraseSelectedCropping(self.pixelList, self.bc, self.paper)

        self.scaleImg = self.scalling(self.pixelList, (x0, y0), (scaleX, scaleY), self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.scaleImg)

        self.pixelList = None
        self.scalingTool()


    def moveTransition(self, pixelList, newPoint, bc, img):
        deltaX = newPoint[0] - pixelList[0][0][0]
        deltaY = newPoint[1] - pixelList[0][0][1]

        for i in range(0, len(pixelList) - 1):
            pixel = pixelList[i]
            img.putpixel((pixel[0][0] + deltaX, pixel[0][1] + deltaY), pixel[1])

        transitImg = ImageTk.PhotoImage(img)
        return transitImg

    #Escalado de imagen
    def scalling(self, pixelList, center, scale, img):
        centerX = center[0]
        centerY = center[1]

        # render new pattern based on coordinate of newPoint
        for i in range(0, len(pixelList) - 1):
            pixel = self.pixelList[i]

            x = centerX + int(round((pixel[0][0] - centerX) * scale[0]))
            y = centerY + int(round((pixel[0][1] - centerY) * scale[1]))

            img.putpixel((x, y), pixel[1])

        scaleImg = ImageTk.PhotoImage(img)
        return scaleImg


    #Rotacion
    def moveRotation(self,pixelList, center, alpha, bc, img):
        for i in range(0, len(pixelList) - 1):
            pixel = self.pixelList[i]

            centerX = center[0]
            centerY = center[1]

            x = centerX + int(math.cos(alpha) * (pixel[0][0] - centerX) - math.sin(alpha) * (pixel[0][1] - centerY ))
            y = centerY + int(math.sin(alpha) * (pixel[0][0] - centerX) + math.cos(alpha) * (pixel[0][1] - centerY ))

            img.putpixel((x, y), pixel[1])

        roateImg = ImageTk.PhotoImage(img)
        return roateImg   

    #Guarda los pixeles de un area seleccionado
    def cropping(self, startPoint, endPoint, bc, img):
        pixelList = []

        x0 = startPoint[0]
        y0 = startPoint[1]
        x1 = endPoint[0]
        y1 = endPoint[1]

        if y0 > y1:
            y0, y1 = y1, y0
        if x0 > x1:
            x0, x1 = x1, x0

        for j in range(y0, y1):
            for i in range(x0, x1):
                if img.getpixel((i, j)) != bc:
                    color = img.getpixel((i, j))
                    pixelObj = ((i,j), color)
                    pixelList.append(pixelObj)
                    img.putpixel((i,j), bc)

        return pixelList
    #Escoger Color
    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor()[0]
        self.colors=(int(self.color[0]), int(self.color[1]), int(self.color[2]))

    #Activa Borrador
    def use_eraser(self):
        self.activate_button(self.eraser_button)
        self.c.configure(cursor="crosshair")
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.eraser_motion)
        self.c.bind("<ButtonRelease-1>", self.eraser_motion)
        
        
        #self.activate_button(self.eraser_button, eraser_mode=True)

    def eraser_motion(self,event):
        size = self.choose_size_button.get()
        puntos=(self.x, self.y, event.x, event.y)
        #self.c.create_line(self.x, self.y, event.x, event.y, width=size, fill="white")
        self.img=self.eraser(puntos, size, self.paper)
        self.x, self.y = event.x, event.y
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.img)
        
    
    def eraser_release(self, event):
        lol=ImageTk.PhotoImage(self.paper)
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=lol)
    
    def eraser(self, puntos, size, img):
        draw=ImageDraw.Draw(img)
        draw.line((puntos), fill=self.white, width=size)
        imagen=ImageTk.PhotoImage(img)
        return imagen
        
    #Le da efecto de boton seleccionado
    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    #Vino de base, es el lapiz.
    def paint(self, event):
        if self.lapiz_on or self.eraser_on:
            self.line_width = self.choose_size_button.get()
            paint_color = 'white' if self.eraser_on else self.color
            if self.old_x and self.old_y:
                self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                                   width=self.line_width, fill=paint_color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
            self.old_x = event.x
            self.old_y = event.y



    #Vino de base, reinicia las coordenadas x y
    def reset(self, event):
        self.old_x, self.old_y = None, None



    #Algoritmo DDA
    def drawDDA(self,x1,y1,x2,y2, img):
            #x1,y1 = x1,y1
            print("DDA line algorithm")
            self.length = abs(x2-x1) if abs(x2-x1) >= abs(y2-y1) else abs(y2-y1)
            if self.length>0:
                dx = (x2-x1)/float(self.length)
                dy = (y2-y1)/float(self.length)

                for i in range(self.length):
                        #self.c.create_line(x1, y1, x1, y1, width=2, fill=self.color, capstyle=ROUND, smooth=TRUE, splinesteps=36)
                        img.putpixel((int(x1), int(y1)), self.colors)
                        x1 += dx
                        y1 += dy
            else:
                #self.c.create_line(x1,y1,x2,y2)
                img.putpixel((x1,y1), self.colors)
            lineImg = ImageTk.PhotoImage(img)
            return lineImg
    #Algoritmo Bresenham
    def drawBresenham(self,x1,y1,x2,y2, img):
        print("Bresenham's line algorithm")
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        sx = -1 if x1 > x2 else 1
        sy = -1 if y1 > y2 else 1
        if dx > dy:
            err = dx / 2.0
            while x != x2:
                img.putpixel((x,y), self.colors)
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y2:
                img.putpixel((x,y), self.colors)
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy        
        img.putpixel((x,y), self.colors)      
        lineImg = ImageTk.PhotoImage(img)
        return lineImg
        

    def circleputpixel(self, x, y, cemtroX, cemtroY, img):
        img.putpixel((cemtroX+x,cemtroY+y), self.colors)
        img.putpixel((cemtroX-x,cemtroY+y), self.colors)
        img.putpixel((cemtroX-x,cemtroY-y), self.colors)
        img.putpixel((cemtroX+x,cemtroY-y), self.colors)

        img.putpixel((cemtroX+y,cemtroY+x), self.colors)
        img.putpixel((cemtroX+y,cemtroY-x), self.colors)
        img.putpixel((cemtroX-y,cemtroY+x), self.colors)
        img.putpixel((cemtroX-y,cemtroY-x), self.colors)

       
    
    #Algoritmo Circulo DDA
    def drawCircleDDA(self,rad, cx, cy, img):
        print("Circle Algorithm")
        rx= rad
        x= round(rx)
        y=0
        cemtroX=cx #Valor X de prueba del centro del circulo
        cemtroY=cy #Valor Y de prueba del centro del circulo
        while y<=x:
            self.circleputpixel(x,y, cemtroX, cemtroY, img)
            rx= rx-y/rx
            x= round(rx)
            y=y+1
        circleImg = ImageTk.PhotoImage(img)
        return circleImg
        #print("fin")
    
    def elipseputpixel(self,centroX, centroY, x, y, color, img):
        img.putpixel((centroX+x, centroY+y), color)
        img.putpixel((centroX-x, centroY+y), color)
        img.putpixel((centroX+x, centroY-y), color)
        img.putpixel((centroX-x, centroY-y), color)
            
    def drawElipse(self,centroX,centroY, rx, ry, color, img):
        rxSq = rx ** 2
        rySq = ry ** 2
        x = 0
        y = int(ry)
        px = 0
        py = 2 * rxSq * y
        self.elipseputpixel(centroX, centroY, x, y, color, img)
        p = rySq - (rxSq * ry) + (0.25 * rxSq)
        while px < py:
            x = x + 1
            px = px + 2*rySq
            if p < 0:
                p = p + rySq + px
            else:
                y = y - 1
                py = py - 2*rxSq
                p = p + rySq + px - py
            self.elipseputpixel(centroX, centroY, x, y, color, img)

        p = rySq*(x+0.5)*(x+0.5) + rxSq*(y-1)*(y-1) - rxSq*rySq
        while y > 0:
            y = y - 1
            py = py - 2 * rxSq
            if p > 0:
                p = p + rxSq - py
            else:
                x = x + 1
                px = px + 2 * rySq
                p = p + rxSq - py + px
            self.elipseputpixel(centroX, centroY, x, y, color, img)

        eclipseImg = ImageTk.PhotoImage(img)
        return eclipseImg
    
    def fillColors(self, event):
        center=(event.x, event.y)
        self.filledImg=self.fillColor(center, self.paper)
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image= self.filledImg)

        #Relleno
    def fillColor(self, center, img):
        print ('center ', center)
        newColor=self.colors
        oldColor = self.paper.getpixel(center)
        if oldColor == newColor:
            return
            

        listaPixRelleno = []
        listaPixRelleno.append(center)
        while listaPixRelleno:
            seed = listaPixRelleno.pop(0)
            try:
                seedColor = img.getpixel(seed)
            except IndexError:
                seedColor = None
            if  seedColor == oldColor:
                img.putpixel(seed, newColor)
                x, y = seed[0], seed[1]
                listaPixRelleno.append((x+1, y))
                listaPixRelleno.append((x-1, y))
                listaPixRelleno.append((x, y+1))
                listaPixRelleno.append((x, y-1))

        filledImg = ImageTk.PhotoImage(img)
        
        return filledImg
    
    def on_button_choosing_place_motion(self, event):
        x0,y0 = (self.x, self.y)
        x1,y1 = (event.x, event.y)

        paper = copy.copy(self.paper)
        self.drawBox(x0,y0, x1, y1,paper)
        

    
    def eraseSelectedCropping(self, pixelList, bc, img):
        for i in self.pixelList:
            img.putpixel(i[0], bc)


    #Para saber las coordenadas del cursor en el canvas
    def canxy(self, event):
        self.root.title(" Algoritmos ( %i , %i)" %(event.x, event.y))

    def pencil(self, previousPoint, pointNow, color, img):
        draw = ImageDraw.Draw(img)
        draw.line((previousPoint, pointNow), color)

        pencilImg = ImageTk.PhotoImage(img)
        return pencilImg

    def onPencilDraw(self, event):
        
        #self.pencilImg = self.pencil(previousPoint, pointNow, self.color, self.paper)
        self.drawDDA(self.x, self.y, event.x, event.y, self.paper)
        self.pencilImg=ImageTk.PhotoImage(self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.pencilImg)
        self.x = event.x
        self.y = event.y

    #Accion del boton Lapiz
    def use_pen(self):
        self.activate_button(self.pen_button)
        self.lapiz_on=True
        self.line=False
        self.c.configure(cursor="crosshair")
        print('Icono de cursor obtenido de: "https://www.freepik.com/?__hstc=57440181.dfb3ad532d753cdc1cb7d881068f2af0.1560116626434.1560116626434.1560116626434.1&__hssc=57440181.2.1560116626435&__hsfp=2958300247" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" 			    title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/" 			    title="Creative Commons BY 3.0')
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onPencilDraw)
        self.c.bind("<ButtonRelease-1>", self.onPencilDraw)

    def nothing(self,event):
        pass

if __name__ == '__main__':
    Paint()
