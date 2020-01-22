# -*- coding: utf-8 -*-

#importa toda biblioteca do Tkinter
from tkinter import *


#função pra capturar o texto digitado
def feito():                       
    l3['text'] = i1.get()           #método para pegar o texto
    l3['fg'] = "green"              #cor do texto
    i1.delete(0, END)               #deletar o texto da entrada de texto
    
    
#Cria a janela principal
window_p = Tk()             

# Titulo da janela
window_p.title("RSA Encrypt/Decrypt")

# Dimensão da janela e distancia da borda superior e lateral esquerda
window_p.geometry("800x600+200+200")

# Icone da janela
window_p.wm_iconbitmap('icon.ico')

# "Variável" que recebe o método PhotoImage e salva o arquivo dentro de si
foto = PhotoImage(file = "image.png") 

# Label que recebe a imagem da "variável" foto
imag = Label(window_p, image = foto) 

# Label de texto   
l1 = Label(window_p, text = "Digite seu texto abaixo",pady = 15)             

# Entrada de texto
i1 = Entry(window_p) 

# Botão Criptografar
b1 = Button(window_p, text = "Criptografar", command = feito) 

# Label que mostra qual texto foi digitado em i1
l3 = Label(window_p) 

# CheckButton só de teste
check1 = Checkbutton(window_p, text = "Teste", activeforeground = "green") 

# Empacotamento dos widgets segundo a oredem que aparecem
imag.pack() 
l1.pack()
i1.pack()
b1.pack()
l3.pack()
check1.pack()


#Metodo para exibir a janela e todos widgets
window_p.mainloop()
