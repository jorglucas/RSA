from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from random import randint

window = Tk()
window.geometry("300x300+500+200")
window.resizable(0, 0)
window.title("RSA")
window.iconbitmap("icon.ico")

num1 = randint(28, 999999)
num2 = randint(28, 999999)

def cripto():
    btn3.forget()
    scroll['state'] = "disable"
    lb2.pack(side = BOTTOM)

def chaves():
    a = e1.get()
    b = e2.get()
    e1.forget()
    e2.forget()
    lb2.forget()
    scroll['state'] = "normal"
    btn4.forget()
    btn3.pack(side=BOTTOM, padx=5, expand=1)

def gerar():
    p.pack(pady = 15)
    q.pack(pady = 15)
    scroll.focus()
    lb2.forget()
    e1.forget()
    e2.forget()
    btn4.forget()
    btn3.pack(side=BOTTOM, padx=5, expand=1)
    p['text'] = "P", num1
    q['text'] = "Q", num2
    scroll['state'] = "normal"

def inserir():
    lb2.forget()
    p.forget()
    q.forget()
    e1.pack()
    e2.pack()
    btn3.forget()
    scroll['state'] = "disable"
    btn4.pack(pady = 5)


tab_control = ttk.Notebook(window)
cript = ttk.Frame(tab_control)
dcript = ttk.Frame(tab_control)

tab_control.add(cript,text="Criptografar")

tab_control.add(dcript,text="Descriptografar")
tab_control.pack(expand=1, fill= BOTH)

frametop = Frame(cript)
framebottom = Frame(cript)
frameleft = Frame(frametop)
frameright = Frame(frametop)

scroll = scrolledtext.ScrolledText(cript,width=40,height=8, state = "disable")
btn1 = Button(frameleft, text="Gerar Chave Pública", command = gerar)
btn2 = Button(frameright, text="Inserir Chave Manual", command = inserir)
btn3 = Button(framebottom, text="Criptografar Mensagem", command = cripto)
btn4 = Button(cript, text = "Verificar", command = chaves)
lb2 = Label(framebottom, text = "Mensagem Criptografada")

frametop.pack(side=TOP, expand=1)
framebottom.pack(side=BOTTOM, expand=1)
frameleft.pack(side=LEFT, expand=1)
frameright.pack(side=RIGHT, expand=1)

btn1.pack(side=TOP, padx=5, pady = 3, expand=1)
btn2.pack(side=TOP, padx=5, pady = 3, expand=1)
scroll.pack(side=BOTTOM, padx=5, expand=1)

p = Label(frameleft)
q = Label(frameright)
e1 = Entry(cript)
e2 = Entry(cript)

window.mainloop()
