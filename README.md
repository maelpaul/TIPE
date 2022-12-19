# Modèle de prévision des ouragans dans l'Atlantique Nord

Ce modèle s'appuie sur les données du NHC (National Hurricane Center).

Le package Python "Cartopy" doit être installé pour pouvoir exécuter le projet.

## Auteurs

- PAUL Maël
- LE BIHAN Yassin
- HOYAUX Pierre

## Exécuter le projet

Créer la base de données (la base de données est déjà présente dans le dépôt après avoir effectué "git clone"):  
    `python3 create.py`

Créer les fichiers nécessaires au projet (peut prendre jusqu'à 2min, les fichiers sont déjà présents dans le dépôt après avoir effectué "git clone"):  
    `python3 create_loc.py`

Exécuter les deux actions précédentes:  
    `make`

Tracer des trajectoires à partir d'une localisation initiale:  
    `python3 trace_des_trajectoires.py`

Visualiser la zone d'erreur pour une trajectoire:  
    `python3 erreur_trajectoire.py`

Clean les trajectoires:  
    `make clean`

Clean tous les fichiers nécessaires au projet:  
    `make cleanall`
