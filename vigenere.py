
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def vigenere_encode(message, key):
    final = ""
    for i in range(0, len(message)):
        letter1 = message[i]
        index = i % len(key)
        int1 = alpha.index(letter1)
        int2 = alpha.index(key[index])
        int3 = (int1+int2)%26
        finaletter = alpha[int3]
        final += finaletter
    return final
        
def vigenere_decode(message, key):
    final = ""
    for i in range(0, len(message)):
        letter1 = message[i]
        index = i % len(key)
        int1 = alpha.index(letter1)
        int2 = alpha.index(key[index])
        int3 = (int1-int2)%26
        finaletter = alpha[int3]
        final += finaletter
    return final



pt = "SPHINXOFBLACKQUARTZJUDGEMYVOW"
key = "KEYWORD"
ct = vigenere_encode(pt, key)
dt = vigenere_decode(ct, key)
print(ct, dt)
