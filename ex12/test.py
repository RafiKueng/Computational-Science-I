from Tkinter import *

jj = 0

def cng(w):
    global jj
    jj+=10
    w.coords(i,jj*10,jj*10,200,100)
    w.after(1000,cng,w)

master = Tk()

w = Canvas(master, width=800, height=600)
w.pack()

i=w.create_line(0, 0, 200, 100, fill="red")
w.create_line(0, 100, 200, 0, fill="red", dash=())

#w.create_rectangle(50, 25, 150, 75, fill="blue")


w.after_idle(cng,w)
    
    


mainloop()