#!/usr/bin/env python3.9
from base64 import b64decode
from json import loads, dumps
from socket import socketpair
from struct import unpack, pack
from os import fork, kill
from seccomp import SyscallFilter, ALLOW, KILL, Arg, EQ
from random import SystemRandom

randint = SystemRandom().randint

ROUNDS = 1000

# Utility functions for communication 
def readn(sock, n):
    buf = b""
    while len(buf) < n:
        data = sock.recv(n - len(buf))
        if not data: exit(0)
        buf += data
    return buf

def recv_message(sock):
    size = unpack("!H", readn(sock, 2))[0]
    return loads(readn(sock, size).decode())

def send_message(sock, msg):
    msg = dumps(msg).encode()
    sock.sendall(pack("!H", len(msg)) + msg)
    
# Sandbox the program
def sandbox(program):
    local, remote = socketpair()
    pid = fork()
    if pid == 0:
        local.close()

        # Escapeing this is not a part of the challenge.
        # But feel free to try. Good luck.
        f = SyscallFilter(defaction=KILL)
        f.add_rule(ALLOW, "rt_sigaction")
        f.add_rule(ALLOW, "rt_sigreturn")
        f.add_rule(ALLOW, "exit_group")
        f.add_rule(ALLOW, "mmap")
        f.add_rule(ALLOW, "brk")
        f.add_rule(ALLOW, "recvfrom", Arg(0, EQ, remote.fileno()))
        f.add_rule(ALLOW, "sendto", Arg(0, EQ, remote.fileno()))
        f.load()

        exec(program, globals())

        while True:
            args = recv_message(remote)
            resp = function(*args)
            send_message(remote, resp)

        exit(0)

    remote.close()

    def func(*msg):
        send_message(local, msg)
        return recv_message(local)

    return (pid, func)

# https://www.youtube.com/watch?v=vUcQu3t1KCE
def riffle_shuffle(deck):
    lower_half, upper_half = deck[:26], deck[26:]
    deck = []
    while lower_half or upper_half:
        half = upper_half if randint(0, 1) else lower_half
        if half: deck.append(half.pop(0))
    return deck
    
def challenge():
    alice_pid, alice = sandbox(b64decode(input("Alice>")))
    bob_pid, bob = sandbox(b64decode(input("Bob>")))

    for r in range(ROUNDS):
        n = randint(0, (2**32)-1)
        deck = alice(n)
        assert len(deck) == 52
        assert all(card in deck for card in range(52))
        deck = riffle_shuffle(deck)
        deck = riffle_shuffle(deck)
        assert n == bob(deck)

    kill(alice_pid, 9)
    kill(bob_pid, 9)

    print(open("flag.txt", "r").read().strip())

if __name__ == "__main__": challenge()
