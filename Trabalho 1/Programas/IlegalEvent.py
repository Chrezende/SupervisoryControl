from deslab import *

# Definindo Autômato G

syms('a b c')

X = [1,2,3,4,5]
Sigma = [a,b,c]
X0 = [1]
Xm = [2]
T = [(1,a,2),(1,b,3),(2,a,3),(3,b,2),(3,c,4),(5,a,3)]
G = fsa(X,Sigma,T,X0,Xm,name = 'G')

# Função que impede evento ilegal de acontecer

def IlegalEvent(G, event):
    S = sigmakleeneclos(G.Sigma)    #Faz fecho de Kleene com os eventos de G
    S = S.deletevent(event)         #Deleta o evento ilegal (esse é o Supervisor)
    Ha = product(G,S)               #Faz o produto de G x S
    Ha.name = 'Ha'                  # Renomeia o autômato para Ha
    return Ha                       #Retorna autômato controlado

draw(G, IlegalEvent(G,c))
