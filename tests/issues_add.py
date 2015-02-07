from pytrack import pytrack
import creds #This is providing the information for the original connection

p = pytrack(creds.url, creds.port, creds.user, creds.password)
p.issues_add("PTD", "First Automated Ticket", "This was hard to re-produce!")