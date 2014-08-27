from os import urandom
import sys

# alfabeto ordenado segun frecuencias relativas en el idioma ingles
alphabet = {'E': 0,
            'T': 10,
            'A': 110,
            'O': 1110,
            'I': 11110,
            'N': 111110,
            'S': 1111110,
            'H': 11111110,
            'R': 111111110,
            'D': 1111111110,
            'L': 11111111110,
            'C': 111111111110,
            'U': 1111111111110,
            'M': 11111111111110,
            'W': 111111111111110,
            'F': 1111111111111110,
            'G': 11111111111111110,
            'Y': 111111111111111110,
            'P': 1111111111111111110,
            'B': 11111111111111111110,
            'V': 111111111111111111110,
            'K': 1111111111111111111110,
            'J': 11111111111111111111110,
            'X': 111111111111111111111110,
            'Q': 1111111111111111111111110,
            'Z': 11111111111111111111111110 }

def generateBitStream(n):    
    byts = urandom(n)
    bits = ""
    count = 0
    for i in bytearray(byts):
        byte = bin(i)[2:]
        if len(byte) < 8:
            zeros = ""
            dif = 8 - len(byte) 
            for j in xrange(dif):
                zeros += '0'
            byte = zeros + byte
        bits += byte
    return bits

def writeKeys(k, n):
    alice = open('alicekeys', 'w')
    bob = open('bobkeys', 'w')
    key = ""
    for i in xrange(k):
        key = generateBitStream(n)+'\n'
        alice.write(key)
        bob.write(key)    
    alice.close()
    bob.close()

def plaintextToBits(msg):
    p = msg.upper().replace(" ", "")
    bits = ""
    for i in p:
        if i in alphabet:
            bits += str(alphabet[i])        
    #print bits, len(bits)
    return bits

def encrypt(p, k):
    c = ""
    if len(p) > len(k):
        print 'Mensaje muy largo' 
        exit()
    for i in xrange(len(p)):        
        a = int(p[i])
        b = int(k[i])
        tmp = a^b
        c += str(tmp)
    return c

def decrypt(c, k):
    return encrypt(c, k)

def readKey(keyname):
    keyfile = open(keyname, 'r')
    key = keyfile.readline()
    lines = keyfile.readlines()
    keyfile = open(keyname, 'w')
    keyfile.writelines(lines[0:])
    keyfile.close()
    return key

def parseBits(bits):
    buffer = ""
    msg = ""
    for l in bits:  
        buffer += l
        if l is '0':
            msg += alphabet.keys()[list(alphabet.values()).index(int(buffer))]
            buffer = "" 
    return msg

def help():
    print """Argumentos para correr programa: \n
    -g k n        : genera k llaves de n bytes\n
    -a 'mensaje'  : envia 'mensaje' a Alice\n
    -b 'mensaje'  : envia 'mensaje' a Bob"""   

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        help()
        exit()
    if args[1] == '-g' and len(args)>3:
        writeKeys(int(args[2]), int(args[3]))

    elif args[1] == '-a':
        bkey = readKey("bobkeys")
        p = args[2]
        pbits = plaintextToBits(p)
        c = encrypt(pbits, bkey)
        print 'Bob envia ciphertext: ', c    
        akey = readKey("alicekeys")
        pd = decrypt(c, akey)
        msg = parseBits(pd)
        print 'Alice lee mensaje: ', msg
    elif args[1] == '-b':
        akey = readKey("alicekeys")
        p = args[2]
        pbits = plaintextToBits(p)
        c = encrypt(pbits, akey)
        print 'Alice envia ciphertext: ', c    
        bkey = readKey("bobkeys")
        pd = decrypt(c, bkey)
        msg = parseBits(pd)
        print 'Bob lee mensaje: ', msg


#Ejemplo:
# writekeys(3, 15)
#p = "ola k ase" 
#    pbits = plaintextToBits(p)
#    a = readKey("alicekeys")
#    b = readKey("bobkeys")

#    c = encrypt(pbits, a)    
#    pd = decrypt(c, b)
#    msg = parseBits(pd)
#    print msg
