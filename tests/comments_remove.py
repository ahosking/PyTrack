from pytrack import pytrack
import creds #This is providing the information for the original connection

p = pytrack(creds.url, creds.port, creds.user, creds.password)
p.comments_remove("PTD-1", "89-20", True)

p.comments_remove("PTD-1", ["89-18", "89-19"])

p.comments_remove("PTD-1", ["89-9", "89-10", "89-11", "89-12", "89-13", "89-14", "89-15", "89-16"])