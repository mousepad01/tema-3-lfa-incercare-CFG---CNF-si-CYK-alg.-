import copy


def dfs1(node):

    global lv, viz, stack

    viz.add(node)

    if node in lv:
        for i in range(len(lv[node])):
            if lv[node][i] not in viz:

                dfs1(lv[node][i])

    stack.append(node)


def dfs2(node, key):

    global lvn, viz, cct

    viz.add(node)

    cct[key].append(node)

    if node in lvn:
        for i in range(len(lvn[node])):
            if lvn[node][i] not in viz:

                dfs2(lvn[node][i], key)


d = {}      # dictionar de forma : simbol de start ->  [prod1, prod2, ....]
            # conventie: in input, voi avea simbolul de start tot timpul S

r = set()     # nonterminale

nr = int(input())

l = input().split()

for i in range(nr):
    r.add(l[i])

n = int(input())

for i in range(n):
    l = input().split()         # intre oricare doua simboluri se va adauga un spatiu ex: aSb va fi dat a S b

    lprod = []

    for prod in l[1:]:
        lprod.append(" ".join(e for e in prod))

    if l[0] in d.keys():
        d[l[0]].extend(lprod)
    else:
        d.update({l[0]: lprod})

print(d)

# elimin productiile de forma X -> X

for st in list(d):

    i = 0
    while i < len(d[st]):

        if d[st][i] == st:
            d[st][i] = d[st][:i] + d[st][i + 1:]
            i -= 1

        i += 1

# pentru fiecare terminal x, il voi inlocui cu un nonterminal Ux, si voi adauga regula Ux -> x

for st in list(d):
    for i in range(len(d[st])):

        aux = d[st][i].split()

        for j in range(len(aux)):

            if aux[j] not in r and aux[j] != "λ":

                aux[j] = "U" + aux[j]

                if aux[j] not in d.keys():

                    d.update({aux[j]: [aux[j][1:]]})

                    r.add(aux[j])

        d[st][i] = " ".join(aux)

print(d)

# inlocuiesc fiecare regula de tipul U -> W1 W2 W3 .... cu U -> W1 X2 , X2 -> W2 X3, ....

cntX = 0

for st in list(d):
    for i in range(len(d[st])):

        aux = d[st][i].split()

        if len(aux) > 1:    # exclud cazurile de tip nonterminal -> terminal

            d[st][i] = aux[0] + " X" + str(cntX)

            r.add("X" + str(cntX))

            aux = aux[1:]

            cntX += 1

            while len(aux) > 2:

                d.update({"X" + str(cntX - 1): [aux[0] + " X" + str(cntX)]})

                r.add("X" + str(cntX))

                aux = aux[1:]

                cntX += 1

            d.update({"X" + str(cntX - 1): [" ".join(aux)]})

print(d)

# inlocuiesc toate S cu S' si adaug S -> S0

for st in list(d):
    for i in range(len(d[st])):

        aux = d[st][i].split()

        for j in range(len(aux)):

            if aux[j] == "S":

                aux[j] = "S0"

        d[st][i] = " ".join(aux)

for st in list(d):

    aux = st.split()

    for i in range(len(aux)):
        if aux[i] == "S":
            aux[i] = "S0"

    d[" ".join(aux)] = d.pop(st)

d.update({"S": ["S0"]})
r.add("S0")

print(d)

# elimin regulile de tipul A -> λ

# mai intain caut nonterminalele care pot genera λ in una sau mai multe miscari

daux = copy.deepcopy(d)

to_remove = set()

test = False

while not test:

    test = True

    for st in list(daux):
        for i in range(len(daux[st])):

            if daux[st][i] == "λ":
                to_remove.add(st)
                test = False

    for rem in to_remove:
        if rem in daux.keys():
            daux.pop(rem)

    for st in list(daux):
        for i in range(len(daux[st])):

            aux = daux[st][i].split()

            j = 0
            while j < len(aux):

                if aux[j] in to_remove:
                    aux = aux[:j] + aux[j + 1:]
                    j -= 1

                j += 1

            if len(aux) == 0:
                aux = "λ"

            daux[st][i] = " ".join(aux)

# elimin toate regulile de forma A -> λ cu ajutorul to_remove

for st in list(d):
    for i in range(len(d[st])):

        aux = d[st][i].split()

        if len(aux) == 2:

            if aux[0] != "S" and aux[0] in to_remove:
                d[st].append(aux[1])
            elif aux[1] != "S" and aux[1] in to_remove:
                d[st].append(aux[0])

to_del = set()

for st in list(d):

    if st != "S":

        if len(d[st]) == 1 and d[st][0] == "λ":

            d.pop(st)
            to_del.add(st)
        else:
            i = 0
            while i < len(d[st]):

                if d[st][i] == "λ":
                    d[st] = d[st][:i] + d[st][i + 1:]

                i += 1

            if len(d[st]) == 0:
                d.pop(st)
                to_del.add(st)

