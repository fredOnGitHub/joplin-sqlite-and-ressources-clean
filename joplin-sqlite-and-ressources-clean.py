# Créer l'exécutable
# pyinstaller.exe --onefile .\joplin-sqlite-and-ressources-clean.py

import sqlite3
from pathlib import Path
import os
import re
from sys import exit
import subprocess

# exit('route %d %s' % (66,'66'))

def Clean():
    os.system('cls' if os.name == 'nt' else 'clear')

def delete_in_BDD(cur):
    print('delete in BDD...')
    req='''delete from note_resources where is_associated = 0 and resource_id 
    not in (select resource_id from note_resources where is_associated = 1)'''
    print(req)
    result=cur.execute(req)
    for row in result:
        print(row[0])
    
Clean()
f=Path(Path.home(), '.config', 'joplin-desktop', 'database.sqlite')
conn=sqlite3.connect(f)
cur=conn.cursor()

req='select count(*) from note_resources'
print(req)
# result=cur.execute(req)
# rows = result.fetchall()
# # print(type(rows))
# tuple_=rows[0]
# nb=tuple_[0]
# print(nb)

# class list -> tuple -> int 
nb=cur.execute(req).fetchall()[0][0]
print(nb)

print()
req='select count(*) from note_resources where is_associated = 1 and resource_id not in (select resource_id from note_resources where is_associated = 0)'
print(req)
nb3=cur.execute(req).fetchall()[0][0]
print(nb3)

print()
req='select count(*) from note_resources where is_associated = 0 and resource_id not in (select resource_id from note_resources where is_associated = 1)'
print(req)
nb4=cur.execute(req).fetchall()[0][0]
print(nb4)

print()
if nb == (nb3+nb4):
    print('%d == %d+%d => database.sqlite BDD is ok'%(nb, nb3,nb4)) 
else:
    exit('Fatal error 1')


print()
req='delete from note_resources where is_associated = 0 and resource_id not in (select resource_id from note_resources where is_associated = 1)'
print(req)
cur.execute(req)
print(cur.rowcount,"delete(s) before commiting")
conn.commit()
print('done')



print()
print('============================================')
print()

# vecteur de tous les fichiers du rép 'ressources'
R=[]
f=Path(Path.home(), '.config', 'joplin-desktop', 'resources')
for (repertoire, sousRepertoires, fichiers) in os.walk(f):
    if len(fichiers):
        for i in fichiers:
            R.append(i)
nb5=len(R)
print('Number of elements in "%s" directory'%(f))
print('%d'%(nb5),'elements in vector')

print()

disctRess=[]
req='''select distinct resource_id from note_resources where is_associated = 1 and resource_id 
not in (select resource_id from note_resources where is_associated = 0)'''
print(req)
result=cur.execute(req)
for row in result:
    disctRess.append(row[0])
print(len(disctRess),'elements in vector')


for s in R:
    trouve=False
    # print(os.path.splitext(s))
    l=os.path.splitext(s)[0]
    for m in disctRess:
        if l == m:
            trouve=True
            break
    if not trouve:
        # print(s,'not founded')
        src_i=Path(f, s)
        com='Remove-Item -Confirm "%s"'%(src_i)
        # print(com)
        subprocess.run(["powershell", "-Command", com])#,capture_output=True

cur.close()
conn.close()
