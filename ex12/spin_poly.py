from Tkinter import *
from numpy import *

class Polyeder(object):
    def __init__(self):
        pass
    def update(self, dt):
        pass
    def draw(self):
        pass
        
class Cube(Polyeder):
    def __init__(self):
        pass
    def update(self, dt):
        pass
    def draw(self):
        pass


class MyEngine:
    def __init__(self, parent):
        self.myParent = parent

        self.objects = []
        
        self.canvas = Canvas(parent, width = 800, height = 600)
        self.canvas.after(2000, self.draw, [0]) 
        self.canvas.pack()
       
        self.myContainer1 = Frame(parent)
        self.myContainer1.pack()

        self.button1 = Button(self.myContainer1, command=self.button1Click)
        self.button1.configure(text="OK", background= "green")
        self.button1.pack(side=LEFT)
        self.button1.focus_force()

        self.button2 = Button(self.myContainer1, command=self.button2Click)
        self.button2.configure(text="Cancel", background="red")
        self.button2.pack(side=RIGHT)
        
    def addObject(self, obj):
        self.objects.append(obj)

    def draw(self, args):
        dt = 10 # calc real delta t
        for obj in self.objects:
            obj.update(dt)
            obj.draw()
        
        print "IDLE", args[0]
        self.canvas.after(10,self.draw, [args[0]+1])
        
    def button1Click(self):  ### (2)
        print "button1Click event handler"
        if self.button1["background"] == "green":
            self.button1["background"] = "yellow"
        else:
            self.button1["background"] = "green"
        self.canvas.after(2000)

    def button2Click(self): ### (2)
        print "button2Click event handler"
        self.myParent.destroy()



root = Tk()
myapp = MyEngine(root)

poly = Cube()

myapp.addObject(poly)

root.mainloop()

'''
class engine():




window = Tk()
canvas = Canvas(window, width = 800, height = 600)
canvas.pack()

'''