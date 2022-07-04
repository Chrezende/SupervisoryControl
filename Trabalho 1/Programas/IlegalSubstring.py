from deslab import *

# Definindo Autômato G

syms('a b c')

X = [1,2,3,4,5]
Sigma = [a,b,c]
X0 = [1]
Xm = [2]
T = [(1,a,2),(1,b,3),(2,a,3),(3,b,2),(3,c,4),(5,a,3)]
G = fsa(X,Sigma,T,X0,Xm,name = 'G')

# Criando função que impede uma subsequencia ilegal de acontecer

def IlegalSubstring(G, substring):
    Xs = [] # Iniciando array de estados
    Ts = [] # Iniciando array de transiçõ

    # Criando os estados e transições da subsequencia ilegal
    for i in range(len(substring)):
        statename = 'S' + str(i)    # Nomeando o estado
        syms(statename)             # Criando Símbolo
        Xs.append(statename)        # Adicionando Estado no autômato
        # A partir do segundo estado criar transição que liga a ele
        if i>0:                     
            Ts.append((Xs[i-1],substring[i-1],Xs[i]))

    Xs0 = Xs[0] # Estado inicial
    Xsm = Xs    # Marcando todos os estados

    # Varrendo os estados para criar as transições
    for x in Xs:
        ind = Xs.index(x)       # Guardando o índice do estado
        pref = substring[:ind]  # Guardando os eventos ocorridos ate o estado atual

        # Varrendo os eventos
        for event in Sigma:
            # Se for o evento da substring, a transição ja foi criada, então ignora
            if event != substring[ind]:
                # Concatenando os eventos até o estado com o evento da transição
                prefx = pref+event  
                maxsuffix = 0   # Instanciando inteiro para comparação
                for i in range(ind+1):
                    # Compara o sufixo da palavra que estou verificando
                    # com o prefixo da substring ilegal
                    if prefx[(len(prefx)-1)-i:] == substring[:(i+1)]:
                        # Se achou um sufixo em comum, verifica se vai para um 
                        # estado maior e salva esse valor
                        maxsuffix = max(maxsuffix,(i+1))
                # Cria transição do estado para o índice que achou
                Ts.append((x,event,Xs[maxsuffix]))

    # Cria autômato supervisor S
    S = fsa(Xs,Sigma,Ts,Xs0,Xsm,name = 'S')
    draw(S)

    Ha = parallel(G,S)  # Faz o paralelo G|S
    Ha.name = 'Ha'      # Renomeia o autômato para Ha
    return Ha           # Retorna autômato controlado

draw(G, IlegalSubstring(G,"aac"))
