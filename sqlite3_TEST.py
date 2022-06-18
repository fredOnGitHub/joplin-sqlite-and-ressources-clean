import sqlite3
from pathlib import Path
import os

def Clean():
    os.system('cls' if os.name == 'nt' else 'clear')

def creer_BDD(nomBDD):
    try:
        print('\ncreer_BDD')
        conn=sqlite3.connect(nomBDD)
        cur=conn.cursor()
        print("Connexion réussie à SQLite")
        req='create table students(id integer primary key autoincrement,nom text,email text, age float)'
        cur.execute(req)
        conn.commit()
        cur.close()
        conn.close()
        print("Connexion SQLite est fermée")
    except sqlite3.Error as error:
        print("Erreur lors de la création de la table : ", error)


def insert_dans_BDD(nomBDD):
    try:
        print('\ninsert_dans_BDD')
        conn=sqlite3.connect(nomBDD)#crée si n'existe pas
        cur=conn.cursor()
        print("Connexion réussie à SQLite")
        req="insert into students(nom,email,age) values ('Alb ert','*****@g**ail.com','18.25')"
        cur.execute(req)
        print(cur.rowcount,"lignes insérée(s)")
        conn.commit()
        cur.close()
        conn.close()
        print("Connexion SQLite est fermée")
    except sqlite3.Error as error:
        print("Erreur lors de l'insertion dans la table : ", error)

def select_depuis_BDD(nomBDD):
    try:
        print('\nselect_depuis_BDD')
        conn=sqlite3.connect(nomBDD)
        cur=conn.cursor()
        print("Connexion réussie à SQLite")
        req='select * from students'
        result = cur.execute(req)
        print(len(cur.fetchall()),"ligne(s) trouvée(s)")
        # https://stackoverflow.com/questions/839069/cursor-rowcount-always-1-in-sqlite3-in-python3k
        result = cur.execute(req)
        for row in result:
            print(row)
        cur.close()
        conn.close()
        print("Connexion SQLite est fermée")
    except sqlite3.Error as error:
        print("Erreur lors de la sélection dans la table : ", error)

def delect_depuis_BDD(nomBDD):
# https://waytolearnx.com/2020/06/delete-supprimer-des-donnees-en-sqlite-avec-python.html
    try:
        print('\ndelect_depuis_BDD')
        conn=sqlite3.connect(nomBDD)
        cur=conn.cursor()
        print("Connexion réussie à SQLite")
        req="delete from students where nom=?"
        nom='Alb ert'
        cur.execute(req, (nom, ))
        # https://stackoverflow.com/questions/28978931/python-retrieve-number-of-rows-affected-with-sql-delete-query
        print(cur.rowcount,"suppression(s) en attente")
        conn.commit()
        print("commit : Enregistrement(s) supprimé(s) avec succès")
        cur.close()
        conn.close()
        print("Connexion SQLite est fermée")
    except sqlite3.Error as error:
        print("Erreur lors du suppression dans la table :", error)

Clean()
nomBDD="test.sqlite"
creer_BDD(nomBDD)
insert_dans_BDD(nomBDD)
insert_dans_BDD(nomBDD)
select_depuis_BDD(nomBDD)
delect_depuis_BDD(nomBDD)
# delect_depuis_BDD("nomBDD")
select_depuis_BDD(nomBDD)

# Recherche "sqlite acces langage python"
# https://sqlitebrowser.org/dl/

# TEST de
# https://www.youtube.com/watch?v=jXEf84OlU6A&list=PLh-rUZWaw76E5040FjSqUn-i3a6MFxn6e&index=5 #Connexion Python avec SQLite3 et Insertion des données
# https://www.youtube.com/watch?v=uYpW-2BMMU8&list=PLh-rUZWaw76E5040FjSqUn-i3a6MFxn6e&index=6 #Insertion des données de variables dans une table SQLite3 avec Python