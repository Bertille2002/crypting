import random
import sys

def great_comm_div(a, b) :
    while b != 0 :
        a, b = b, a % b
        return a

def modinv(a, m) :
    m0, x0, x1 = m, 0, 1
    while a > 1 :
        q = a // m 
        a, m = m, a % m 
        x0, x1 = x1 - q * x0, x0 
    return x1 + m0 if x1 < 0 else x1

def is_prime(n) :
    if n < 2 :
        return False
    for i in range(2, int(n**0.5) + 1) :
        if n % i == 0 :
            return False
    return True

def gen_prime(start = 1, end = 200) : 
    while True :
        p = random.randint(start, end)
        if is_prime(p) :
            return p 

def generate_keys() :
    p = gen_prime()
    q = gen_prime()
    while q == p :
        q = gen_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    while great_comm_div(e, phi) != 1 :
        e = random.randrange(2, phi)
    d = modinv(e, phi)
    return ((e, n), (d, n)) #public key, private key

def encrypt(public_key, plain_text) :
    e, n = public_key
    return [pow(ord(char), e, n) for char in plain_text]

def decrypt(private_key, cipher_text) :
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in cipher_text])

def main() :
    print("\nSimple RSA encryption")
    while True : 
        # print("\nPlease write the message you wish to encrypt : ")
        # message = sys.stdin.read()
        message = input("\nPlease write the message you wish to encrypt : ")
        public_key, private_key = generate_keys()
        print(f"\nPublic Key: {public_key}")
        print(f"\nPrivate Key: {private_key}")
        encrypted_message = encrypt(public_key, message)
        print("\nEncrypted message : ", encrypted_message)
        choice = input("Would you like to decrypt the message (y/n) ? ")
        if choice == 'y' : 
            decrypted_message = decrypt(private_key, encrypted_message)
            print("\nDecrypted message : ", decrypted_message)
        else : 
            choice2 = input("Encryption complete. Do you wish to encrypt another message (y/n) ? ")
            if choice2 == n : 
                print("Thank you.")
                break 

if __name__ == "__main__" :
    main()