print(d)

t = False

while not t:

    t = True

    for st in list(d):

        i = 0
        while i < len(d[st]):

            aux = d[st][i].split()

            j = 0
            while j < len(aux):

                if aux[j] in to_del:
                    aux = aux[:j] + aux[j + 1:]
                    j -= 1

                j += 1

            if len(aux) == 0:
                d[st] = d[st][:i] + d[st][i + 1:]
                i -= 1
            else:
                d[st][i] = " ".join(aux)

            i += 1

        if len(d[st]) == 0:

            d.pop(st)
            to_del.add(st)

            t = False

if "S" in to_remove:
    d["S"].append("λ")

# elimin posibilele productii duplicate care au aelasi nonterminal de plecare, aparute in urma ultmilor pasi executati

for st in list(d):

    i = 0
    while i < len(d[st]) - 1:

        j = i + 1
        while j < len(d[st]):

            if d[st][i] == d[st][j]:
                d[st] = d[st][:j] + d[st][j + 1:]
                j -= 1

            j += 1

        i += 1

print(d)

# elimin productiile unitare

# caut componentele tari conexe ale grafului format pe baza productiilor A -> B

lv = {}
lvn = {}

viz = set()

stack = []

for st in list(d):
    for i in range(len(d[st])):

        if d[st][i] in r:

            if st in lv:
                lv[st].append(d[st][i])
            else:
                lv.update({st: [d[st][i]]})

            if d[st][i] in lvn:
                lvn[d[st][i]].append(st)
            else:
                lvn.update({d[st][i]: [st]})

#print(lv)
#print(lvn)

for key in list(lv):
    if key not in viz:
        dfs1(key)

#print(viz)
#print(stack)

viz = set()

cct = {}

for key in stack[::-1]:
    if key not in viz:

        cct.update({key: []})
        dfs2(key, key)

print(cct)

for key in list(cct):
    for i in range(len(cct[key])):

        for st in list(d):
            for j in range(len(d[st])):

                aux = d[st][j].split()

                for z in range(len(aux)):

                    if aux[z] == cct[key][i]:
                        aux[z] = key

                d[st][j] = " ".join(aux)

print(d)

for key in list(cct):
    for i in range(1, len(cct[key])):

        for st in list(d):

            if st == cct[key][i]:
                d[key].extend(d[st])
                d.pop(st)

for key in list(cct):
    for i in range(1, len(cct[key])):
        r.remove(cct[key][i])

# elimin posibilele productii duplicate care au aelasi nonterminal de plecare, aparute in urma ultmilor pasi executati

for st in list(d):

    i = 0
    while i < len(d[st]) - 1:

        j = i + 1
        while j < len(d[st]):

            if d[st][i] == d[st][j]:
                d[st] = d[st][:j] + d[st][j + 1:]
                j -= 1

            j += 1

        i += 1

print(d)

# elimin productiile de forma X -> X

for st in list(d):

    i = 0
    while i < len(d[st]):

        if d[st][i] == st:
            d[st] = d[st][:i] + d[st][i + 1:]
            i -= 1

        i += 1

print(d)
print(r)
# pas final pentru eliminat productiile unitare

t = False

while not t:

    t = True

    for st in list(d):
        for i in range(len(d[st])):

            if d[st][i] in r:
                d[st] = d[st][:i] + d[d[st][i]] + d[st][i + 1:]

                t = False

print(d)


# in d am acum gramatica in forma normala Chomsky
# aplic algoritmul CYK (implementare bazata pe sursa din WIKIPEDIA)

a = input()     # cuvantul de citit
a = " " + a
n = len(a) - 1

R = []      # nonterminale, cu elementul de start pe prima pozitie
nr = 0      # numarul de nonterminale

iR = {}     # dictionar Ri : i

for nt in r:
    if nt == "S":

        nr = 1
        R.append(nt)

        iR.update({nt: 1})

for nt in r:
    if nt != "S":
        nr += 1
        R.append(nt)

        iR.update({nt: nr})

P = [[[False for i in range(nr + 1)] for j in range(n + 1)] for k in range(n + 1)]

# executarea algoritmului

for s in range(1, n + 1):

    for st in list(d):
        for rr in d[st]:
            if rr == a[s]:
                P[1][s][iR[st]] = True

for l in range(2, n + 1):
    for s in range(1, n - l + 2):
        for p in range(1, l):

            for st in list(d):
                for rr in d[st]:

                    aux = rr.split()
                    if len(aux) == 2:

                        if P[p][s][iR[aux[0]]] and P[l - p][s + p][iR[aux[1]]]:
                            P[l][s][iR[st]] = True

if P[n][1][1]:
    print("CUVANTUL ESTE GENERAT DE GRAMATICA")
else:
    print("CUVANTUL NU ESTE GENERAT DE GRAMATICA")







