from deslab import *

#syms('en rdy task go1 ret1')

#1a Parte ========================================================
print("=============== Configuração assincrona ===============")

X_m0 = [0,1,2]
Sigma_m0 = ['en','rdy','task']
X0_m0 = [0]
Xm_m0 = [0]
T_m0 = [(0,'rdy',1),(1,'en',2),(2,'task',0)]

M0 = fsa(X_m0,Sigma_m0,T_m0,X0_m0,Xm_m0,name='M0')
print("Módulo Controlador M0:")
print("# Estados: " + str(len(M0)))
print("# Transições: " + str(size(M0)))
print("# Eventos: " + str(len(M0.Sigma)))
print('')

X_m1 = [0,1]
Sigma_m1 = ['ret1','go1']
X0_m1 = [0]
Xm_m1 = [0]
T_m1 = [(0,'go1',1),(1,'ret1',0)]

M1 = fsa(X_m1,Sigma_m1,T_m1,X0_m1,Xm_m1,name='M1')
print("Máquina M1:")
print("# Estados: " + str(len(M1)))
print("# Transições: " + str(size(M1)))
print("# Eventos: " + str(len(M1.Sigma)))
print('')

X_mb1 = [0,1]
Sigma_mb1 = ['en','go1']
X0_mb1 = [0]
Xm_mb1 = [0]
T_mb1 = [(0,'en',1),(1,'go1',0),(1,'en',1)]

MB1 = fsa(X_mb1,Sigma_mb1,T_mb1,X0_mb1,Xm_mb1,name='MB1')
print("Supervisor (Mailbox) MB1:")
print("# Estados: " + str(len(MB1)))
print("# Transições: " + str(size(MB1)))
print("# Eventos: " + str(len(MB1.Sigma)))
print('')

Sync1 = M0//M1//MB1
Sync1.name = 'M0|M1|MB1'
print("||(M0,M1,MB1):")
print("# Estados: " + str(len(Sync1)))
print("# Transições: " + str(size(Sync1)))
print("# Eventos: " + str(len(Sync1.Sigma)))
print('')

print("Análise de especificações: ==============================")
Sync1M = Sync1.setpar(Xm=Sync1.X)

X_rec1 = [0,1,2]
Sigma_rec1 = ['en','go1','ret1']
X0_rec1 = [0]
Xm_rec1 = [2]
T_rec1 = [(0,'go1',1),(1,'en',2)]

Rec1 = fsa(X_rec1,Sigma_rec1,T_rec1,X0_rec1,Xm_rec1,name='en->go1')

X_rec2 = [0,1,2]
Sigma_rec2 = ['go1','ret1','en']
X0_rec2 = [0]
Xm_rec2 = [2]
T_rec2 = [(0,'ret1',1),(1,'go1',2)]

Rec2 = fsa(X_rec2,Sigma_rec2,T_rec2,X0_rec2,Xm_rec2,name='go1->ret1')

RecK1 = Rec1+Rec2
RecK1.name = "Vio(1)"


SyncK1 = trim(parallel(Sync1M,RecK1))
SyncK1.name = 'Rec(K1)'

print("Específicação K1: (en->go1) OU (go1->ret1)")
#print("# Estados de Rec(K1): " + str(len(SyncK1)))
print("Atende a especificação K1? "+str(isitempty(SyncK1)))



#SyncK2 = trim(parallel(Sync1M,RecK2))
#SyncK2.name = 'Rec(K2)'
#print("Específicação K2: go1->ret1")
#print("# Estados de Rec(K2): " + str(len(SyncK2)))
#print("Atende a especificação K2? "+str(isitempty(SyncK2)))

print('\n')
#2a Parte ========================================================
print("=============== Adicionando uma máquina ===============")
M2 = M1.renamevents([('ret1','ret2'),('go1','go2')])
M2.name = 'M2'
MB2 = MB1.renamevents([('go1','go2')])
MB2.name = 'MB2'


M = parallel(M1,M2)
M.name = 'M(1,2)'
print("M(1,2):")
print("# Estados: " + str(len(M)))
print("# Transições: " + str(size(M)))
print("# Eventos: " + str(len(M.Sigma)))
print('')
MB = parallel(MB1,MB2)
MB.name = 'MB(1,2)'
print("MB(1,2)")
print("# Estados: " + str(len(MB)))
print("# Transições: " + str(size(MB)))
print("# Eventos: " + str(len(MB.Sigma)))
print('')

Sync2 = M0//M//MB
Sync2.name = 'M0|M|MB'
print("||(M0,M(1,2),MB(1,2)):")
print("# Estados: " + str(len(Sync2)))
print("# Transições: " + str(size(Sync2)))
print("# Eventos: " + str(len(Sync2.Sigma)))
print('')

print("Análise de especificações: ==============================")
print("K2: (en->go1) OU (go1->ret1) OU (en->go2) OU (go2->ret2)\n")
Sync2M = Sync2.setpar(Xm=Sync2.X)

