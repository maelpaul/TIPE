from math import *
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patches as mpatches #pour la légende en fonctions des couleurs


#cartopy
latitude_min=0
latitude_max=60
longitude_min=-110
longitude_max=0

ax = plt.axes(projection=ccrs.PlateCarree(),autoscale_on=False,xlim=(longitude_min,longitude_max),ylim=(latitude_min,latitude_max))


#quadrillage
for i in range(10,60,10):
    plt.plot([-110,0],[i,i],'-',color='grey',linewidth=0.8)

for j in range(10,110,10):
    plt.plot([-j,-j],[0,60],'-',color='grey',linewidth=0.8)


def liste_moins(L): #applique un x(-1) à tous les éléments de la liste
    M=[]
    for i in range(len(L)):
        M.append(-L[i])
    return M


def poly_L(L,M): #interpolation de Lagrange, L: liste des abscisses, M: liste des ordonnées
    n = len(L)
    s = 0 #somme des produits multipliés par les ordonnées
    X = np.poly1d([1,0]) #polynôme égal à 1X+0=X
    for j in range(0,n): #réalise la somme
        a = 1
        for i in range(0,n): #réalise le produit pour i =/= j
            if i != j:
                a *= (X-L[i])/(L[j]-L[i])
        s += M[j]*a
    return s #retourne le polynôme de Lagrange


trajx = open("trajectoires x","r") #ouvre le fichier contenant la liste des abscisses de tous les cyclones modélisés
tx = trajx.readlines() #tableau contenant les listes des abscisses de tous les cyclones
trajx.close()


trajy = open("trajectoires y","r") #ouvre le fichier contenant la liste des ordonnées de tous les cyclones modélisés
ty = trajy.readlines() #tableau contenant les listes des ordonnées de tous les cyclones
trajy.close()


a = int(input("Numéro trajectoire (0 pour la trajectoire moyenne, le numéro de la trajectoire voulue sinon) : ")) #numéro de la trajectoire dont on veut connaître l'erreur (0 pour la trajectoire moyenne, n° de la trajectoire modélisée pour les autres)
X=[]
Y=[]
if a == 0:
    nom = 'trajectoire moyenne' #nom du cyclone
    X = liste_moins(eval(tx[len(tx)-1])) #liste des abscisses du cyclone
    Y = eval(ty[len(ty)-1]) #liste des ordonnées du cyclone
else:
    nom = 'trajectoire '+str(a) #nom du cyclone
    X = liste_moins(eval(tx[a-1])) #liste des abscisses du cyclone
    Y = eval(ty[a-1]) #liste des ordonnées du cyclone


L = [0,12,24,36,48,72,96,120] #abscisses : pris par rapport au graphe de la NHC (National Hurricane Center), en heures
M1 = [0,25,40,55,70,100,140,190] #ordonnées : pris par rapport au graphe de la NHC (National Hurricane Center), en miles
P1 = poly_L(L,M1) #calcul du polynôme de Lagrange modélisant la fonction du graphe (entre 2010 et 2019)
M2 = [0,45,90,145,205,320,415,480] #valeurs pour CLIPER5
P2 = poly_L(L,M2)


for i in range(len(X)-1,-1,-1): #dégressif car pour i grand, erreur grande -> permet de voir l'erreur pour les petits i
    if i <= 20: #en dessous de 20, respect du graphe
        r = (P2(6*i)*1.852*180)/(6371*np.pi) #6xi car entre chaque position il y 6 heures d'intervalles (en accord avec la base du NHC) x 1.852 pour la conversion miles vers km x (180/(6371*pi)) pour la conversion en ° (6371 km = rayon de la Terre)
        circle1 = plt.Circle((X[i], Y[i]), r, color='r')
        ax.add_artist(circle1)


for i in range(len(X)-1,-1,-1): #dégressif car pour i grand, erreur grande -> permet de voir l'erreur pour les petits i
    if i <= 20: #en dessous de 20, respect du graphe
        r = (P1(6*i)*1.852*180)/(6371*np.pi) #6xi car entre chaque position il y 6 heures d'intervalles (en accord avec la base du NHC) x 1.852 pour la conversion miles vers km x (180/(6371*pi)) pour la conversion en ° (6371 km = rayon de la Terre)
        circle1 = plt.Circle((X[i], Y[i]), r, color='b')
        ax.add_artist(circle1)


ax.add_feature(cfeature.BORDERS)
ax.add_feature(cfeature.COASTLINE)


if a == 0:
    X1 = []
    Y1 = []
    for i in range(len(tx)-1): #trace les autres trajectoires
        X1 = liste_moins(eval(tx[i]))
        Y1 = eval(ty[i])
        plt.plot(X1,Y1,'-',linewidth=2,color="grey")
    plt.plot(X,Y,'-',linewidth=2,label="trajectoire moyenne",color="k") #trace la meilleure trajectoire
else:
    X1 = []
    Y1 = []
    for i in range(len(tx)-1): #trace les autres trajectoires
        if i != a-1:
            X1 = liste_moins(eval(tx[i]))
            Y1 = eval(ty[i])
            plt.plot(X1,Y1,'-',linewidth=2,color="grey")
    X2 = liste_moins(eval(tx[len(tx)-1]))
    Y2 = eval(ty[len(ty)-1])
    plt.plot(X2,Y2,'-',linewidth=2,label="trajectoire moyenne",color="maroon") #trace la meilleure trajectoire, permet d'avoir la trajectoire moyenne en couleur
    plt.plot(X,Y,'-',linewidth=2,label="trajectoire "+str(a),color="k") #trace la trajectoire n°a


if len(X) >= 21:
    for i in range(21):
        plt.plot(X[i],Y[i],marker="x",color="y",markersize=3)
else:
    for i in range(len(X)):
        plt.plot(X[i],Y[i],marker="x",color="y",markersize=3)


#définition de la légende
a = mpatches.Patch(color='b', label='NHC Official')
b = mpatches.Patch(color='r', label='CLIPER5')

plt.plot(X[0],Y[0],marker="o",color="black",markersize=3) #point de départ

plt.legend(handles=[a,b],prop={'size':5},loc = 2) #légende spécifique définie au dessus avec taille lettres et position

plt.title('Erreur '+nom)

ax.set_aspect('equal')

plt.show()