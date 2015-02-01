from pytrack import pytrack
import creds #This is providing the information for the original connection

p = pytrack(creds.url, creds.port, creds.user, creds.password)
p.comments_remove("PTD-1", "89-20", True)

p.comments_remove("PTD-1", ["89-18", "89-19"], True)