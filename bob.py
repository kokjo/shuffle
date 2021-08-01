def swap(l, a, b): l[a], l[b] = l[b], l[a]

def group_cards(deck):
    for i in range(52//N):
        part = [card for card in deck if card < (i+1)*N]
        deck = [card for card in deck if card not in part]
        min_card = min(part)
        part = [n - min_card for n in part]
        yield part
    
N = 13

def function(deck):
    ns = []
    for part in group_cards(deck):
        js = []
        for i in range(N):
            n = part[i]
            js.append(n-i)
            swap(part, part.index(i), i)

        n = 0
        for i, j in enumerate(js[::-1]):
            n = n * (i+1) + j
        ns.append(n)

    number = 0
    for n in ns:
        if ns.count(n) > ns.count(number):
            number = n

    return number
