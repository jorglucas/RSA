#-*- coding: utf-8 -*-
##BIBLIOTECAS USADAS PARA O CÓDIGO RSA
import time
import secrets
import math
import random
from random import randint

##BIBLIOTECAS USADAS PARA A INTERFACE GRÁFICA
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

#dicionarios que ajudam na criptografia(dicionario1) e descriptografia(dicionario2)
dicionario1 = {"a" : 2, "b" : 3, "c" : 4, "d" : 5, "e" : 6, "f" : 7, "g" : 8, "h" : 9, "i" : 10, "j" : 11,"k" : 12,
  "l" : 13, "m": 14, "n":15, "o" : 16, "p" : 17, "q": 18, "r" : 19, "s":20, "t":21, "u":22, "v":23, "w":24,"x":25,
  "y":26, "z":27, " ":28}

dicionario2 = {2 : "a", 3 : "b", 4 : "c", 5 : "d", 6 : "e" , 7 : "f" , 8 : "g", 9 : "h", 10 : "i", 11: "j" , 12 : "k" ,
  13 : "l", 14 : "m", 15 : "n", 16 : "o", 17 : "p", 18 : "q", 19 : "r", 20 : "s", 21: "t", 22 : "u", 23: "v", 24 : "w",
  25 : "x", 26 : "y", 27 : "z", 28 : " "}

