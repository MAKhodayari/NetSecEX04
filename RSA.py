from math import sqrt
from numpy import gcd
from time import time


def PrimalityCheck(Num):
    Num = int(Num)
    Sqr = int(sqrt(Num)) + 1
    if Num <= 2:
        return False
    else:
        for i in range(3, Sqr):
            if Num % i == 0:
                return False
        return True


def APowerBModN(A, B, N):
    C, F = 0, 1
    BinaryB = format(B, 'b')
    for i in BinaryB:
        C *= 2
        F = (F * F) % N
        if i == '1':
            C = C + 1
            F = (F * A) % N
    return F


def GenerateKey():
    P = int(input('Enter A Prime Number As P: '))
    while not PrimalityCheck(P) or P == '':
        P = int(input('Enter A Prime Number As P: '))
    Q = int(input('Enter A Prime Number As Q: '))
    while not PrimalityCheck(Q) or Q == '':
        Q = int(input('Enter A Prime Number As Q: '))
    N = P * Q
    Phi = (P - 1) * (Q - 1)
    E = int(input('Enter E (1 < E < {}): '.format(Phi)))
    while 1 >= E or E >= Phi or gcd(Phi, E) != 1 or E == '':
        E = int(input('Enter E (1 < E < {}): ').format(Phi))
    for i in range(1, Phi):
        Temp = (Phi * i) + 1
        if Temp % E == 0:
            D = Temp // E
            break
    PublicKey = (E, N)
    PrivateKey = (D, N)
    return PublicKey, PrivateKey


def Encrypt(Plain, Public):
    PlainT = Plain.encode()
    PlainBlock = list()
    CypherBlock = list()

    for P in range(0, len(PlainT), 2):
        if P + 1 < len(PlainT):
            if len(str(PlainT[P])) == 3 and len(str(PlainT[P + 1])) == 3:
                PlainBlock.append(str(PlainT[P]) + str(PlainT[P + 1]))
            elif len(str(PlainT[P])) == 3 and len(str(PlainT[P + 1])) != 3:
                PlainBlock.append(str(PlainT[P]) + str(PlainT[P + 1] * 10))
            elif len(str(PlainT[P])) != 3 and len(str(PlainT[P + 1])) == 3:
                PlainBlock.append(str(PlainT[P] * 10) + str(PlainT[P + 1]))
            else:
                PlainBlock.append(str(PlainT[P] * 10) + str(PlainT[P + 1] * 10))
        else:
            if len(str(PlainT[P])) == 3:
                PlainBlock.append(str(PlainT[P]))
            else:
                PlainBlock.append(str(PlainT[P] * 10))

    for PB in PlainBlock:
        CypherBlock.append(str(APowerBModN(int(PB), Public[0], Public[1])))

    return CypherBlock


def Decrypt(Cypher, Private):
    DecryptionBlock = list()
    ASCIIBlock = list()
    Received = str()

    for CB in Cypher:
        DecryptionBlock.append(str(APowerBModN(int(CB), Private[0], Private[1])))

    for DB in DecryptionBlock:
        if len(DB) != 3:
            if int(DB[:3]) % 10 == 0 and int(DB[:3]) > 120:
                ASCIIBlock.append(str(int(DB[:3]) // 10))
            else:
                ASCIIBlock.append(DB[:3])
            if int(DB[3:]) % 10 == 0 and int(DB[3:]) > 120:
                ASCIIBlock.append(str(int(DB[3:]) // 10))
            else:
                ASCIIBlock.append(DB[3:])
        else:
            if int(DB) % 10 == 0 and int(DB) > 120:
                ASCIIBlock.append(str(int(DB) // 10))
            else:
                ASCIIBlock.append(DB)

    for ASCII in ASCIIBlock:
        Received += chr(int(ASCII))

    return Received


if __name__ == '__main__':
    PublicKey, PrivateKey = GenerateKey()
    PlainText = input('Enter Plain Text: ')
    CypherText = Encrypt(PlainText, PublicKey)
    print('Encrypted Plain Text: {}'.format(CypherText))
    DecryptedText = Decrypt(CypherText, PrivateKey)
    print('Decrypted Cypher Text: {}'.format(DecryptedText))
    # p = ['Mohammad Ali Khodayari', '40032715', 'makhodayari99@gmail.com', 'zxcvbnm123654', 'q7w8e9r6t5y4u1i2o3']
    # t1 = time()
    # for j in range(5):
    #     c = list()
    #     e = list()
    #     for i in range(5):
    #         c.append(Encrypt(p[i], PublicKey))
    #         e.append(Decrypt(c[i], PrivateKey))
    # t2 = time()
    # t3 = (((t2 - t1) / 5) * 1000)
    # print(t3)
