import random
import sys
import time
import os

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

def gen_prime(start = 100, end = 300) : 
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

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def envelope_animation():
    frames = [
        "Alice     ✉                                                  Bob",
        "Alice          ✉                                             Bob",
        "Alice               ✉                                        Bob",
        "Alice                    ✉                                   Bob",
        "Alice                         ✉                              Bob",
        "Alice                              ✉                         Bob",
        "Alice                                   ✉                    Bob",
        "Alice                                        ✉               Bob",
        "Alice                                             ✉          Bob",
        "Alice                                                  ✉     Bob",
        "Alice                                                       ✉Bob",
        "Alice                                                        📬Bob",
    ]
    for frame in frames : 
        clear()
        print("\n" * 5)
        print(frame)
        time.sleep(0.2)


def main() :
    print("\nSimple RSA encryption")
    print("""\n
        
        +--------+         +----------------+         +----------------+         +--------+
        | Alice  | ----->  | Texte en clair | ----->  | Texte chiffré  | ----->  |  Bob   |
        +--------+         +----------------+         +----------------+         +--------+
                                 |                          ^
                                 v                          |
                       +------------------+         +------------------+
                       | Clé publique de  |         |  Clé privée de   |
                       |      Bob         | ======> |       Bob        |
                       +------------------+         +------------------+

    """)
    username_alice = 'alice'
    password_alice = 'alice'
    username_bob = 'bob'
    password_bob = 'bob'
    while True : 
        print("\nWelcome Alice, to verify it's you, please sign in.")
        username_sender = input("Please enter your username : ").strip()
        if username_sender == username_alice : 
            password_sender = input("Please enter your password : ").strip()
            if password_sender == password_alice :
                print("\nLogin successful !")
                print("\nPlease write the message you wish to encrypt : ")
                message = sys.stdin.read()
                public_key, private_key = generate_keys()
                print(f"\nPublic Key: {public_key}")
                print(f"\nPrivate Key: {private_key}")
                encrypted_message = encrypt(public_key, message)
                print("\nEncrypted message : ", encrypted_message)
                print("\nSending message to Bob...")
                envelope_animation()
                choice = input("\nWould you like to decrypt the message (y/n) ? ")
                if choice == 'y' : 
                    print("\nTo receive the message, you must be logged in as Bob.")
                    username_receiver = input("\nPlease enter your username : ").strip()
                    if username_receiver == username_bob :
                        password_receiver = input("\nPlease enter your password : ").strip()
                        if password_receiver == password_bob : 
                            print("\nLogin successful !")
                            decrypted_message = decrypt(private_key, encrypted_message)
                            print("\nDecrypted message : ", decrypted_message)
                        else :
                            print("Incorrect password.")
                    else :
                        print("Incorrect username")
                else : 
                    print("\nOkay !") 
                choice2 = input("Encryption complete. Do you wish to encrypt another message (y/n) ? ")
                if choice2 == 'n' : 
                    print("Thank you.")
                    break 
            else :
                print("Incorrect password.")
        else :
            print("Incorrect username.")

if __name__ == "__main__" :
    main()