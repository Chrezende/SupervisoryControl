from deslab import *

# Definindo Autômato G

syms('a b c')

X = [1,2,3,4,5]
Sigma = [a,b,c]
X0 = [1]
Xm = [2]
T = [(1,a,2),(1,b,3),(2,a,3),(3,b,2),(3,c,4),(5,a,3)]
G = fsa(X,Sigma,T,X0,Xm,name = 'G')

# Função que impede estado ilegal de acontecer

def IlegalState(G, state):
    S = deletestate(G, state)       # Deleta o estado ilegal
    S = ac(S)                       # Tira a parte acessivel (Esse é o Supervisor)
    Ha = parallel(G,S)              # Faz o paralelo G|S
    Ha.name = "Ha"		    # Renomeia o autômato para Ha
    return Ha                       # Retorna autômato controlado

draw(G, IlegalState(G,3))
