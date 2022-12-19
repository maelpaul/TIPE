from math import *
import random as rd
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os #pour la suppression des fichiers créés
import sys #pour tuer le programme quand la localisation initiale est impossible


#longitude=CYCX ; latitude=CYCY


path = './'
if os.path.exists(path+'trajectoires x'):
    os.remove(path+'trajectoires x')
if os.path.exists(path+'trajectoires y'):
    os.remove(path+'trajectoires y')
if os.path.exists(path+'trajectoire moyenne'):
    os.remove(path+'trajectoire moyenne')
for i in range(1,1001):
    if os.path.exists(path+'trajectoire '+str(i)):
        os.remove(path+'trajectoire '+str(i))


#cartopy
latitude_min=0
latitude_max=60
longitude_min=-110
longitude_max=0

ax = plt.axes(projection=ccrs.PlateCarree(),autoscale_on=False,xlim=(longitude_min,longitude_max),ylim=(latitude_min,latitude_max))
ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)


#quadrillage
for i in range(10,60,10):
    plt.plot([-110,0],[i,i],'-',color='grey',linewidth=0.8)

for j in range(10,110,10):
    plt.plot([-j,-j],[0,60],'-',color='grey',linewidth=0.8)


base=open("base.txt","r") #ouvre le fichier txt contenant la base de données normalisée à exploiter
m=base.readlines() #crée un tableau contenant les lignes de la base en chaines de caractères
base.close()


def traitement_int(t,c):
    L = []
    a = ""
    for i in range (1, len(t[c])):
        if t[c][i] == "]":
            L.append(int(a)) 
            return L
        elif t[c][i] == ",":
            L.append(int(a))
            a = ""
        else:
            a += t[c][i]


def traitement_float(t,c):
    L = []
    a = ""
    for i in range (1, len(t[c])):
        if t[c][i] == "]":
            L.append(float(a)) 
            return L
        elif t[c][i] == ",":
            L.append(float(a))
            a = ""
        else:
            a += t[c][i]


CYCX,CYCY=[],[]
cyclonex=open("coord_x.txt","r")
mx=cyclonex.readlines()
cyclonex.close()
cycloney=open("coord_y.txt","r")
my=cycloney.readlines()
cycloney.close()

for i in range(len(mx)):
    CYCX.append(traitement_float(mx,i))
    CYCY.append(traitement_float(my,i))


l=[] #base des localisations
loc=open("localisation.txt","r")
ml=loc.readlines()
loc.close()

for i in range(len(ml)):
    l.append(traitement_int(ml,i))


def loc_init(t): #renvoie la localisation initiale du cyclone
    n = rd.randint(0,len(t)-1) #renvoie un entier aléatoire entre 0 et len(t)-1
    return t[n][0]


bd1=np.zeros((6601,1),dtype = list) #base de données des localisations suivantes possibles
bd2=np.zeros((6601,1),dtype = list) #base de données des probabilités associés
bd1_storage=open("bd1_storage.txt","r")
m1=bd1_storage.readlines()
bd1_storage.close()
bd2_storage=open("bd2_storage.txt","r")
m2=bd2_storage.readlines()
bd2_storage.close()


for i in range(6601):
    bd1[i,0] = traitement_int(m1,i)
    bd2[i,0] = traitement_float(m2,i)


def position_suivante(a): #fonction qui donne la localisation suivante du cyclone ; a = localisation présente
    M = bd1[a,0]
    P = bd2[a,0]
    n = rd.random() #renvoie un réel aléatoire entre 0 et 1
    s = P[0] #somme des probabilités qui vaut 1 au maximum
    for i in range (len(P)): #P et M ont la même longueur
        if n <= s:
            return M[i]
        else:
            s = s + P[i+1]


def trajectoire_cyclone(a): #fonction qui renvoie la liste des localisations successives du cyclone ; a = localisation initiale
    m = a
    L = [] #liste des localisations successives du cyclone
    while m != 0:
        L.append(m)
        m = position_suivante(m)
    return L


def liste_moins(L): #applique un x(-1) à tous les éléments de la liste
    M=[]
    for i in range(len(L)):
        M.append(-L[i])
    return M


def name(t,n): #fonction récupérant le nom et la date pour un cyclone de la base de données (t), n = (numéro du cyclone)-1 (le -1 permet de commencer à 0 au 1er cyclone rencontré pour avoir la correspondance avec les indices d'une liste)
    a = -1 #compte le nombre de cyclones rencontrés, -1 pour 0 cyclone rencontré (même raison que pour n)
    name = ""
    for i in range(len(t)):
        if t[i][0] == "A": #correspond à un nouveau cyclone à traiter
            a += 1 #on augmente de 1 le nombre de cyclones rencontrés
            if a == n:
                c = t[i][4]+t[i][5]+t[i][6]+t[i][7] #année du cyclone
                j = 9 #premier blanc de la ligne du nom
                while t[i][j] != ",": #boucle qui donne le nom du cyclone
                    if t[i][j] != " ":
                        name = name + t[i][j]
                    j+=1
                name = name + " " + c
                return name


n = int(input("Rentrer le nombre de cyclones à tracer (nombre entre 1 et 1000 inclus) : ")) #nombre de cyclones à tracer
aa = int(input("Localisation initiale du cyclone (nombre entre 0 et 6600 inclus, si 0 localisation initiale aléatoire) : ")) #la localisation initiale est un nombre compris entre 1 et 6600 obtenu avec la formule du calcul de la localisation
if (aa == 0):
    a = loc_init(l) #l = base des localisations
