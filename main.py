from randtree import randSequent
import maude


CALCULUS = "IPL"
SIZE = 20

maude.init()
maude.load(f"{CALCULUS}.maude")
m = maude.getModule(CALCULUS)

target = m.parseTerm("True")

for _ in range(10):
    sequent = randSequent(SIZE)
    term = m.parseTerm(str(sequent))
    for _ in term.search(2, target):
        print(sequent)


