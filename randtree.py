import random


# credit to Arnold & Sleep "Uniform Random Generation of Balanced Parenthesis Strings"
def randParens(n:int):
    running = ""
    k = 2*n
    r = 0
    while r != k:
        probClose = (r*(r+k+2))/(2*k*(r+1))
        if random.random() < probClose:
            # close
            running += ")"
            r -= 1
            k -= 1
        else:
            # open
            running += "("
            r += 1
            k -= 1
    return running + (")"*k)

class Formula:

    def __init__(self, conn, args):
        self.conn = conn
        self.args = args

    def __str__(self):
        if self.conn == "VAR":
            return "p"
        return f"({self.args[0]} {self.conn} {self.args[1]})"

CONNS = ["->","<-","*"]

# credit to me, not ChatGPT
def parens2formula(parens, sequent=False):
    if parens == "":
        return Formula("VAR",[])

    i = 0
    balance = 0
    while balance != 0 or i == 0:
        balance += 1 if parens[i] == "(" else -1
        i += 1
    left = parens2formula(parens[1:i-1])
    right = parens2formula(parens[i:])

    conn = "=>" if sequent else random.choice(CONNS)
    return Formula(conn,[left,right])

def randSequent(n):
    return parens2formula(randParens(n-1), sequent=True)