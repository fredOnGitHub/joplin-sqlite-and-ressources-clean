# joplin-sqlite-and-ressources-clean

Be sure to stop completely joplin from taskbar (Windows)...

After You would like to run "joplin-sqlite-and-ressources-clean.py" to 

- move ghost references from resources Joplin's directory (.png, .pdf,...) 


You can see more info about sqlite and other implementation :

See https://www.youtube.com/watch?v=jXEf84OlU6A about tuto

and  https://sqlitebrowser.org/dl/ to watch into the tables

All is in database.sqlite

See https://github.com/tessus/joplin-scripts/blob/master/jnrmor about joplin access DB

<pre>
...
sqlite3 $DB "select resource_id from note_resources where is_associated = 0 and resource_id 
not in (select resource_id from note_resources where is_associated = 1) 
group by resource_id having max(last_seen_time) 
< strftime('%s','now','-${KEEP} days')*1000" >$TMPFILE
...
</pre>
