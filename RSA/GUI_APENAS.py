## IMPORTAR BIBLIOTECAS E INSTANCIAS DO TKINTER
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext


##FUNÇOES DOS BOTOES E ABAS
def msg_decripted():
    lb4.forget()
    e3.forget()
    e4.forget()
    e5.forget()
    btn7.forget()
    lb6.pack(side = TOP, pady = 90, expand = 1)

def descriptografar():
    tab_control.select(dcript)
    btn1.forget()
    btn2.forget()
    e3.pack(side = TOP, expand = 1)
    e4.pack(side = TOP, expand = 1)
    e5.pack(side = TOP, expand = 1)

def criptografar():
    lb1.pack(side = TOP, expand = 1, pady = 40, fill = BOTH)
    frame_top_cript.forget() 
    frame_bottom_cript.forget() 
    lb3.pack(side = TOP, expand = 1, pady = 40, fill = BOTH)
    btn6.pack(side = BOTTOM)

def gerar_chave():
    frame_tleft_key.forget()
    frame_tright_key.forget()
    btn1.forget()
    btn2.forget()
    lb1.pack(side = TOP, expand = 1, pady = 40, fill = BOTH)
    btn3.pack(side = BOTTOM, expand = 1, pady = 30)

def inserir():
    frame_tleft_key.forget()
    frame_tright_key.forget()
    btn1.forget()
    btn2.forget()
    lb5.pack(side = TOP)
    e1.pack(side = TOP, expand = 1, pady = 10)
    e2.pack(side = TOP, expand = 1, pady = 10)
    e6.pack(side = TOP, expand = 1, pady = 10)
    btn4.pack(side = BOTTOM)

def prosseguir():
    e1.forget()
    e2.forget()
    e6.forget()
    lb5.forget()
    btn4.forget()
    btn3.pack(side = BOTTOM, expand = 1, pady = 30)
    btn5.pack(side=TOP, padx=10, pady = 20, expand=1)
    lb1.pack(side = TOP, expand = 1)
    tab_control.select(cript)
    scroll['state'] = "normal"
    scroll.focus()


##CONFIGURAÇÕES DO FORMATO A JANELA
window = Tk()
window.geometry("300x300+500+200")
window.resizable(0, 0)
window.title("RSA")
window.iconbitmap("icon.ico")


##CRIAÇÃO E CONFIGURAÇÃO DAS ABAS
tab_control = ttk.Notebook(window)
key = ttk.Frame(tab_control)
cript = ttk.Frame(tab_control)
dcript = ttk.Frame(tab_control)
tab_control.add(key,text="Gerar chaves")
tab_control.add(cript,text="Criptografar")
tab_control.add(dcript,text="Descriptografar")
tab_control.pack(expand=1, fill= BOTH)


#FRAMES E WIDGETS DA ABA DE GERAR CHAVE
frame_top_key = Frame(key)
frame_bottom_key = Frame(key)

frame_tleft_key = Frame(frame_top_key)
frame_tright_key = Frame(frame_top_key)

btn1 = Button(frame_tleft_key, text="Gerar Chave", command = gerar_chave)
btn2 = Button(frame_tright_key, text="Inserir Chave", command = inserir)
lb1 = Label(frame_top_key, text = "Suas chaves foram validadas!\n\nO arquivo key.txt foi criado no diretório onde\nestá esse executável. Prossiga com a criptografia\n da sua mensagem clicando abaixo.")
lb5 = Label(frame_top_key, text = "Digite os valores de P, Q e de um co-primo\na esses dois números, nessa ordem")
e1 = Entry(frame_top_key)
e2 = Entry(frame_top_key)
e6 = Entry(frame_top_key)
btn3 = Button(frame_top_key, text="Prosseguir", command = prosseguir)
btn4 = Button(frame_top_key, text="Validar", command = prosseguir)

frame_top_key.pack(side=TOP, expand=1)
frame_tleft_key.pack(side=LEFT, expand=1)
frame_tright_key.pack(side=RIGHT, expand=1)

btn1.pack(side=LEFT, padx=10, pady = 3, expand=1)
btn2.pack(side=RIGHT, padx=10, pady = 3, expand=1)


#FRAMES E WIDGETS DA ABA DE CRIPTOGRAFAR
frame_cript = Frame(cript)
frame_top_cript = Frame(frame_cript)
frame_bottom_cript = Frame(frame_cript)
lb2 = Label(frame_top_cript, text = "Digite sua mensagem abaixo para ser criptografada")
scroll = scrolledtext.ScrolledText(frame_top_cript,width=40,height=8, state = "disable")
btn5 = Button(frame_bottom_cript, text="Criptografar", command = criptografar)
frame_cript.pack(side = TOP, expand = 1)
frame_top_cript.pack(side = TOP, expand = 1)
frame_bottom_cript.pack(side = BOTTOM, expand = 1)
lb2.pack(side = TOP, expand = 1, pady = 10)
scroll.pack(side = TOP, padx=10, pady = 10, expand = 1)
lb3 = Label(frame_cript, text = "Sua mensagem já foi criptografada e o\narquivo msg.txt foi gerado no diretório onde\nestá este executável")
btn6 = Button(frame_cript, text="Descriptografar", command = descriptografar)


#FRAMES E WIDGETS DA ABA DE DESCRIPTOGRAFAR
frame_dcript = Frame(dcript)
e3 = Entry(frame_dcript)
e4 = Entry(frame_dcript)
e5 = Entry(frame_dcript)
lb4 = Label(frame_dcript, text = "Digite os valores de E, P e Q nessa ordem\npara descriptografar seu arquivo")
lb4.pack(side = TOP, pady = 5)
e3.pack(side = TOP, pady = 20)
e4.pack(side = TOP, pady = 20)
e5.pack(side = TOP, pady = 20)
lb6 = Label(frame_dcript, text = "Seu arquivo foi descriptografado e está no diretório\ndeste executável como msg_descripted.txt")
btn7 = Button(frame_dcript, text="Validar", command = msg_decripted)
btn7.pack(side = BOTTOM, pady = 10)
frame_dcript.pack()


##LOOP DA JANELA PRINCIPAL
window.mainloop()
