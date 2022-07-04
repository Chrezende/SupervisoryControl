#===============================================#
#   Autor: Christiano Henrique Rezende          #
#   Matricula: 120175020                        #
#   Disciplina: CPE 743 - Controle Supervisório #
#   Prof. Dr. Gustavo da Silva Viana            #
#===============================================#

## Questão 2: K seta pra cima C, tanto genérico quanto para K = Kbarra ##
## Caso pref. fechado: 179 do PDF do livro
## Caso genérico: Página 187 do PDF do livro

## Passos para o caso Prefixo-Fechado:
## Faz a diferença entre M e K: M - K
## Faz o quociente com o fecho de kleene dos eventos não controláveis:
## (M-K) / Euc* (quotient)
## Depois concatena com o fecho de kleene de todos os eventos
## [(M-K)/Euc*] E*
## Por fim, retira isso tudo de K, fazendo a diferença entre eles
## K - [(M-K)/Euc*]E*


from deslab import *

## Caso Prefixo-Fechado:
def supC_pf(K, M):
    # Para começar, marca todos os estados de M e separa os eventos não-controláveis
    Mm = M.setpar(Xm = M.X)
    Euc = K.Sigma - K.Sigcon

    # Faz a diferença de M e K
    G1 = (M - K)
    G1.name = '$M-K$'

    # Prepara o fecho de kleene dos eventos não controlaveis
    Euc_est = sigmakleeneclos(Euc,x0=0,label='$q_{\Sigma_{uc}}$')
    # Faz o quociente entre M-K e Euc*
    G2 = G1/Euc_est
    G2.name = '$(M-K)/{E^{*}}_{uc}$'

    # Prapara o fecho de kleene de todos os eventos
    E_est = sigmakleeneclos(K.Sigma,x0=0,label='$q_{\Sigma}$')
    # Concatena o resultado ate então com E*
    G3 = G2*E_est
    G3.name = '$[(M-K)/{E^{*}}_{uc}]E$'

    # Faz a diferença entre K e o resultado até o momento,
    # essa é a sublinguagem suprema controlavel
    Ksupc = K - G3
    Ksupc.name = '$K^{spc C}$'
    Ksupc = Ksupc.renamestates('number')
    return Ksupc

## Caso genérico:
## (como o livro adota H, e G no algoritmo, decidi usar a mesma nomenclatura)
def supC(H, G):
    # Para começar, marca todos os estados de G e separa os eventos não-controláveis
    Gm = G.setpar(Xm = G.X)
    Euc = G.Sigma - G.Sigcon

    # Faz um autômato Hi que é a interseção entre H e Gm
    # em sequencia iguala os eventos controláveis e observáveis com G
    Hi = H & Gm
    Hi = Hi.setpar(Sigcon = G.Sigcon, Sigobs = G.Sigobs, name='supC(L(%s))'%(H.name))

    # Começa o processo iterativo criando uma variável auxiliar com valor 1
    # para poder entrar no loop while
    aux = 1
    while aux:
        aux = 0

        # Verifica todos os estados de Hi(xh,xg)
        for (x,xg) in Hi.X:
            
            # Existe uma transição com evento não controlavel em G
            # que não está no produto Hi?
            if not(Gm.Gamma(xg) & Euc <= Hi.Gamma((x,xg))):
                
                # Se existir, apaga esse estado e continua as iterações
                Hi = Hi.deletestate((x,xg))
                aux = 1
                
        # Quando terminar de varrer os estados, faz o trim (Ac e CoAc)
        # de Hi para eliminar os estados não alcançaveis e os bloqueios
        Hi = trim(Hi)

        # Se Hi ficar vazio, então não tem necessidade de continuar o loop
        # então retorna Ksupc = vazio
        if isitempty(Hi):
            return Hi
        # Sai do loop quando não houver mais estados que "escapem"
        # com um evento não-controlavel
    Hi = Hi.renamestates('number')
    return Hi

    
## Exemplo
syms('a1 a2 b1 b2')

table = [(a1,'a_1'),(a2,'a_2'),(b1,'b_1'),(b2,'b_2')]

X_g = [0, 1, 2, 3, 4, 5, 6, 7, 8]
X0 = [0]
Xm = [8]
E = [a1, a2, b1, b2]
SigCon = [a1, b1]
T_g = [(0,a1,1),(1,b1,2),(0,a2,3),(1,a2,4),(2,a2,5),(3,a1,4),(4,b1,5),(3,b2,6),(4,b2,7),(5,b2,8),(6,a1,7),(7,b1,8)]
G = fsa(X_g,E,T_g,X0,Xm,table, Sigcon = SigCon, name = 'G')
#draw(G)

X_ha = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
T_ha = [(0,a1,1),(1,b1,2),(0,a2,3),(1,a2,9),(2,a2,5),(3,a1,4),(9,b1,5),(3,b2,6),(4,b2,7),(5,b2,8),(6,a1,7),(7,b1,8)]
Ha = fsa(X_ha,E,T_ha,X0,Xm,table, Sigcon = SigCon, name = 'Ha')
#draw(Ha)

draw(supC_pf(Ha, G))
draw(supC(Ha,G))

