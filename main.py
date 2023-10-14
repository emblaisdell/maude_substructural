from randtree import randSequent
import maude



CALCULI = ["IAMLL","IMLL","LCS","LC","NL"]
SIZE = 14
SAMPLES = 100000

PRINT_EVERY = 100


def main():

    maude.init()
    mods = {}
    target = {}
    numProvable = {"CPL":0}
    for calculus in CALCULI:
        maude.load(f"{calculus}.maude")
        mods[calculus] = maude.getModule(calculus)
        target[calculus] = mods[calculus].parseTerm("True")
        numProvable[calculus] = 0

    for i in range(SAMPLES+1):
        if i % PRINT_EVERY == 0:
            print("CHECKED",i,"SEQUENTS OF SIZE",SIZE,":")
            for calculus in ["CPL"] + CALCULI:
                print("\t",calculus,"|-",numProvable[calculus])
        sequent = randSequent(SIZE)
        if not evalFormula(sequent):
            continue
        numProvable["CPL"] += 1
        provableInIAMLL = False
        for calculus in CALCULI:
            m = mods[calculus]
            term = m.parseTerm(str(sequent))
            if calculus=="IPL" and provableInIAMLL:
                numProvable[calculus] += 1
                # print("SKIP")
                continue
            provable = False
            for _ in term.search(2, target[calculus], depth=SIZE*2):
                provable = True
                if calculus=="IAMLL":
                    provableInIAMLL = True
                # print(calculus,"|-",sequent)
                numProvable[calculus] += 1
                break
            if not provable:
                break

def evalFormula(form):
    return evalSub(form, True) and evalSub(form, False)
    
def evalSub(form, sub):
    if form.conn == "VAR":
        return sub
    if form.conn == "=>":
        return (not evalSub(form.args[0],sub)) or evalSub(form.args[1],sub)
    if form.conn == "->":
        return (not evalSub(form.args[0],sub)) or evalSub(form.args[1],sub)
    if form.conn == "<-":
        return evalSub(form.args[0],sub) or (not evalSub(form.args[1],sub))
    if form.conn == "->":
        return evalSub(form.args[0],sub) and evalSub(form.args[1],sub)

main()