else:
    a = aa


M = [] #liste des indices de ligne contenant par a
for i in range(len(l)):
    for j in range(len(l[i])):
        if l[i][j] == a:
            if (i in M) == False:
                M.append(i)
if M == []:
    print("localisation initiale impossible") #la localisation n'est pas présente dans la base de données
    sys.exit() #tue le programme
# else:
#     for i in range(len(M)):
#         nom = name(m,M[i]) #m = base de données
#         X = liste_moins(CYCX[M[i]])
#         Y = CYCY[M[i]]
#         plt.plot(X,Y,'-',linewidth=2,label=nom) #trace tous les cyclones ayant commencé à la localisation a


traj=[]

for k in range(1,n+1):
    L = trajectoire_cyclone(a)
    X = []
    Y = []
    A = []
    nom="trajectoire "+str(k)
    for i in range (len(L)):
        x = ((L[i]-1)%110) + 0.5 #-1 pour compenser le +1 de la formule ; %110 pour accéder au reste = longitude ; +0.5 pour centrer au milieu d'un carré de 1°x1°
        y = ((L[i]-1)//110) + 0.5 #-1 pour compenser le +1 de la formule ; //110 pour accéder au quotient = latitude ; +0.5 pour centrer
        X.append(-x) #-x pour l'utilisation de cartopy
        Y.append(y)
        A.append(x)
    traj.append([nom,A,Y])
    cyclone=open(nom,"a") #crée un fichier avec les listes des coordonnées
    cyclone.write("X:"+str(traj[k-1][1])+"\n")
    cyclone.write("Y:"+str(traj[k-1][2])+"\n")
    cyclone.close()
    plt.plot(X,Y,'-',linewidth=2,label=nom)


for i in range(1,n+1):
    t1 = traj[i-1][1]
    t2 = traj[i-1][2]
    trajx = open("trajectoires x","a") #crée le fichier avec la liste des abscisses de tous les cyclones modélisés
    trajx.write(str(t1)+"\n")
    trajx.close()
    trajy = open("trajectoires y","a") #crée le fichier avec la liste des ordonnées de tous les cyclones modélisés
    trajy.write(str(t2)+"\n")
    trajy.close()


def moyenne(t): #fonction qui calcule la moyenne de la longueur des lignes du tableau t, ici tableau des cyclones modélisés
    s = 0 #somme des longueurs des lignes
    for i in range(len(t)):
        s += len(t[i][1])
    s = floor(s/len(t)) #floor = partie entière car la longueur d'une liste est un entier
    return s #renvoie la moyenne de la longueur des lignes du tableau t


def longitude(t): #fonction qui calcule la longitude moyenne (= moyenne des abscisses) des cyclones modélisés
    mX=[]
    n = moyenne(t)
    for j in range(0,n): #on va effetuer le calcul des moyennes des abscisses sur la longueur moyenne des lignes
        s = 0 #somme des abscisses pour un indice j de liste fixé
        c = 0 #compteur du nombre de listes ayant une longueur strictement supérieur à j
        for i in range(0,len(t)): #prend en compte tous les cyclones
            if j < len(t[i][1]): #il faut que l'indice j soit présent dans la liste
                s +=t[i][1][j]
                c += 1
        mX.append(round((s/c),1)) #on arrondi à une décimale la moyenne des abscisses associé à l'indice j pour correspondre avec les autres valeurs qui ont seulement un seul chiffre après la virgule
    trajx = open("trajectoires x","a")
    trajx.write(str(mX)+"\n") #on ajoute la liste des abscisses de la meilleure trajectoire au fichier contenant toutes la liste des abscisses de tous les cyclones
    trajx.close()
    mt = open("trajectoire moyenne","a") #ouvre le fichier meilleure trajectoire
    mt.write("X:"+str(mX)+"\n") #on ajoute la liste des abscisses de la meilleure trajectoire au fichier "meilleure trajectoire"
    mt.close()
    return mX #renvoie le tableau contenant les listes des abscisses de tous les cyclones (meilleure trajectoire comprise)


def latitude(t): #fonction qui calcule la latitude moyenne (= moyenne des ordonnées) des cyclones modélisés, note idem fonction longitude en remplaçant abscisses par ordonnées et longitude par latitude
    mY=[]
    n = moyenne(t)
    for j in range(0,n):
        s,c = 0,0
        for i in range(0,len(t)):
            if j < len(t[i][2]):
                s += t[i][2][j]
                c += 1
        mY.append(round((s/c),1))
    trajy = open("trajectoires y","a")
    trajy.write(str(mY)+"\n")
    trajy.close()
    mt = open("trajectoire moyenne","a")
    mt.write("Y:"+str(mY)+"\n")
    mt.close()
    return mY #renvoie le tableau contenant les listes des ordonnées de tous les cyclones (meilleure trajectoire comprise)


X = liste_moins(longitude(traj)) #tableau contenant les listes des abscisses de tous les cyclones (meilleure trajectoire comprise)
Y = latitude(traj) #tableau contenant les listes des ordonnées de tous les cyclones (meilleure trajectoire comprise)

plt.plot(X,Y,'-',linewidth=2,label="trajectoire moyenne",color="k")


plt.plot(-traj[0][1][0],traj[0][2][0],marker="o",color="black",markersize=3) #point de départ

plt.legend(prop={'size':5},loc = 2) #légende avec taille lettres et position

plt.title('Trajectoires des cyclones')

ax.set_aspect('equal')

plt.show()