import sqlite3
import re

# These two SQLite3-specific commands let the user execute SQL commands through Python
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

# This deletes the pre-existing table so that we recreate a new Counts table
# else we run into an error
cur.execute('''
DROP TABLE IF EXISTS Counts''')

cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

fname = input('Enter file name: ')
if (len(fname) < 1): fname = 'mbox-short.txt'
fh = open(fname)

# This for loop scans each line in the email log for email transactions
# and extracts domain names through regular expression
for line in fh:
    if not line.startswith('From: '): continue
    pieces = line.split()
    piece = re.search('(?:@).+', pieces[1])
    org = piece.group()[1:]
    
    # This SQL command queries to see if that domain name exists 
    # and stores that count into memory
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (org,))
    row = cur.fetchone()
    
    # If there is no count, then we create a new domain in the table
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count)
                VALUES (?, 1)''', (org,))
                
    # Else, we increase the count by 1
    else:
        cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ?',
                    (org,))
    
conn.commit()

# https://www.sqlite.org/lang_select.html
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 5'

# This just shows you the list of all domains and their counts
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
