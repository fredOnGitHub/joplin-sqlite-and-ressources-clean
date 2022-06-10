# Créer l'exécutable
# pyinstaller.exe --onefile .\joplin_sqlite.py

import sqlite3
from pathlib import Path
import os
import re

def Clean():
    os.system('cls' if os.name == 'nt' else 'clear')

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
    print('%d == %d+%d => all is ok'%(nb, nb3,nb4)) 
else:
    print('Fatal error')
    exit(0)

if nb4 == 0:
    exit(0)
print('======================')
print()
req='select count(DISTINCT resource_id) from note_resources'
print(req)
nb2=cur.execute(req).fetchall()[0][0]
print(nb2)


# on va créer un dictionnaire des ressources de Joplin
# qui contient les extensions de fichiers
print()
D={}
f=Path(Path.home(), '.config', 'joplin-desktop', 'resources')
for (repertoire, sousRepertoires, fichiers) in os.walk(f):
    if len(fichiers):
        for i in fichiers:
            D[i]=''
nb5=len(D)
print('Counting number of elements in "%s" directory'%(f))
print('%d'%(nb5))

print()
if nb5 == nb2:
    print('%d == %d => all is ok'%(nb5, nb2)) 
else:
    print('Fatal error')
    exit(0)

print()
req='''
select count(*) FROM 
(
select DISTINCT resource_id from note_resources where is_associated = 0 and resource_id 
not in (select resource_id from note_resources where is_associated = 1)
)'''
print(req)
nb6=cur.execute(req).fetchall()[0][0]
print(nb6)

print('======================')
print()
req='''
select DISTINCT resource_id from note_resources where is_associated = 0 and resource_id 
not in (select resource_id from note_resources where is_associated = 1)
'''
print(req)
R=[]
result=cur.execute(req)
for row in result:
    R.append(row[0])

# for a in R:
    # print(a)


to_delete=[]

for s in R:
    trouve=False
    # print(s)
    for c,v in D.items():
        r = re.search(s+'.*', c, re.IGNORECASE)
        if r:
            trouve = True
            break
    if not trouve:
        print('NON ok %d %s' % (ir,s))
        exit(0)
    if trouve:
        to_delete.append(c)
        
ir=1
# for s in to_delete:
    # print('%d %s' % (ir,c))
    # ir+=1

f=Path(Path.home(), 'COPY_RESSOURCES_JOPLIN')
print(f)
if not os.path.exists(f):
    os.makedirs(f)
    # os.mkdir(f)
else:
    print('exist')

import shutil

src=Path(Path.home(), '.config', 'joplin-desktop', 'resources')
for s in to_delete:
    src_i=Path(src, s)
    dest_i=Path(f, s)
    # https://stackoverflow.com/questions/123198/how-to-copy-files
    shutil.copy2(src_i,dest_i)
    # print('copy %s' % (src_i))
    # print('to %s' % (dest_i))


print('delete all unused files...')
import subprocess
# subprocess.run(["powershell", "-Command", "Write-Host 'Hello Wolrd!'"])#,capture_output=True
for s in to_delete:
    src_i=Path(src, s)
    # com='Remove-Item -Confirm \'%s\''%(src_i)
    com='Remove-Item "%s"'%(src_i)
    print(com)
    # Executing PowerShell from Python
    subprocess.run(["powershell", "-Command", com])#,capture_output=True

print('delete in BDD...')
req='''delete from note_resources where is_associated = 0 and resource_id 
not in (select resource_id from note_resources where is_associated = 1)'''
print(req)
result=cur.execute(req)

conn.close()
