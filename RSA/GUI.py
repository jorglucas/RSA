# -*- coding: utf-8 -*-

from tkinter import * #importa toda biblioteca do Tkinter

def feito():
    l3['text'] = i1.get()
    l3['fg'] = "green"
    i1.delete(0, END)

window_p = Tk() #Cria a janela principal

window_p.title("RSA Encrypt/Decrypt") #Titulo da janela
window_p.geometry("800x600+200+200") #Dimensão da janela e distancia da borda superior e lateral esquerda
window_p.wm_iconbitmap('icone.ico') #icone da janela

foto = PhotoImage(file = "image.png")
ima = Label(window_p, image = foto)

l1 = Label(window_p, text = "Digite seu texto abaixo",pady = 15)                        

i1 = Entry(window_p)

b1 = Button(window_p, text = "Criptografar", command = feito) 

l3 = Label(window_p)

ima.pack()
l1.pack()
i1.pack()
b1.pack()
l3.pack()

check1 = Checkbutton(window_p, text = "Teste", activeforeground = "green")
check1.pack()


window_p.mainloop()
