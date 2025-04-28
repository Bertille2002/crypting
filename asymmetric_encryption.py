import random
import sys
import time
import os
import hashlib

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

def encrypt(public_key, message) :
    e, n = public_key
    encrypted = [str(pow(ord(char), e, n)) for char in message]
    return ' '.join(encrypted)

def decrypt(private_key, cipher_text) :
    d, n = private_key
    cipher_nums = list(map(int, cipher_text.split()))
    decrypted_chars = [chr(pow(num, d, n)) for num in cipher_nums]
    return ''.join(decrypted_chars)

def hash_message(encrypted_message) :
    return hashlib.sha256(encrypted_message.encode()).hexdigest()

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
    print("\nSimple asymetric encryption")
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
    while True : 
        print("\nPlease write the message you wish to encrypt : ")
        message = sys.stdin.read()
        public_key, private_key = generate_keys()
        print(f"\nPublic Key: {public_key}")
        encrypted_message = encrypt(public_key, message)
        message_hash = hash_message(encrypted_message)
        combined_message = f"{encrypted_message}||{message_hash}"
        print("\nEncrypted message : ", combined_message)
        print("\nPreparing to send message to Bob...")
        time.sleep(5)
        envelope_animation()
        choice = input("\nWould you like to decrypt the message (y/n) ? ")
        if choice == 'y' : 
            print(f"\nPrivate Key: {private_key}")
            print(f"\nPublic Key: {public_key}")
            encrypted_message_str, received_hash = combined_message.rsplit("||", 1)
            recalculated_hash = hash_message(encrypted_message_str)
            if recalculated_hash == received_hash :
                message_received = decrypt(private_key, encrypted_message_str)
                print("\nDecrypted message (Integrity Verified):", message_received)
            else : 
                print("\nWarning: Message integrity could not be verified! The message may have been tampered with.")
                print("Received message:", message_received)
        else : 
            print("\nOkay !") 
        choice2 = input("Encryption complete. Do you wish to encrypt another message (y/n) ? ")
        if choice2 == 'n' : 
            print("Thank you.")
            break 

if __name__ == "__main__" :
    main()