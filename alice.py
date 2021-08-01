N = 13

def group(n, deck):
    while deck:
        chunk, deck = deck[:n], deck[n:]
        yield chunk

def swap(l, a, b): l[a], l[b] = l[b], l[a]

def function(number):
    deck = []
    for part in group(N, list(range(52))):
        n = number
        for i in range(N):
            j = n % (N - i)
            n = (n - j) // (N - i)
            swap(part, i, i+j)
        deck += part

    return deck
