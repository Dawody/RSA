from Crypto.Util import number
from fractions import gcd
import os
import time


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
	

#Calculate the mod_inverse : https://gist.github.com/ofaurax/6103869014c246f962ab30a513fb5b49
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b%a,a)
    return (g, x - (b//a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    return x%m


f= open("output.dat","w+")

for i in range (10,1000,10):
#Generating very big prime numbers : https://stackoverflow.com/questions/35164881/generating-large-prime-numbers-with-py-crypto
    n_length = i
    p = number.getPrime(n_length, os.urandom)
    q = number.getPrime(n_length, os.urandom)

#    print("p=",p,"\nq=",q)

    n=p*q
#    print("n=",n)
    fin = (p-1)*(q-1)
###################################################
#----------------generate small (e)--------------
#    e =2
#    while (gcd(e,fin)-1):
#        if e<fin:
#            e=e+1
#        else:
#            raise Exception('ERROR can not find (e)')
            

#------------generate very big (e)---------------
    e = fin-1
    while (gcd(e,fin)-1):
        if e>1:
            e=e-1
        else:
            raise Exception('ERROR can not find (e)')
#------------------------------------------------
#    print("e=",e)
###################################################

    d = modinv(e, fin)


    print("***i= ",i,"***")
    print("PU={e,n} = {",e,",",n,"}")
    print("PR={d,n} = {",d,",",n,"}")
    print("========================")

#################################################
#------------------encrypt-----------------------
    start = time.time()
    m=222
    print("m = ", m)
    c = pow(m,e,n)
    print("c = ", c)
    end = time.time()


#------------------decrypt-----------------------
#calculate the power for very large numbers : https://stackoverflow.com/questions/23759098/pow-or-for-very-large-number-in-python
    m = pow(c,d,n)
    print("m = ",m)


#################################################
    f.write("%s %s\n" % (i,(end-start)))
f.close()
