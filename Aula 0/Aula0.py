from deslab import *

# Definindo simbolos
syms('a b c')

# Criando o FSA G1
X = [1,2,3,4,5]
Sigma = [a,b,c]
X0 = [1]
Xm = [2]
T = [(1,a,2),(1,b,3),(2,a,3),(3,b,2),(3,c,4),(5,a,3)]
G1 = fsa(X,Sigma,T,X0,Xm,name = 'G1')

# Tirando a parte Acessível de G1
AcG1 = ac(G1)
#AcG1(name = 'Ac(G1)')

# Tirando a parte Co-Acessível de G1
CoAcG1 = coac(G1)
#CoAcG1(name = 'CoAc(G1)')

# Fazendo o Trim de G1
TrimG1 = trim(G1)
#TrimG1(name = 'Trim(G1)')

# Desenhando os autômatos
draw(G1, AcG1, CoAcG1, TrimG1)