##funcoes matematicas, pelas quais o usuario nao interage
#funcoes usadas pelas funcoes decript() e encript():
def invert(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = invert(b % a, a)
        return (g, x - (b // a) * y, y)

def inversom_m(a, m): #funcao que retorna o inverso modular, ou inverso mutiplicativo
    g, x, y = invert(a, m)
    if g != 1:
        raise Exception('Nao existe inverso modular')
    else:
        return x % m

def exp_mod_rap(list_int_pow, d, mod, exp, r): #funcao de exponenciacao modular rapida
    if list_int_pow[-1] >= exp: #se o ultimo valor da lista de espoentes for maior ou igual ao expoente atual a funcao executa
        
        if exp == 1: #checagem para definir o r na primeira execucao dessa funcao
            r = d % mod
            if exp in list_int_pow: #checagem para ver se o expoente esta na decomposicao do numero binario
                return r * exp_mod_rap(list_int_pow, d, mod, (exp*2), r) #retornando a mutiplicacao dos fators

        else: #atribuicao feita a r a partir do segundo caso em diante
            r = (r*r) % mod 
            if exp in list_int_pow: #checagem para ver se o expoente esta na decomposicao do numero binario
                return r * exp_mod_rap( list_int_pow, d, mod, (exp*2), r) #retornando ja a multiplicacao dos fatores

        return exp_mod_rap(list_int_pow, d, mod, (exp*2), r) #caso nao caia em nenhuma das checagens acima a funcao nao multiplica
    
    else:
        return 1

def generate_list_int(convert, list_int_pow): #gerador de uma lista que contem a decomposicao do numero binario em potencias de base 2 
    j = 0 #posicao na string
    
    for i in convert:
        if i == "0": #se o algarismo binario da posicao for 0, ele simplesmente parte para o proximo digito
            j+=1 #incremento do expoente ao qual a base 2 será elevada
        
        else:
            list_int_pow.append(pow(2, j)) #caso o digito daquela posicao seja 1, ele adiciona a lista uma potencia de base 2 cujo expoente e a posicao do digito na string(no caso o j)
            j+=1 #incremento do expoente ao qual a base 2 será elevada

def int_bin(div, convert): #funcao que converte um valor inteiro para binario, pega int e retorna string

    if div != 1:
        convert = convert + str(div%2)
        return int_bin(div//2, convert)

    else:
        convert = convert + str(div)
        return convert #note que retornando assim o numero binario esta invertido, contudo essa invercao e conveniente a funcao exp_mod_rap

#funcoes usadas pela funcao generate_key()
def euclides(num1, num2): #algoritmo de euclides utilizado para saber o mdc

        resto = num1 % num2

        if resto == 0: #condicao de retorno do mdc
            return num2 

        return euclides(num2, resto)

def test_prime(n): #funcao que checa se um numero e primo

    s = int(math.sqrt(n)) + 3 #segundo a matematica, na busca por um numero primo, so precisamos tentar encontrar um divisor ate a raiz quadrada do numero em questao

    if n % 2 == 0: #se o numero for par ja retorna que ele nao e primo
        return False #essa checagem e necessaria pois no ciclo abaixo o divisor incrementa de 2 em 2, se não houvessee essa checagem bugaria

    for x in range(3, s, 2): #ciclo que incrementa em 2 o divisor (inicializado em 3) ate ele atingir o limite s 
        if n % x == 0: #caso seja encontrado um divisor antes do s o numero nao e primo
            return False

    return True #caso nao tenha sido encontrado um divisor nas condicoes acima, o numero e primo

def gen_prime(): #funcao que gera um numero primo aleatorio entre 10000 e 1000000

    n = secrets.randbits(32) #gerando numero aleatorio dentro do intervalo especificado

    while test_prime(n) == False: #esse ciclo serve para impedir que um numero aleatorio nao primo seja retornado
        n = secrets.randbits(32) #atribuindo um novo numero aleatorio a n ate que n seja primo

    return n

def phi(p, q): #funcao totiente
    return (p-1)*(q-1)

def co_primos(x): #funcao que retorna um numero co-primo do numero passado
    y = gen_prime()

    while euclides(x, y) !=1: #ciclo para garantir a condicao de coprimos(numeros que o mdc entre eles e 1)
        y = gen_prime() #enquanto o y nao atender essa condicao ele vai sendo gerado novamente

    return y

#funcoes que irao interagir com o usuario:
#funcao que gera a chave publica
def generate_key():
    p = gen_prime()
    q = gen_prime()
    while p == q:
        q = gen_prime()
    n = p*q
    tot_n = phi(p, q)
    e = co_primos(tot_n)

    #RETIRA TODOS WIDGETS DA ABA GERAR CHAVES
    frame_tleft_key.forget()
    frame_tright_key.forget()
    btn1.forget()
    btn2.forget()
    #CRIA OS ARQUIVOS PUBLIC_KEY.TXT E PRIVATE_KEY.TXT
    create_archive(n, e, p, q)

def create_archive(n, e, p, q):
    #RETIRA TODOS WIDGETS DA TELA DE INSERIR CHAVES NA ABA GERAR CHAVES
    lb5.forget()
    e1.forget()
    e2.forget()
    e6.forget()
    btn4.forget()
    #EMPACOTA A LABEL INFORMATIVA E O BOTÃO PROSSEGUIR
    lb1.pack(side = TOP, expand = 1, pady = 40, fill = BOTH)
    btn3.pack(side = BOTTOM, expand = 1, pady = 30)
    
    chave_publica = ("Valores da chave publica:\nn = %d e = %d\n" %(n,e))
    chave_privada = ("Valores da chave privada:\ne = %d n = %d p = %d q = %d\n" %(e, n, p, q))
    key = open("public_key.txt", "w")
    key_p = open("private_key.txt", "w")
    key_p.write(chave_privada)
    key.write(chave_publica)
    key_p.close()
    key.close()

## FUNÇÃO DO BOTÃO VALIDAR
def validate_prime():
  #PEGA OS VALORES INSERIDOS PELOS USUÁRIO E CONVETE PARA INTEIRO
    p = int(e1.get())    
    q = int(e2.get())
    e = int(e6.get())
    
    #TESTA DE OS VALORES DE 'P' E 'Q' SÃO PRIMOS
    if(test_prime(p) == False):
        messagebox.showerror("Erro", "P não é primo tente outro valor")
        insert_key()

    elif(test_prime(q) == False):
        messagebox.showerror("Erro", "Q não é primo tente outro valor")
        insert_key()
        
    elif p == q:
        messagebox.showerror("Erro", "P e Q possuem o mesmo valor")   
        insert_key()

    n = p*q
    tot_n = phi(p, q)
    
    #TESTA SE O VALOR DE N É UM CO-PRIMO DE 'P' E 'Q'
    if euclides(tot_n, e) !=1:
        messagebox.showerror("Erro", "Esse número não é um co-primo")
        insert_key()
        
    #SE TUDO ESTIVER CORRETO, GERA O ARQUIVO PUBLIC_KEY.TXT E PRIVATE_KEY.TXT
    if(test_prime(p) != False and test_prime(q) != False and euclides(tot_n, e) == 1):
        create_archive(n, e, p, q)

## FUNÇÃO DO BOTÃO INSERIR CHAVES
def insert_key():
    # RETIRA OS BOTÕES DA TELA DE ESCOLHA NA ABA GERAR CHAVES
    frame_tleft_key.forget()
    frame_tright_key.forget()
    
    lb5.pack(side = TOP)                            #EMPACOTAMENTO DA LABEL DE INSTRUÇÃO
    e1.pack(side = TOP, expand = 1, pady = 10)      #EMPACOTAMENTO DA ENTRADE DE 'P'
    e2.pack(side = TOP, expand = 1, pady = 10)      #EMPACOTAMENTO DA ENTRADE DE 'Q'
    e6.pack(side = TOP, expand = 1, pady = 10)      #EMPACOTAMENTO DA ENTRADE DE 'E'
    e1.focus()                                      #DÁ FOCO NA ENTRADA DE 'P'
    btn4.pack(side = BOTTOM, pady = 10)             #EMPACOTAMENTO DO BOTÃO VALIDAR

def decript():
    #entradas do usuario
    e = int(e3.get())                #PEGANDO O VALOR DE 'E' E CONVERTENDO PARA INTEIRO
    p = int(e4.get())                #PEGANDO O VALOR DE 'P' E CONVERTENDO PARA INTEIRO
    q = int(e5.get())                #PEGANDO O VALOR DE 'Q' E CONVERTENDO PARA INTEIRO

    #calculo dos valores necessarios
    n = p * q
    tot_n = ((p-1) * (q-1))
    d = inversom_m(e, tot_n) #inverso multiplicativo de e, fundamental para a descriptografia

    #manipulação do arquivo de entrada
    arquivo_cript = open("encripted.txt", "r") #abrindo arquivo criptografado indicado pelo usuario
    mensagem = arquivo_cript.read() #atribuindo conteudo do arquivo criptografado a uma string

    #transformando o conteudo do arquivo em uma lista contendo o numero que representa cada letra criptografada
    lista = mensagem.split(" ")
    
    arquivo_cript.close() #fechando arquivo de entrada

    #processo de descriptografia
    desc = "" #string vazia que v1ai armazenar a mensagem descriptografada

    for item in lista:
        #objetos auxiliares
        list_int_pow = [] #lista auxiliar que ira guardar dados para o funcionamento da funcao exponencial modular rapida
        if item == '': #condicao pra nao bugar no ultimo item da lista que sempre vai ser vazio 
            break
        x = int(item) #atribui a x o inteiro da lista que vai ser descriptografado em um caracter
        #r = (x**d) % n
        convert = int_bin(d, "") #convertendo expoente d em binario para poder iniciar a exponenciação
        generate_list_int(convert, list_int_pow) #armazenando em uma lista a decomposição do expoente em potencias de base 2
        y = exp_mod_rap(list_int_pow, x, n, 1, 0) #executando a exponenciacao modular rapida com o expoente d
        
        desc = desc + dicionario2[y%n] #concatenando a mensagem com o caracter que acabou de ser descriptografada

    #manipulacao do arquivo de saida
    arquivo_descript = open("decripted.txt", "w")#criando arquivo .txt com o nome provido pelo usuario
    arquivo_descript.write(desc)#escrevendo mensagem descriptografada no arquivo
    arquivo_descript.close() #fechando o arquivo

    #RETIRA TODOS WIDGETS DA ABA DESCRIPTOGRAFAR 
    lb4.forget()
    e3.forget()
    e4.forget()
    e5.forget()
    btn7.forget()
    #EMPACOTA A LABEL INFORMATIVA
    lb6.pack(side = TOP, pady = 70)


def encript():
    #entradas providas pelo usuario
    n = int(e7.get())                       #PEGANDO O VALOR DE 'N' DA ENTRADA E CONVERTENDO PARA INTEIRO
    e = int(e8.get())                       #PEGANDO O VALOR DE 'E' DA ENTRADA E CONVERTENDO PARA INTEIRO
    mensagem  = scroll.get('1.0', END)      #CAPTURANDO O TEXTO DIGITADO NA SCROLLEDTEXT
    mensagem = mensagem.lower()
    
    i = 0
    error = 0
    criptografado = ""
    while i < int(len(mensagem) - 1):
        #objetos auxiliares
        list_int_pow = [] #lista auxiliar que vai guardar dados para o funcionamento da funcao exponencial modular rapida  
        #x = dicionario1[mensagem[i]]#valor de determinado caracter atribuido de acordo com o dicionario
        try :
            x = dicionario1[mensagem[i]]
        except :
            error = -1
            break
        x = dicionario1[mensagem[i]]#valor de determinado caracter atribuido de acordo com o dicionario
        convert = int_bin(e, "") #convertendo o valor de e (o expoente da potenciacao) em binario
        generate_list_int(convert, list_int_pow) #armazenando em "list_int pow" os valores na base 2  que decompoem o valor e

        y = exp_mod_rap( list_int_pow, x, n, 1, 0) #exponenciacao modular rapida para criptografar a mensagem
            
        criptografado = criptografado + str(y%n) +" "#gerando string que contem a mensagem criptografada
        i+=1

    #manipulando arquivo de saida
    if error == -1:
        messagebox.showerror("Erro", "Caractere inválido.\nNão use acentos nem pontuações.") #BOX DE ERRO PARA CARACTERES INVÁLIDOS
    else:
        arquivo = open("encripted.txt", "w") #gerando arquivo txt que guardará o texto descriptografado
        arquivo.write(criptografado) #escrevendo a mensagem criptografada no arquivo
        
        #RETIRA TODOS WIDGETS DA ABA CRIPTOGRAFAR 
        lb2.forget()
        e7.forget()
        e8.forget()
        scroll.forget()
        btn5.forget()
        #EMPACOTA LABEL INFORMATIVA 
        lb3.pack(side = TOP, pady = 50)

###---------- COMEÇO DA GUI ----------###
# FUNÇÃO QUE LEVA PARA A ABA CRIPTOGRAFAR
def prosseguir():
    e1.forget()                                           #FORGET() TIRA DA TELA A ENTRADA DO VALOR DE 'P'
    e2.forget()                                           #FORGET() TIRA DA TELA A ENTRADA DO VALOR DE 'Q'
    e6.forget()                                           #FORGET() TIRA DA TELA A ENTRADA DO VALOR DE 'E'
    lb5.forget()                                          #FORGET() TIRA DA TELA A LABEL DE INSTRUÇÃO
    btn4.forget()                                         #FORGET() TIRA DA TELA O BOTÃO VALIDAR
    tab_control.select(cript)                             #REDIRECIONA PARA A ABA CRIPTOGRAFAR
    lb1.pack(side = TOP, expand = 1)                      #EMPACOTAMENTO DA LABEL INFORMATIVA
    btn3.pack(side = BOTTOM, expand = 1, pady = 30)       #EMPACOTAMENTO DO BOTÃO PROSSEGUIR
    e7.focus()                                            #FOCUS() JÁ DEIXA SELECIONADA A ENTRADA DO VALOR DE 'N'

## CONFIGURAÇÕES DO FORMATO A JANELA
window = Tk()                             #CRIAÇÃO DA JANELA PRINCIPAL
window.geometry("300x300+200+200")        #DIMENSIONAMENTO DA JANELA
window.resizable(0, 0)                    #BLOQUEIO DO REDIMENSIONAMENTO
window.title("RSA")                       #TÍTULO
window.iconbitmap("icon.ico")             #ÍCONE

## CRIAÇÃO E CONFIGURAÇÃO DAS ABAS
tab_control = ttk.Notebook(window)                  #CRIAÇÃO DA INSTÂNCIA DE ABAS
key = ttk.Frame(tab_control)                        #FRAME GERAL DA ABA GERAR CHAVES
cript = ttk.Frame(tab_control)                      #FRAME GERAL DA ABA CRIPTOGRAFAR
dcript = ttk.Frame(tab_control)                     #FRAME GERAL DA ABA DESCRIPTOGRAFAR
tab_control.add(key,text="Gerar chaves")            #ADICIONANDO A ABA GERAR CHAVES
tab_control.add(cript,text="Criptografar")          #ADICIONANDO A ABA CRIPTOGRAFAR
tab_control.add(dcript,text="Descriptografar")      #ADICIONANDO A ABA DESCRIPTOGRAFAR
tab_control.pack(expand=1, fill= BOTH)              #EMPACOTAMENTO DAS ABAS

## ABA GERAR CHAVES
# FRAMES E WIDGETS
frame_top_key = Frame(key)                                                          #FRAME SUPERIOR DA ABA
frame_bottom_key = Frame(key)                                                       #FRAME INFERIOR DA ABA
frame_tleft_key = Frame(frame_top_key)                                              #FRAME ESQUERDO DA ABA
frame_tright_key = Frame(frame_top_key)                                             #FRAME DIREITO DA ABA
btn1 = Button(frame_tleft_key, text="Gerar Chaves", command = generate_key)         #BOTÃO GERAR CHAVES
btn2 = Button(frame_tright_key, text="Inserir Chaves", command = insert_key)        #BOTÃO INSERIR CHAVES
lb1 = Label(frame_top_key, text = "Suas chaves foram validadas!\n\nOs arquivos private_key.txt e public_key.txt\nforam criados no diretório onde está esse executável.\nProssiga com a criptografia da sua mensagem\nclicando abaixo.") #LABEL INFORMATIVA
lb5 = Label(frame_top_key, text = "Digite os valores de P, Q e de um co-primo\na esses dois números, nessa ordem.\n*P e Q devem ser diferentes*") #LABEL DE INSTRUÇÃO
e1 = Entry(frame_top_key)                                                   #ENTRADA DO VALOR DE 'P'
e2 = Entry(frame_top_key)                                                   #ENTRADA DO VALOR DE 'Q'
e6 = Entry(frame_top_key)                                                   #ENTRADA DO VALOR DE 'E'
btn3 = Button(frame_top_key, text="Prosseguir", command = prosseguir)       #BOTÃO PROSSEGUIR
btn4 = Button(frame_top_key, text="Validar", command = validate_prime)      #BOTÃO VALIDAR
frame_top_key.pack(side=TOP, expand=1)                                      #EMPACOTAMENTO DO FRAME SUPERIOR
frame_tleft_key.pack(side=LEFT, expand=1)                                   #EMPACOTAMENTO DO FRAME ESQUERDO
frame_tright_key.pack(side=RIGHT, expand=1)                                 #EMPACOTAMENTO DO FRAME DIREITO
btn1.pack(side=LEFT, padx=10, pady = 3, expand=1)                           #EMPACOTAMENTO DO BOTÃO GERAR CHAVES
btn2.pack(side=RIGHT, padx=10, pady = 3, expand=1)                          #EMPACOTAMENTO DO BOTÃO INSERIR CHAVES

## ABA CRIPTOGRAFAR
# FRAMES E WIDGETS
frame_top_cript = Frame(cript)                  #FRAME SUPERIOR DA ABA
frame_bottom_cript = Frame(cript)               #FRAME INFERIOR DA ABA
lb2 = Label(frame_top_cript, text = "Insira 'N, 'E' e sua mensagem para ser criptografada.\nObs.: Sem pontos nem acentos")  #LABEL DE INSTRUÇÃO
lb2.pack(side = TOP, expand = 1, pady = 10)     #EMPACOTAMENTO DA LABEL DE INSTRUÇÃO
e7 = Entry(frame_top_cript)                     #ENTRADA DO VALOR DE 'N'
e8 = Entry(frame_top_cript)                     #ENTRADA DO VALOR DE 'E'
e7.pack(side = TOP)                             #EMPACOTAMENTO DA ENTRADA DE 'N'
e8.pack(side = TOP)                             #EMPACOTAMENTO DA ENTRADA DE 'E'
scroll = scrolledtext.ScrolledText(frame_top_cript,width=40,height=8)           #WIDGET DA CAIXA DE TEXTO COM SCROLL
btn5 = Button(frame_bottom_cript, text="Criptografar", command = encript)       #BOTÃO CRIPTOGRAFAR
scroll.pack(side = BOTTOM, padx=10, pady = 7)                                   #EMPACOTAMENTO DA CAIXA E TEXTO
btn5.pack(side=BOTTOM, padx=10, pady = 2)                                       #EMPACOTAMENTO DO BOTÃO CRIPTOGRAFAR
frame_top_cript.pack(side = TOP, expand = 1)                                    #EMPACOTAMENTO DO FRAME SUPERIOR
frame_bottom_cript.pack(side = BOTTOM, expand = 1)                              #EMPACOTAMENTO DO FRAME INFERIOR
lb3 = Label(frame_top_cript, text = "Sua mensagem já foi criptografada e o\narquivo encripted.txt foi gerado no diretório onde\nestá este executável")  #LABEL INFORMATIVA

## ABA DESCRIPTOGRAFAR
# FRAMES E WIDGETS
frame_dcript = Frame(dcript)          #FRAME DA ABA
e3 = Entry(frame_dcript)              #ENTRADA DO VALOR DE 'E'
e4 = Entry(frame_dcript)              #ENTRADA DO VALOR DE 'P'
e5 = Entry(frame_dcript)              #ENTRADA DO VALOR DE 'Q'
lb4 = Label(frame_dcript, text = "Digite os valores de E, P e Q nessa ordem\npara descriptografar seu arquivo") #LABEL DE INSTRUÇÃO
lb4.pack(side = TOP, pady = 5)        #EMPACOTAMENTO DA LABEL DE INSTRUÇÃO
e3.pack(side = TOP, pady = 20)        #EMPACOTAMENTO DA ENTRADA DE 'E'
e4.pack(side = TOP, pady = 20)        #EMPACOTAMENTO DA ENTRADA DE 'P'
e5.pack(side = TOP, pady = 20)        #EMPACOTAMENTO DA ENTRADA DE 'Q'
lb6 = Label(frame_dcript, text = "Seu arquivo foi descriptografado e está no diretório\ndeste executável como decripted.txt") #LABEL INFORMATIVA DE QUE O ARQUIVO FOI GERADO
btn7 = Button(frame_dcript, text="Descriptografar", command = decript)  #BOTÃO PARA DESCRIPTOGRAFAR O ARQUIVO
btn7.pack(side = BOTTOM, pady = 10)   #EMPACOTAMENTO DO BOTÃO DESCRIPTOGRAFAR
frame_dcript.pack()                   #EMPACOTAMENTO DO FRAME PRINCIPAL DA ABA

window.mainloop()                     #LOOP DA JANELA PRINCIPAL
