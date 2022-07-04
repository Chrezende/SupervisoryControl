from deslab import *

# Definindo Autômato G
syms('a b c')

X = [1,2,3,4,5]
Sigma = [a,b,c]
X0 = [1]
Xm = [2]
T = [(1,a,2),(1,b,3),(2,b,3),(3,a,2),(3,c,4),(5,a,3)]
G = fsa(X,Sigma,T,X0,Xm,name = 'G')

# Função que obriga a alternância dos eventos especificados
syms('S0 S1 S2 S3 S4')      # Definindo nome dos estados de S
def EventAlternation(G, ev1, ev2):
    # Criando o Supervisor de alternância de eventos
    Xs = [S0, S1, S2, S3, S4]
    Sigma_s = [ev1, ev2]
    Ts = [(S0,ev1,S1),(S0,ev2,S3),(S1,ev2,S2),(S2,ev1,S1),(S3,ev1,S4),(S4,ev2,S3)]
    X0s = [S0]
    Xms = Xs
    S = fsa(Xs, Sigma_s, Ts, X0s, Xms, name = 'S')
    draw(S)

    Ha = parallel(G,S)      # Faz paralelo G|S
    Ha.name = "Ha"          # Renomeia o autômato para Ha
    return Ha               # Retorna autômato controlado

draw(G, EventAlternation(G,a,b))
