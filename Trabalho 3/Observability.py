## Questão 4: Verificar a propriedade de Observabilidade ##
## Página 208/209 do PDF do livro

## O intuito é criar o autômato ObsTest
## ObsTest(H,G):= Ac((Xh×Xh×Xh)∪{dead},Eε×Eε×Eε,ftest,(x0,H,x0,H,x0,G),{dead})
## e depois verificar se Lm(ObsTest) é vazio ou não (chegou em algum estado 'dead')

from deslab import *

def ObsTest(H,G):
    # Inicialmente crio o conjunto de estados triplos (X_h × X_h × X_g)
    tristates = [(x1,x2,x3) for x1 in H.X for x2 in H.X for x3 in G.X]
    # união com estado 'dead'
    tristates.append(dead)

    # Faço o estado inicial ser (X0_h × X0_h × X0_g)
    x0h = next(iter(H.X0))
    x0g = next(iter(G.X0))
    X0 = [(x0h,x0h,x0g)]

    # Estado marcado é apenas o estado 'dead'
    Xm = ['dead']

    # Declaro o conjunto de eventos, eventos controlaveis e eventos observáveis
    E = G.Sigma
    Eo = G.Sigobs
    Ec = G.Sigcon

    # Aqui cria as transições de ObsTest
    T = []
    # Em cada estado possivel, faz a função ftest
    # para cada evento disponível em sigma
    for xfrom in tristates:
        for ev in G.Sigma:
            tf = ftest(xfrom,ev,H,G)

            # Se ftest retorna uma (ou mais) transição(ões),
            # adiciona ao conjunto de transições
            if tf != None:
                T = join(T,tf)


    nam = "ObsTest({},{})".format(H.name,G.name)

    # Cria o autômato com os dados que criamos acima, e ja tira a parte
    # acessivel dele, para remover os estados não alcançáveis
    obsTest = ac(fsa(tristates,E,T,X0,Xm,Sigobs=Eo,Sigcon=Ec,name = nam))
    obsTest.setgraphic(style='observer')
    draw(obsTest)

    # Se a Lm(ObsTest) é vazia, então H é observavel em relação a G, isso é,
    # não tem uma string que, a partir do estado inicial, alcance o estado 'dead',
    # que indica que há um conflito de controle.
    if isitempty(obsTest):
        print('{} é observável em relação a {}' .format(H.name,G.name))
    else:
        print('{} NÃO é observável em relação a {}' .format(H.name,G.name))
    return(isitempty(obsTest))


## Aqui é implementado a função de transição ftest, que verifica tanto a condição de 
## violação de observabilidade, quanto cria as transições de acordo com algumas regras
def ftest(tristate,e,H,G):

    # Condições para a violação de observabilidade (VO):
    # 1: e ser controlável
    cond1 = e in G.Sigcon
    # 2: fh(x1,e) definido?
    cond2 = any((item[0] == tristate[0]) and (item[1] == e) for item in H.transitions())
    # 3: fh(x2,e) definido?
    cond3 = any((item[0] == tristate[1]) and (item[1] == e) for item in H.transitions())
    # 4: fg(x3,e) definido?
    cond4 = any((item[0] == tristate[2]) and (item[1] == e) for item in G.transitions())
    
    # VO = 1 ∧ 2 ∧ ¬3 ∧ 4
    if (cond1 and cond2 and not cond3 and cond4):

        # Se VO = True: violou as condições de observabilidade e vai para estado 'dead'
        # OBS: Isso é válido tanto para Eo quanto para Euo
        return (tristate,e,'dead')
    else:

        # Como não violou a observabilidade, fazemos ftest:
        # Primeiro, o evento é observável ou não?
        if e in G.Sigobs:

            # Com e observavel, se f(e) for definido nos 3 estados (xh1, xh2, xg),
            # então vai avançar em todos.
            if cond2 and cond3 and cond4:
                x1 = [state[2] for state in H.transitions() if state[:2] == (tristate[0],e)]
                x2 = [state[2] for state in H.transitions() if state[:2] == (tristate[1],e)]
                x3 = [state[2] for state in G.transitions() if state[:2] == (tristate[2],e)]
                return (tristate,e,(x1[0],x2[0],x3[0]))
        else:

            # Com e não observável, temos que verificar duas condições

            # OBS: Criei um vetor para ser possivel retornar uma 
            # ou duas transições de uma vez
            to = []

            # Se f(e) esta definido em xh1,
            # então avança em Xh1, mas não em Xh2 e Xg
            if cond2:
                x1 = [state[2] for state in H.transitions() if state[:2] == (tristate[0],e)]
                x2 = [tristate[1]]
                x3 = [tristate[2]]
                to.append((tristate,e,(x1[0],x2[0],x3[0])))

            # Se f(e) esta definido em xh2 E em xg
            # então avança em Xh2 e Xg, mas não em Xh1
            if cond3 and cond4:
                x1 = [tristate[0]]
                x2 = [state[2] for state in H.transitions() if state[:2] == (tristate[1],e)]
                x3 = [state[2] for state in G.transitions() if state[:2] == (tristate[2],e)]
                to.append((tristate,e,(x1[0],x2[0],x3[0])))

            # Se criou alguma transição, então retorna ela
            if to != []:
                return to
    ## OBS: Se nenhuma condição foi satisfeita, a função retorna nada, 
    ## então é preciso fazer essa verificação ao usar ela
    
    
## Função auxiliar para inserir as novas transições independente de ser
## uma lista ou uma tupla
## (criei ela por algumas dificuldades em python, mas pode ser descartada
## quando conseguir melhorar ftest)
def join(a,b):
	if type(b) == list:
		a = a+b
	if type(b) == tuple:
		a.append(b)
	return a


## Exemplo

syms('u b a dead')

X_1 = [1, 2, 3]
Sig_1 = [u, b]
SigObs = [b]
SigCon = [b]
X0_1 = [1]
Xm_1 = []
T_1 = [(1,u,2),(1,b,3),(2,b,3)]

#G1 = fsa(X_1,Sig_1,T_1,X0_1,Xm_1, Sigobs = SigObs,Sigcon = SigCon, name = '$G_1$')

## H1 observável
X_h = [1,2]
T_h = [(1,b,2)]

#H1 = fsa(X_h,Sig_1,T_h,X0_1,Xm_1, Sigobs = SigObs,Sigcon = SigCon, name = '$H_1$')

#ObsTest(H1,G1)

## H2 não observável
X_h2 = [1,2,3]
T_h2 = [(1,u,2),(2,b,3)]

#H2 = fsa(X_h2,Sig_1,T_h2,X0_1,Xm_1, Sigobs = SigObs,Sigcon = SigCon, name = '$H_2$')

#ObsTest(H2,G1)

