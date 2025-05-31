import bcrypt



szoveg = "Admin"

hashed = bcrypt.hashpw(szoveg.encode(), bcrypt.gensalt())
print(hashed)