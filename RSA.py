
from Crypto.Util import number
from fractions import gcd
import os
import time
import matplotlib.pyplot as plt


#
#####  RSA-algorithm ##############################################################################
#  Key Generation
#  1.select two prime numbers p & q
#  2.calculate n = p * q
#  3.calculate fiN = (p-1) * (q-1)
#  4.choose value for e : 1 < e < fiN & gcd(e,fiN) = 1
#  5.calculate d = e^-1 mod(fiN) -> d*e*mod(fiN)=1 -> d*e must equal multible of fiN +1
#  6.PU = {e,n}
#  7.PR = {d,n}
# -----------------------------------------------
#  Encryption
#  C = M^e mod(n) : plaintext, M < n
# -----------------------------------------------
#  Decryption
#  M = C^d mod(n) : ciphertext, C
###################################################################################################
#



#Calculate the mod_inverse
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a, a)
    return (g, x - (b//a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m




def RSA():
    f= open("output.dat","w+")
    bits_time = []
    for i in range (5,500,10):
        #Generating very big prime numbers
        n_length = i
        p = number.getPrime(n_length, os.urandom)
        q = number.getPrime(n_length, os.urandom)

        n=p*q
        fin = (p-1)*(q-1)


        e = fin-1
        while (gcd(e,fin)-1):
            if e>1:
                e=e-1
            else:
                raise Exception('ERROR can not find (e)')


        d = modinv(e, fin)



        print("number of bits = ",i*2,"")
        print("PU={e,n} = {",e,",",n,"}")
        print("PR={d,n} = {",d,",",n,"}")
        print("=============================================================================================================================================")




###################################################################################################
        #------------------encrypt-----------------------
        start = time.time()
        m=9999
        print("m = ", m)
        c = pow(m,e,n)
        print("c = ", c)
        end = time.time()


        #------------------decrypt-----------------------
        #pow(x,y,z) : With two arguments, equivalent to x**y.  With three arguments,equivalent to (x**y) % z
        m = pow(c,d,n)
        print("m = ",m)
        bits_time.append([i*2, end-start])

###################################################################################################


        f.write("%s %s\n" % (i,(end-start)))

    x = [a for (a, b) in bits_time]
    y = [b for (a, b) in bits_time]
    plt.plot(x,y)
    plt.show()
    f.close()


def brute(n):
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            return i, n/i

    return -1, -1



def choosenCipher(c,e,d,n):
    m = pow(c*pow(2,e,n), d, n)/2
    return m



def brute_force():
    f= open("bruteforce.dat","w+")
    bits_time = []
    for i in range (10,25,1):

        #Generating very big prime numbers :
        n_length = i
        p = number.getPrime(n_length, os.urandom)
        q = number.getPrime(n_length, os.urandom)

        n=p*q

        fin = (p-1)*(q-1)

        e = fin-1
        while (gcd(e,fin)-1):
            if e>1:
                e=e-1
            else:
                raise Exception('ERROR can not find (e)')


        d = modinv(e, fin)

        print("number of bits = ",i,"")
        print("PU={e,n} = {",e,",",n,"}")
        print("PR={d,n} = {",d,",",n,"}")
        start = time.time()
        p, q =brute(n)
        if p==-1 or q==-1:
            print("ERROR")
        else:
            print("cracked n=", p*q)
        print("========================")
        end = time.time()
        bits_time.append([i, end-start])


            #------------------encrypt-----------------------
        start = time.time()
        m=222
        print("m = ", m)
        c = pow(m,e,n)
        print("c = ", c)
        end = time.time()

        print("choosen cipher:",choosenCipher(c,e,d,n))

        f.write("%s %s\n" % (i,(end-start)))

    f.close()
    x = [a for (a, b) in bits_time]
    y = [b for (a, b) in bits_time]
    plt.plot(x,y)
    plt.show()


RSA()
brute_force()

