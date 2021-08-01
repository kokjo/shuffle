from pwn import *
from base64 import b64encode

#r = process("./challenge.py")
r = remote("0", 1337)
r.sendlineafter("Alice>", b64encode(read("alice.py")))
r.sendlineafter("Bob>", b64encode(read("bob.py")))
r.interactive()
print(r.readline().decode().strip())
