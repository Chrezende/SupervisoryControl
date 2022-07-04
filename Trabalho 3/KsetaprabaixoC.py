#===============================================#
#   Autor: Christiano Henrique Rezende          #
#   Matricula: 120175020                        #
#   Disciplina: CPE 743 - Controle Supervisório #
#   Prof. Dr. Gustavo da Silva Viana            #
#===============================================#

## Questão 3: K seta pra baixo C ##
## Página 181/182 do PDF do livro

## KinfC = Kb Euc* INT M
## Primeiro, faz o fecho de prefixo de K (Kb)
## e o fecho de kleene dos eventos não controlaveis (Euc*)
## Concatena Kb com Euc*
## Por fim, faz a interseção do resultado com M
## KbEuc* x M


from deslab import *

def infC(K, M):
    # Primeiro separa os eventos não-controláveis de M
    # e faz o fecho de prefixo de K (K barra)
    Euc = M.Sigma - M.Sigcon
    Kb = pclosure(K)
    
    # Prepara o fecho de kleene dos eventos não controlaveis
    Euc_est = sigmakleeneclos(Euc,x0=0,label='$q_{\Sigma_{uc}}$')

    # Faz a concatenação de Kb e Euc*, e já faz a interseção com M
    # Essa é a superlinguagem ínfima prefixo-fechada controlável
    Kinfc = (Kb * Euc_est) & M
    Kinfc.name = '$K^{\downarrow C}$'
    Kinfc = Kinfc.renamestates('number')
    return Kinfc

## Exemplo
syms('a1 a2 b1 b2 A B C D E F G H')

table = [(a1,'a_1'),(a2,'a_2'),(b1,'b_1'),(b2,'b_2')]

X_g = [0, 1, 2, 3]
X0 = [0]
Xm = []
E = [a1, a2, b1, b2]
SigCon = [a2, b2]
T_g = [(0,a1,1),(0,a2,2),(1,b1,0),(1,a2,3),(2,b2,0),(2,a1,3),(3,b1,2),(3,b2,1)]
G = fsa(X_g,E,T_g,X0,X_g,table, Sigcon = SigCon, name = 'G') 


X_h = [0, 1, 2, 3, 4, 5, 6, 7]
T_h = [(0,a1,1),(0,a2,4),(1,a2,5),(1,b1,2),(2,a2,6),(2,a1,3),(3,a2,7),
       (4,b2,0),(4,a1,5),(5,b2,1),(5,b1,6),(6,a1,7),(6,b2,0),(7,b2,1)]
H = fsa(X_h,E,T_h,X0,X_h,table, Sigcon = SigCon, name = 'H')

#draw(G,H)
draw(infC(H,G))
