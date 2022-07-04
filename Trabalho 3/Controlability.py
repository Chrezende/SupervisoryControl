#===============================================#
#   Autor: Christiano Henrique Rezende          #
#   Matricula: 120175020                        #
#   Disciplina: CPE 743 - Controle Supervisório #
#   Prof. Dr. Gustavo da Silva Viana            #
#===============================================#

## Questão 1: Verificar se K é controlavel ##
## Página 167 do PDF do livro

## Fazer prefixo fechado de K
## Fazer self-loops com Euc
## Fazer produto com M (Kbarra Euc INTERSEÇÃO M: KbEucIntM)
## Se KbEucIntM está contido em Kb (*)
## Retorna SIM
## Caso contrário
## Retorna NÃO

## (*) O operador <= faz a verificação se A esta contido em B: A <= B
## e retorna verdadeiro ou falso
## Obs: ele faz essa operação ao fazer o complemento de B, depois a interseção
## de A e B, e verificando se Lm é vazio

from deslab import *

def Controlable(K, M):
    # Primeiro separa os eventos não-controláveis de M
    Euc = M.Sigma - M.Sigcon

    # Faz o fecho de prefixo de K (K barra)
    Kb = pclosure(K)
    Kb.name = '$\overline{K}$'

    # Concatena K barrado com os eventos não-controlaveis
    # para isso adiciono um self-loop em todos os estados com os Euc
    KbEuc = Kb
    for q in Kb.X:
        for euc in Euc:
            # Apenas verifico se ja existe uma transição com o Euc no estado
            # para o autômato permanecer determinístico
            if not any((item[0] == q) and (item[1] == euc) for item in K.transitions()):
                KbEuc = KbEuc.addselfloop(q,euc)
    KbEuc.name = '$\overline{K}{E}_{uc}$'

    # Faz a interseção de K barra Euc com M,
    # para isso basta fazer o produto entre os dois
    KbEucIM = KbEuc & M
    KbEucIM.name = '$\overline{K}{E}_{uc} \cap M$'
    
    # Se o resultado dessa interseção está contido no fecho de prefixo de K,
    # então K é controlável em relação a M
    if KbEucIM <= Kb:
        print(K.name + " é controlável em relação a " + M.name)
    else:
        print(K.name + " NÃO é controlável em relação a " + M.name)
        

## Exemplo
#syms('a1 a2 b1 b2')
#
#table = [(a1,'a_1'),(a2,'a_2'),(b1,'b_1'),(b2,'b_2')]

#X_g = [0, 1, 2, 3, 4, 5, 6, 7, 8]
#X0 = [0]
#Xm = [8]
#E = [a1, a2, b1, b2]
#SigCon = [b2, b1]
#T_g = [(0,a1,1),(1,b1,2),(0,a2,3),(1,a2,4),(2,a2,5),(3,a1,4),(4,b1,5),(3,b2,6),(4,b2,7),(5,b2,8),(6,a1,7),(7,b1,8)]
#G = fsa(X_g,E,T_g,X0,Xm,table, Sigcon = SigCon, name = 'G')

#X_ha = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
#T_ha = [(0,a1,1),(1,b1,2),(0,a2,3),(1,a2,9),(2,a2,5),(3,a1,4),(9,b1,5),(3,b2,6),(4,b2,7),(5,b2,8),(6,a1,7),(7,b1,8)]
#Ha = fsa(X_ha,E,T_ha,X0,Xm,table, Sigcon = SigCon, name = 'Ha')

#Controlable(Ha, G)
