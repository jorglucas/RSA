#-*- coding: utf-8 -*-

import time
import secrets
import math
import random
from random import randint

#dicionarios que ajudam na criptografia(dicionario1) e descriptografia(dicionario2)
dicionario1 = {"a" : 2, "b" : 3, "c" : 4, "d" : 5, "e" : 6, "f" : 7, "g" : 8, "h" : 9, "i" : 10, "j" : 11,"k" : 12,
  "l" : 13, "m": 14, "n":15, "o" : 16, "p" : 17, "q": 18, "r" : 19, "s":20, "t":21, "u":22, "v":23, "w":24,"x":25,
  "y":26, "z":27, " ":28}

dicionario2 = {2 : "a", 3 : "b", 4 : "c", 5 : "d", 6 : "e" , 7 : "f" , 8 : "g", 9 : "h", 10 : "i", 11: "j" , 12 : "k" ,
  13 : "l", 14 : "m", 15 : "n", 16 : "o", 17 : "p", 18 : "q", 19 : "r", 20 : "s", 21: "t", 22 : "u", 23: "v", 24 : "w",
  25 : "x", 26 : "y", 27 : "z", 28 : " "}

#funcoes matematicas, pelas quais o usuario nao interage

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

    print("Para gerar a chave sao necessarios dois numeros primos diferentes entre si e de um numero primo em relacao a eles, quanto maiores os numeros, mais dificil de quebrar o codigo")
    print("Deseja digitar os valores desses dois numeros e de um numero primo em relacao aos mesmos, ou prefere que o sistema os gere automaticamente?")
    
    n = int(input("1 - Gostaria de digitar os valores dos numeros!\n2 - Gere os numeros automaticamente!\n"))

    #entrada dinamica na qual o usuario pode utilizar numeros ja escolhidos por ele para gerar a chave
    if n == 1: 
        p = int(input("Digite o valor de p (primeiro numero primo): "))

        while(test_prime(p) == False):
            print("O valor que você tentou atribuir a p nao e primo!\nTente outro valor!")
            p = int(input("Digite o valor de p (primeiro numero primo): "))

        q = int(input("Digite o valor de q (segundo numero primo): "))

        while(test_prime(q) == False):
            print("O valor que você tentou atribuir a q nao e primo!\nTente outro valor!")
            q = int(input("Digite o valor de q (segundo numero primo): "))
        while p == q:
            print("Você digitou dois valores iguais para p e q\nDigite outro valor diferente de p:")
            q = int(input("Digite o valor de q (segundo numero primo): "))
            while(test_prime(q) == False):
                print("O valor que você tentou atribuir a q nao e primo!\nTente outro valor!")
                q = int(input("Digite o valor de q (segundo numero primo): "))
        n = p*q
        tot_n = phi(p, q)

        e = int (input("Digite um numero relativamente primo a 'p' e 'q': "))

        while euclides(tot_n, e) !=1:
            print("Valor invalido (esse numero nao e co-primo)")
            e = int (input("Digite um numero relativamente primo a 'p' e 'q': "))

    #entrada "estatica" na qual todos os valores sao gerados pelo sistema
    else: 
        p = gen_prime()
        q = gen_prime()
        while p == q:
            q = gen_prime()
        n = p*q
        tot_n = phi(p, q)
        e = co_primos(tot_n)

    chave_publica = ("Valores da chave pública:\nn = %d e = %d\n" %(n,e))
    chave_privada = ("Valores da chave privada:\np = %d q = %d\n" %(p, q))
    key = open("public_key.txt", "w")
    key_p = open("private_key.txt", "w")
    key_p.write(chave_privada)
    key.write(chave_publica)
    key_p.close()
    key.close()
    print("Chaves geradas com sucesso! Agora use-a para criptografar um texto!\nVocê pode encontrá-las nos arquivos key.txt e key_p.txt localizados no diretorio desse programa!")


def decript():
    #entradas do usuario
    #file_name = input("Digite o nome do arquivo criptografado(sem o .txt): ")
    e = int (input('Digite o valor "e" da chave pública: '))
    p = int (input('Digite o valor "p": '))
    q = int (input('Digite o valor "q": '))

    #calculo dos valores necessarios
    n = p*q
    tot_n = (p-1) * (q-1)
    d = inversom_m (e, tot_n) #inverso multiplicativo de e, fundamental para a descriptografia

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

    print("Arquivo descriptografado com sucesso!\nEncontre-o no diretorio desse programa sob o nome de decripted.txt")


def encript():

    #entradas providas pelo usuario
    n = int(input('Digite o valor "n" da chave publica: '))
    e = int(input('Digite o valor "e" da chave publica: '))
    mensagem  = input("Digite a mensagem que deseja criptografar (em minusculo, sem acentos e pontuação): ")
    mensagem = mensagem.lower()
    #file_name = input("Digite o nome do arquivo txt no qual o texto criptografado sera guardado (apenas o nome): ")

    
    i = 0
    error = 0
    criptografado = ""
    while i < len(mensagem):
        #objetos auxiliares
        list_int_pow = [] #lista auxiliar que vai guardar dados para o funcionamento da funcao exponencial modular rapida  
        #x = dicionario1[mensagem[i]]#valor de determinado caracter atribuido de acordo com o dicionario
        try :
            x = dicionario1[mensagem[i]]
        except :
            error = -1
            print("Caracter Inválido Corno!")
            break
        x = dicionario1[mensagem[i]]#valor de determinado caracter atribuido de acordo com o dicionario
        convert = int_bin(e, "") #convertendo o valor de e (o expoente da potenciacao) em binario
        generate_list_int(convert, list_int_pow) #armazenando em "list_int pow" os valores na base 2  que decompoem o valor e

        y = exp_mod_rap( list_int_pow, x, n, 1, 0) #exponenciacao modular rapida para criptografar a mensagem
            
        criptografado = criptografado + str(y%n) +" "#gerando string que contem a mensagem criptografada
        i+=1

    #manipulando arquivo de saida
    if error == -1:
        print("Não foi possível gerar o arquivo pois sua mensagem não obedeceu os parâmetros propostos!")
    else:
        arquivo = open("encripted.txt", "w") #gerando arquivo txt que guardará o texto descriptografado
        arquivo.write(criptografado) #escrevendo a mensagem criptografada no arquivo

        print("Seu arquivo foi criptografado com sucesso!\nO mesmo se encontra no diretorio desse programa sob o nome de encripted.txt")


#interacao com o usuario

comando = 10000
print("-------------------------------------------------------------------")
print("Bem vindo ao nosso algoritmo que realiza criptografia/descritografia RSA!")
while comando != 0:
    print("-------------------------------------------------------------------")
    comando = int(input("O que deseja fazer?\n1 - Gerar uma chave pública\n2 - Criptografar uma mensagem\n3 - Descritografar um arquivo\n0 - Sair\n"))
    print("-------------------------------------------------------------------")
    if comando == 1:
        generate_key()
    elif comando == 2:
        encript()
    elif comando == 3:
        decript()
