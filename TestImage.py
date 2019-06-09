import math
from tkinter import *
from tkinter.colorchooser import askcolor
import math
import copy
from PIL import Image, ImageTk, ImageDraw, ImageColor


class Paint(object):
    red = (255,0,0)
    dark = (0,0,0)
    green = (0, 255, 0)
    yellow = (255, 204, 0)
    orange = (255, 102, 0)
    white = (255,255, 255)
    pink = (255, 186, 210)
    blueLight = (0, 153, 204)
    blueMalibu = (102, 204, 255)
    purple = (102, 0, 204)  
    colors=dark    
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'
    x=0
    y=0
    xf=0
    yf=0
    
    pixelList=[]
    clicks=0
    paperWidht=1024
    paperHeight=720
    def __init__(self):
        #La ventana
        self.root = Tk()
        #Titulo de la ventana
        self.root.title("Algoritmos")

        #Los botones
        #Boton Lapiz, vino de base.
        self.pen_button = Button(self.root, text='lapiz', command=self.use_pen)
        self.pen_button.grid(row=0, column=16)


        #Boton DDA
        self.brush_button = Button(self.root, text='DDA', command=self.dda)
        self.brush_button.grid(row=4, column=1)

        #Boton Circulo
        self.circulo_button = Button(self.root, text="Circulo", command= self.circulo)
        self.circulo_button.grid(row= 0, column= 8)

        #Boton Triangulo
        self.triang_button = Button(self.root, text='Triangulo', command=self.triangulo)
        self.triang_button.grid(row=0, column=4)

        #Boton Bresenham
        self.Bresenham_button = Button(self.root, text='Bresenham', command=self.Bresenham)
        self.Bresenham_button.grid(row=0, column=10)

        #Boton box
        self.Box_button = Button(self.root, text = 'Box', command= self.box)
        self.Box_button.grid(row=0, column=12)

        #Boton para hacer lineas con clicks
        self.algo_button = Button(self.root, text='Lineas', command=self.do_something)
        self.algo_button.grid(row=0, column=18)

        #Boton Elipse
        self.elipse_button = Button(self.root, text="Elipse", command= self.elipse)
        self.elipse_button.grid(row=0, column=20)    

        #Boton Relleno
        self.fill_button = Button (self.root, text="Relleno", command=self.fill)
        self.fill_button.grid(row=0, column=24)


        #Boton Translacion
        self.transi_button = Button (self.root, text="Translacion", command=self.transitionTool)
        self.transi_button.grid(row=0, column=22)

        #Resto de botones que vinieron con el codigo
        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=25)

        
        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=23)



        self.choose_size_button = Scale(self.root, from_=1, to=100, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=25)


        #El Canvas
        self.c = Canvas(self.root, bg='white', width=self.paperWidht, height=self.paperHeight)
        self.c.grid(row=8, columnspan=28)


        

        #Entrada de Datos Circulo
        self.cir=Entry(self.root)
        self.cir.grid(row=1, column=8)

        self.cx=Entry(self.root)
        self.cx.grid(row=2, column=8)

        self.cy=Entry(self.root)
        self.cy.grid(row=3, column=8)

        self.ry=Entry(self.root)
        self.ry.grid(row=1, column=20)

        #Entrada de Datos Triangulo
        self.tr= Entry(self.root)
        self.tr.grid(row=1, column=4)

        self.tr2= Entry(self.root)
        self.tr2.grid(row=2, column=4)

        self.tr3= Entry(self.root)
        self.tr3.grid(row=3, column=4)

        self.tr4= Entry(self.root)
        self.tr4.grid(row=4, column=4)

        self.tr5= Entry(self.root)
        self.tr5.grid(row=1, column=6)

        self.tr6= Entry(self.root)
        self.tr6.grid(row=2, column=6)

        

        #Los Labels Triangulo
        Label(self.root, text="X1").grid(row=1, column=3)
        Label(self.root, text="Y1").grid(row=2, column=3)
        Label(self.root, text="X2").grid(row=3, column=3)
        Label(self.root, text="Y2").grid(row=4, column=3)
        Label(self.root, text="X3").grid(row=1, column=5)
        Label(self.root, text="Y3").grid(row=2, column=5)

        #Los Labels del Circulo
        Label(self.root, text="Radio").grid(row=1, column=7)
        Label(self.root, text="Centro x").grid(row=2, column=7)
        Label(self.root, text="Centro y").grid(row=3, column=7)

        #Label
        self.label1=Label(self.root, text="DDA")
        self.label1.grid(row=1, column=18)

        self.bgcolor="white"
        self.paper = Image.new("RGB", (self.paperWidht,self.paperHeight), self.bgcolor)
        self.usePaper = ImageTk.PhotoImage(self.paper)
        self.c.img = self.usePaper
        self.c.create_image(0, 0, image=self.c.img)

        self.setup()
        #Parte del codigo de la ventana grafica.
        self.root.mainloop()


    #Funcion para iniciar datos, vino con el codigo base pero decidi aprovecharlo
                       
    def setup(self):
    
        self.old_x = None
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        
        self.eraser_on = False
        self.lapiz_on=True
        self.line=False
        self.line_DDA=True
        self.circle=False
        self.c.configure(cursor="crosshair")
        self.active_button = self.pen_button
        self.activate_button(self.pen_button)
        #self.c.bind('<B1-Motion>', self.paint)
        #self.c.bind('<ButtonRelease-1>', self.reset)
        self.c.bind("<Motion>", self.canxy)





    #Accion del boton Linea
    def do_something(self):
        self.activate_button(self.algo_button)
        self.lapiz_on=False
        self.line=True
        self.c.configure(cursor="cross")
      


    #Accion de la funcion linea, lee la posicion del click y crea la linea si es el segundo click
    

    def onClickPress(self, event):
        self.x, self.y = event.x, event.y

    def onMotionLine(self, event):
        x1,y1 =self.x, self.y
        x2, y2 = event.x, event.y
        paper=copy.copy(self.paper)
        if self.line_DDA:
            self.lineImg=self.drawDDA(x1,y1,x2,y2, paper)
        else:
            self.lineImg=self.drawBresenham(x1,y1,x2,y2,paper)
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=self.lineImg)

    def onReleaseLine(self, event):
        x1,y1 =self.x, self.y
        x2, y2 = event.x, event.y
        if self.line_DDA:
            self.lineImg=self.drawDDA(x1,y1,x2,y2, self.paper)
        else:
            self.lineImg=self.drawBresenham(x1,y1,x2,y2,self.paper)
       
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=self.lineImg)


    #Corre Algoritmo DDA
    def dda(self):
        self.line_DDA=True
        self.activate_button(self.brush_button)
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onMotionLine)
        self.c.bind("<ButtonRelease-1>", self.onReleaseLine)
        #self.lapiz_on=False
        self.label1.config(text="DDA")
  
 
    #Algoritmo Bresenham
    def Bresenham(self):
        #self.activate_button(self.brush_button)
        #self.res=self.t.get()
        self.line_DDA=False
        self.label1.config(text="Bresenham")
        self.activate_button(self.Bresenham_button)
        self.c.bind("<ButtonPress-1>", self.onClickPress)
        self.c.bind("<B1-Motion>", self.onMotionLine)
        self.c.bind("<ButtonRelease-1>", self.onReleaseLine)
    

    #Funcion Circulo
    def circulo(self):
        cx= int(self.cx.get())
        cy= int(self.cy.get())
        self.circle=True
        self.line_DDA=False
        self.rad=float(self.cir.get())
        self.circleImg=self.drawCircleDDA(self.rad, cx, cy,self.paper)
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=self.circleImg)

    #Funcion elipse
    def elipse(self):
        cx= int(self.cx.get())
        cy= int(self.cy.get())
        self.circle=True
        self.line_DDA=False
        self.radX=float(self.cir.get())
        self.radY=float(self.ry.get())
        self.elipseImg=self.drawElipse(cx,cy,self.radX, self.radY, self.colors, self.paper)
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=self.elipseImg)
    #Funcion Triangulo
    def triangulo(self):
        self.activate_button(self.triang_button)
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
        x1,y1=int(self.x), int(self.y)
        x2,y2=x1, int(event.y)
        x3=int(x2+x1/2)
        y3=y2 
        paper=copy.copy(self.paper)
        self.drawTriangulo(x1,y1,x2,y2,x3,y3,paper)
    
    def onTrianguloRelease(self, event):
        x1,y1=int(self.x), int(self.y)
        x2,y2=x1, int(event.y)
        x3=int(x2+x1/2)
        y3=y2 
        self.drawTriangulo(x1,y1,x2,y2,x3,y3,self.paper)
        

    def box(self):
        self.activate_button(self.Box_button)
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
        self.c.bind("<ButtonPress-1>", self.fillColors)
        self.c.bind("<ButtonRelease-1>", self.release)

    def release(self, event):
        pass    

    def transitionTool(self):
        self.activate_button(self.transi_button)
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
        self.c.bind("<ButtonPress-1>", self.on_button_press)
        self.c.bind("<B1-Motion>", self.onTransitionMotion)
        self.c.bind("<ButtonRelease-1>", self.onTransitionRelease)
        
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

    def moveTransition(self, pixelList, newPoint, bc, img):
        deltaX = newPoint[0] - pixelList[0][0][0]
        deltaY = newPoint[1] - pixelList[0][0][1]

        for i in range(0, len(pixelList) - 1):
            pixel = pixelList[i]
            img.putpixel((pixel[0][0] + deltaX, pixel[0][1] + deltaY), pixel[1])

        transitImg = ImageTk.PhotoImage(img)
        return transitImg

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
        self.color = askcolor(color=self.color)[1]

    #Activa Borrador
    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)


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

    def on_button_draw_pencil(self, event):
        previousPoint = (self.old_x, self.old_y)
        pointNow = (event.x, event.y)
        self.pencilImg = self.pencil(previousPoint, pointNow, self.color, self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.pencilImg)
        self.old_x = event.x
        self.old_y = event.y

    #Accion del boton Lapiz
    def use_pen(self):
        self.activate_button(self.pen_button)
        self.lapiz_on=True
        self.line=False
        self.c.configure(cursor="crosshair")
        self.c.bind("<ButtonPress-1>", self.on_button_press)
        self.c.bind("<B1-Motion>", self.on_button_draw_pencil)
        self.c.bind("<ButtonRelease-1>", self.on_button_draw_pencil)

    def on_button_press(self, event):
        self.old_x = event.x
        self.old_y = event.y

if __name__ == '__main__':
    Paint()
