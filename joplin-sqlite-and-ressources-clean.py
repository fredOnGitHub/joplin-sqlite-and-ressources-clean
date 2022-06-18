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
    print()
    req='delete from note_resources where is_associated = 0'
    print(req)
    cur.execute(req)
    print(cur.rowcount,"delete(s) before commiting")
    conn.commit()
    print('done')

def count(req):
    # result=cur.execute(req)
    # rows = result.fetchall()
    # print(type(rows))
    # tuple_=rows[0]
    # nb=tuple_[0]
    # print(nb)
    print()
    print(req)
    nb=cur.execute(req).fetchall()[0][0]
    print(nb)
    return nb

def print_req_result(req):
    print()
    print(req)
    result=cur.execute(req)
    print(len(cur.fetchall()),"ligne(s) trouvée(s)")
    result=cur.execute(req)#re-faire
    for row in result:
        print(row[0])

Clean()
database_sqlite=Path(Path.home(), '.config', 'joplin-desktop', 'database.sqlite')
conn=sqlite3.connect(database_sqlite)
cur=conn.cursor()
count('select count(*) from note_resources')
count('select count(*) from note_resources where is_associated = 1')
count('select count(distinct resource_id) from note_resources where is_associated = 1')
count('select count(*) from note_resources where is_associated = 0')

# delete_in_BDD(cur)#joplin re-create always the deleted "is_associated = 0"

print()
# exit(0)
# tous les fichiers du rép 'ressources'
R=[]
path_resources=Path(Path.home(), '.config', 'joplin-desktop', 'resources')
for (repertoire, sousRepertoires, fichiers) in os.walk(path_resources):
    if len(fichiers):
        for i in fichiers:
            R.append(i)
nb5=len(R)
print('Number of elements in "%s" directory'%(path_resources))
print('%d'%(nb5))
print()


setBDD=set()
# print(type(setRessources))
req='select distinct resource_id from note_resources where is_associated = 1'
print(req)
result=cur.execute(req)
for row in result:
    setBDD.add(row[0])
print(len(setBDD),'distinct elements in set')
print()
# print(setBDD)
# exit(0)

# exit(0)


# # TEST SET
# r=set(['41d1570bbd244038a5f3858e3e855e12']).intersection(setBDD)
# print(r)
# r=setBDD.intersection(set(['41d1570bbd244038a5f3858e3e855e12']))
# print(r)
# if not r:
    # print('non')
# if not set([]):
    # print('empty')
# exit(0)


joplin_moved=Path(Path.home(), '.config', 'joplin-desktop', 'joplin-moved')
if os.path.exists(joplin_moved):
    print(joplin_moved,'exists')
else:
    os.mkdir(joplin_moved)
    print(joplin_moved,'created')


founded=0
notFounded=0
for ri in R:
    # print(os.path.splitext(ri))
    ri_split =os.path.splitext(ri)[0]
    set_i = set([ri_split])
    if not set_i.intersection(setBDD):
        notFounded+=1

        fsrc=Path(path_resources,ri)
        fdest=Path(joplin_moved,ri)

        if os.path.exists(fdest):
            print(fdest,'exists')
        else:
            print(fsrc, '->', fdest)
            os.rename(fsrc, fdest)

        # com='Remove-Item -Confirm "%s"'%(fsrc)
        # print(com)
        # subprocess.run(["powershell", "-Command", com])#,capture_output=True
    # if set_i.intersection(setBDD):
    else:
        founded+=1
print()
print('founded : ', founded)
print('notFounded and moved : ', notFounded)
print()

cur.close()
conn.close()
