import random, string

def GenRandomKey(length):
    rg = random.SystemRandom()
    alphabet = string.letters[0:52] + string.digits
    pw = str().join([rg.choice(alphabet) for i in range(length)])
    return pw