Rec3 = RecK1.renamevents([('go1','go2'),('ret1','ret2')])
Rec3 = Rec3.addevent(RecK1.Sigma)
Rec3.name = "K2"
RecK1 = RecK1.addevent(Rec3.Sigma)
#Rec3.name = 'Vio(2)'

#RecK4 = RecK2.renamevents([('go1','go2'),('ret1','ret2')])
#RecK4.name = 'K4: go2->ret2'

RecK2 = RecK1+Rec3
RecK2.name = "Vio(2)"

SyncK2 = trim(parallel(Sync2M,RecK2))
SyncK2.name = 'Rec(K2)'
#print("# Estados de Rec(K1): " + str(len(SyncK12)))
print("Atende a especificação K2? "+str(isitempty(SyncK2)))

#SyncK22 = trim(parallel(Sync2M,RecK2))
#SyncK22.name = 'Rec(K2)'
#print("# Estados de Rec(K2): " + str(len(SyncK22)))
#print("Atende a especificação K2? "+str(isitempty(SyncK22)))

#SyncK3 = trim(parallel(Sync2M,RecK3))
#SyncK3.name = 'Rec(K3)'
#print("# Estados de Rec(K3): " + str(len(SyncK2)))
#print("Atende a especificação K3? "+str(isitempty(SyncK3)))

#SyncK4 = parallel(Sync2M,RecK4)
#SyncK4.name = 'Rec(K4)'
#print("# Estados de Rec(K4): " + str(len(SyncK2)))
#print("Atende a especificação K4? "+str(isitempty(SyncK4)))

print('\n')
#2a Parte-B ======================================================
print("=============== Aumentando quantidade de máquinas! ===============")
print("3 máquinas:")
M3 = M1.renamevents([('ret1','ret3'),('go1','go3')])
MB3 = MB1.renamevents([('go1','go3')])

Ma3 = parallel(M,M3)
MBa3 = parallel(MB,MB3)
print("# Estados M: " + str(len(Ma3)))
print("# Estados MB: " + str(len(MBa3)))

print('')

SyncA3 = M0//Ma3//MBa3
print("# Estados: " + str(len(SyncA3)))
print("# Transições: " + str(size(SyncA3)))
print("# Eventos: " + str(len(SyncA3.Sigma)))
print('')

print("4 máquinas:")
M4 = M1.renamevents([('ret1','ret4'),('go1','go4')])
MB4 = MB1.renamevents([('go1','go4')])

Ma4 = parallel(Ma3,M4)
MBa4 = parallel(MBa3,MB4)
print("# Estados M: " + str(len(Ma4)))
print("# Estados MB: " + str(len(MBa4)))

SyncA4 = M0//Ma4//MBa4
print("# Estados: " + str(len(SyncA4)))
print("# Transições: " + str(size(SyncA4)))
print("# Eventos: " + str(len(SyncA4.Sigma)))
print('')

print("5 máquinas:")
M5 = M1.renamevents([('ret1','ret5'),('go1','go5')])
MB5 = MB1.renamevents([('go1','go5')])

Ma5 = parallel(Ma4,M5)
MBa5 = parallel(MBa4,MB5)
print("# Estados M: " + str(len(Ma5)))
print("# Estados MB: " + str(len(MBa5)))

SyncA5 = M0//Ma5//MBa5
print("# Estados: " + str(len(SyncA5)))
print("# Transições: " + str(size(SyncA5)))
print("# Eventos: " + str(len(SyncA5.Sigma)))
print('\n')

#3a Parte ========================================================
print("=============== Alterando Configuração para Síncrona ===============")
print("2 máquinas:\n")

X_n = [0,1,2,3,4]
Sigma_n = ['en','go1','go2','task']
X0_n = [0]
Xm_n = [0]
T_n = [(0,'en',1),(1,'go1',2),(1,'go2',3),(2,'go2',4),(3,'go1',4),(4,'task',0)]

N = fsa(X_n,Sigma_n,T_n,X0_n,Xm_n,name='N2')
print("N:")
print("# Estados: " + str(len(N)))
print("# Transições: " + str(size(N)))
print("# Eventos: " + str(len(N.Sigma)))
print('')

Sync3 = parallel(N,M)
Sync3.name = 'N|M'
print("||(N,M(1,2))")
print("# Estados: " + str(len(Sync3)))
print("# Transições: " + str(size(Sync3)))
print("# Eventos: " + str(len(Sync3.Sigma)))
print('')
draw(simplify(Sync3),'figure')


#Imagens =========================================================

#Parte1
#draw(M0,'figure')
#draw(M1,'figure')
#draw(MB1,'figure')
#draw(Sync1,'figure')
#draw(RecK1,'figure')


#Parte2
#draw(M2,'figure')
#draw(MB2,'figure')
#draw(M,'figure')
#draw(MB,'figure')
#draw(Sync2,'figure')
#draw(RecK2,'figure')

#Parte3
#draw(N,'figure')
#draw(Sync3,'figure')
