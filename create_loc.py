from math import *


#longitude=CYCX ; latitude=CYCY


def traitement(t,n): #fonction récupérant les coordonnées pour un cyclone de la base de données (t) et la ligne de début du prochain cyclone (n)
    CX,NCX,CY = [],[],[]
    for i in range (n,len(t)):
        if t[i][0] == "A" : #correspond à un nouveau cyclone à traiter
            return CX,NCX,CY,i
        else:
            w=float(t[i][30]+t[i][31]+t[i][32]+t[i][33]+t[i][34]) #coordonnées ouest
            n=float(t[i][23]+t[i][24]+t[i][25]+t[i][26]) #coordonnées nord
            if 0.0 <= w < 110.0 and 0.0 <= n < 60.0: 
                CX.append(w) #ajoute la nouvelle coordonnée longitude au tableau (positive)
                NCX.append(-w) #ajoute la nouvelle coordonnée longitude au tableau (N = négative pour l'utilisation de cartopy)
                CY.append(n) #ajoute la nouvelle coordonnée latitude au tableau
    return CX,NCX,CY,i


base=open("base.txt","r") #ouvre le fichier txt contenant la base de données normalisée à exploiter
m=base.readlines() #crée un tableau contenant les lignes de la base en chaines de caractères
base.close()


cyclonex=open("coord_x.txt","w") #crée un fichier avec les listes des coordonnées x de tous les cyclones
cycloney=open("coord_y.txt","w") #crée un fichier avec les listes des coordonnées y de tous les cyclones

CYCX,CYCY=[],[]
c=1 #numéro ligne début cyclone
while c<len(m):
    a,x,y,c0 = traitement(m,c) #a <- CX ; x <- NCX ; y <- CY ; c0 <- i = ligne nom cyclone suivant
    cyclonex=open("coord_x.txt","a")
    cyclonex.write(str(a)+"\n")
    cyclonex.close()
    CYCX.append(a)
    cycloney=open("coord_y.txt","a")
    cycloney.write(str(y)+"\n")
    cycloney.close()
    CYCY.append(y)
    c=c0+1 #numéro ligne début cyclone suivant


l=[] #base des localisations
loc=open("localisation.txt","w") #crée un fichier avec la localisation de tous les cyclones


for i in range (len(CYCY)): #la=CYCY et lo=CYCX sont de longueur égale
    L1 = []
    for j in range (len(CYCY[i])):
        l1 = 110 * floor(CYCY[i][j]) + 1 #110 pour 110 degrés de longitude ; floor(float(a)) = partie entière de la latitude ; +1 pour la formule qui crée 6600 (110x60) cases numérotées de 1 à 6600
        L1.append(l1)
    L2 = []
    c = 0 #indice des éléments de L1
    for k in range (len(CYCX[i])):
        l2 = floor(CYCX[i][k]) + L1[c] #floor(float(b)) pour la longitude ; la formule crée le tableau de 6600 cases ; formule : localisation = 110 x floor(latitude) + floor(longitude) + 1
        L2.append(l2)
        c += 1
    loc=open("localisation.txt","a")
    loc.write(str(L2)+"\n")
    loc.close()
    l.append(L2)


bd1_storage=open("bd1_storage.txt","w") #crée un fichier pour stocker bd1
bd2_storage=open("bd2_storage.txt","w") #crée un fichier pour stocker bd1


for a in range(6601):
    L = [] #localisations
    for i in range (len(l)):
        for j in range (len(l[i])):
            if l[i][j] == a and len(l[i]) > j+1 :
                L.append(l[i][j+1])
            elif l[i][j] == a and j == len(l[i])-1 :
                L.append(0) #0 correspond à l'état mort (plus de cyclone)
            elif i == len(l)-1 and j == len(l[i])-1 and l[i][j] != a and L == [] :
                L.append(0)
    P = [] #probabilités de transition
    L.sort() #trie la liste L
    M = [] #liste L sans doublons
    c = 1 #compteur du nombre de répétitions d'une même localisation
    for i in range (len(L)):
        if i != len(L)-1 and L[i] != L[i+1] :
            P.append(c/len(L)) #c/len(L) = proba
            M.append(L[i])
            c = 1
        elif i == len(L)-1 :
            P.append(c/len(L))
            M.append(L[i])
        else:
            c = c+1
    bd1_storage=open("bd1_storage.txt","a")
    bd1_storage.write(str(M)+"\n")
    bd1_storage.close()
    bd2_storage=open("bd2_storage.txt","a")
    bd2_storage.write(str(P)+"\n")
    bd2_storage.close()
