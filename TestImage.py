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
    points=[]
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
        #Boton Borrar entrada DDA
        self.clearDDA_button = Button(self.root, text='Borrar', command=self.borrarDDA)
        self.clearDDA_button.grid(row=4, column=0)

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

        #Resto de botones que vinieron con el codigo
        self.color_button = Button(self.root, text='color', command=self.choose_color)
        self.color_button.grid(row=0, column=20)

        self.eraser_button = Button(self.root, text='eraser', command=self.use_eraser)
        self.eraser_button.grid(row=0, column=22)

        self.choose_size_button = Scale(self.root, from_=1, to=100, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=24)


        #El Canvas
        self.c = Canvas(self.root, bg='white', width=self.paperWidht, height=self.paperHeight)
        self.c.grid(row=8, columnspan=24)


        #Entrada de Datos DDA y Bresenham
        self.t= Entry(self.root)
        self.t.grid(row=0, column=1)

        self.t2= Entry(self.root)
        self.t2.grid(row=1, column=1)

        self.t3= Entry(self.root)
        self.t3.grid(row=2, column=1)


        self.t4= Entry(self.root)
        self.t4.grid(row=3, column=1)

        #Entrada de Datos Circulo
        self.cir=Entry(self.root)
        self.cir.grid(row=1, column=8)

        self.cx=Entry(self.root)
        self.cx.grid(row=2, column=8)

        self.cy=Entry(self.root)
        self.cy.grid(row=3, column=8)

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

        #Los Labels DDA
        Label(self.root, text="X").grid(row=0, column=0)
        Label(self.root, text="Y").grid(row=1, column=0)
        Label(self.root, text="Xf").grid(row=2, column=0)
        Label(self.root, text="Yf").grid(row=3, column=0)

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
        self.c.bind("<Button-1>", self.point)


    #Accion de la funcion linea, lee la posicion del click y crea la linea si es el segundo click
    def point(self, event):
        if self.line:
            self.points.append(event.x)
            self.points.append(event.y)
            self.clicks+=1
            self.c.create_line(event.x, event.y, event.x, event.y, width=2, fill=self.color,
                                   capstyle=ROUND, smooth=TRUE, splinesteps=36)
            if self.clicks>=2:

                self.clicks=0
                pointx=self.points[0]
                pointy=self.points[1]
                pointxf=self.points[2]
                pointyf=self.points[3]
                if self.line_DDA:
                    papel=copy.copy(self.paper)
                    self.lineImg=self.drawDDA(pointx, pointy, pointxf, pointyf, self.paper)
                    self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)

                else:
                    self.lineImg=self.drawBresenham(pointx, pointy, pointxf, pointyf, self.paper)
                    self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)

                if self.circle:
                    dx=self.points[2]-self.points[0]
                    dy=self.points[3]-self.points[1]
                    leng=math.sqrt(dx**2+dy**2)
                    self.circleImg=self.drawCircleDDA(leng, self.points[0], self.points[1], self.paper)
                    self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=self.circleImg)
                self.points.clear()

    def onClickLine(self):
        pass

    def onMotionLine(self):
        pass

    def onReleaseLine(self):
        pass


    #Corre Algoritmo DDA
    def dda(self):
        #self.activate_button(self.brush_button)
        #self.lapiz_on=False
        self.label1.config(text="DDA")
        self.line_DDA=True
        if (not self.t.index(END)==0) and (not self.t2.index(END)==0) and not self.t3.index(END)==0 and not self.t4.index(END)==0:
            #Adquiere x inicial
            self.x=int(self.t.get())

            #Adquiere y inicial
            self.y=int(self.t2.get())

            #Adquiere x final
            self.xf=int(self.t3.get())

            #Adquiere y final
            self.yf=int(self.t4.get())

            #Dibuja la linea
            papel=copy.copy(self.paper)
            self.lineImg=self.drawDDA(self.x,self.y,self.xf,self.yf,self.paper)
            self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)



    #Para borrar los campos de entrada
    def borrarDDA(self):
        self.t.delete(0, END)
        self.t2.delete(0, END)
        self.t3.delete(0, END)
        self.t4.delete(0, END)


    #Algoritmo Bresenham
    def Bresenham(self):
        #self.activate_button(self.brush_button)
        #self.res=self.t.get()
        self.line_DDA=False
        self.label1.config(text="Bresenham")

        if (not self.t.index(END)==0) and (not self.t2.index(END)==0) and not self.t3.index(END)==0 and not self.t4.index(END)==0:

            self.x=int(self.t.get())


            self.y=int(self.t2.get())


            self.xf=int(self.t3.get())


            self.yf=int(self.t4.get())


            self.lineImg=self.drawBresenham(self.x,self.y,self.xf,self.yf, self.paper)
            self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)

    #Funcion Circulo
    def circulo(self):
        cx= int(self.cx.get())
        cy= int(self.cy.get())
        self.circle=True
        self.line_DDA=False
        self.rad=float(self.cir.get())
        self.circleImg=self.drawCircleDDA(self.rad, cx, cy,self.paper)
        self.c.create_image(self.paperWidht/2, self.paperHeight/2, image=self.circleImg)

    #Funcion Triangulo
    def triangulo(self):
        x1=int(self.tr.get())
        y1=int(self.tr2.get())
        x2=int(self.tr3.get())
        y2=int(self.tr4.get())
        x3=int(self.tr5.get())
        y3=int(self.tr6.get())
        self.lineImg=self.drawDDA(x1,y1,x2,y2,self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)
        self.lineImg2=self.drawDDA(x2,y2,x3,y3, self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg2)
        self.lineImg3=self.drawDDA(x1,y1,x3,y3, self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg3)

    #Funcion Box
    def box(self):
        x1=int(self.t.get())

        y1=int(self.t2.get())

        x2=int(self.t3.get())

        y2=int(self.t4.get())

        self.lineImg=self.drawDDA(x1,y1,x1,y2, self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)
        self.lineImg=self.drawDDA(x1,y1,x2,y1, self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)
        self.lineImg=self.drawDDA(x1,y2,x2,y2, self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)
        self.lineImg=self.drawDDA(x2,y1,x2,y2, self.paper)
        self.c.create_image(self.paperWidht / 2, self.paperHeight / 2, image=self.lineImg)

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
        lineImg = ImageTk.PhotoImage(img)
        return lineImg
        #print("fin")
    
        def drawEclipse(centerPoint, x, y, color, img):
            pass
            
        def eclipseMidPoint(centerPoint, rx, ry, color, img):
            rxSq = rx ** 2
            rySq = ry ** 2
            x = 0
            y = ry
            px = 0
            py = 2 * rxSq * y
            drawEclipse(centerPoint, x, y, color, img)
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
                drawEclipse(centerPoint, x, y, color, img)

            p = rySq*(x+0.5)*(x+0.5) + rxSq*(y-1)*(y-1) - rxSq*rySq
            while y > 0:
                y = y - 1
                py = py - 2 * rxSq;
                if p > 0:
                    p = p + rxSq - py;
                else:
                    x = x + 1
                    px = px + 2 * rySq;
                    p = p + rxSq - py + px;
                drawEclipse(centerPoint, x, y, color, img);

            eclipseImg = ImageTk.PhotoImage(img)
            return eclipseImg
    
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
