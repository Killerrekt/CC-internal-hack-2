import imaplib
import email
import os
from dotenv import load_dotenv
import mysql.connector

server = "imap.gmail.com"
load_dotenv()
address = os.environ['ADDRESS']
password = os.environ['PASS']

imap = imaplib.IMAP4_SSL(server)
imap.login(address,password)

imap.select('Inbox')

dummy,msg = imap.search(None,"SUBJECT 'transfer","ALL")
print(msg)

con = mysql.connector.connect(host="localhost",password="140604",user="root",charset="utf8")
cur = con.cursor()
cur.execute("create database if not exists clubs")
cur.execute("use clubs")
cur.execute("create table if not exists transfer(subject varchar(255))")

t = 0
cur.execute("delete from transfer")
for message in msg[0].split()[::-1]:
    if(t>9):
        break
    dummy,data = imap.fetch(message,'(RFC822)')
    m = email.message_from_bytes(data[0][1])
    cur.execute("insert into transfer values ('"+m.get('Subject')+"!')")
    t+=1
con.commit()

cur.execute("create table if not exists internship(subject varchar(255))")

t = 0
cur.execute("delete from internship")

dummy,msg = imap.search(None,"TEXT 'Internship'","ALL")
print(msg)

t = 0
for message in msg[0].split()[::-1]:
    if(t>9):
        break
    dummy,data = imap.fetch(message,'(RFC822)')
    m = email.message_from_bytes(data[0][1])
    if ('Clubs' in m.get('Subject') or 'Newsletter' in  m.get('Subject')):
        continue
    cur.execute("insert into internship values (\""+m.get('Subject')+"?\")")
    t+=1
con.commit()
con.close()
