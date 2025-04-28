import os
import sys
import time
import hashlib
import random
import math

def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('No modular inverse')
    else:
        return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

def generate_keys():
    N = 65537  
    while True:
        M = random.randint(2, N-1)
        if math.gcd(M, N) == 1:
            break
    O = random.randint(1000, 5000)
    M_inv = modinv(M, N)
    public_key = (M, O, N)
    private_key = (M_inv, O, N)
    return public_key, private_key

def encrypt(public_key, plaintext):
    M, O, N = public_key
    ciphertext = []
    for ch in plaintext:
        c = (M * (ord(ch) + O)) % N
        ciphertext.append(str(c)) 
    return ' '.join(ciphertext)

def decrypt(private_key, ciphertext_str):
    M_inv, O, N = private_key
    ciphertext = list(map(int, ciphertext_str.split()))
    plaintext = ''
    for c in ciphertext:
        p = (M_inv * c) % N
        plaintext += chr(p - O)
    return plaintext

def hash_message(encrypted_message):
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
    for frame in frames:
        clear()
        print("\n" * 5)
        print(frame)
        time.sleep(0.2)

def main():
    print("\nSimple asymmetric encryption")
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

    while True:
        print("\nPlease write the message you wish to encrypt (end with Ctrl+D or Ctrl+Z + Enter):\n")
        try:
            message = sys.stdin.read().strip()
        except KeyboardInterrupt:
            print("\nInput interrupted. Exiting.")
            break

        public_key, private_key = generate_keys()
        print(f"\nPublic Key: {public_key}")

        encrypted_message = encrypt(public_key, message)
        message_hash = hash_message(encrypted_message)
        combined_message = f"{encrypted_message}||{message_hash}"
       
        print("\nEncrypted message:\n", combined_message)
        print("\nPreparing to send message to Bob...")
        time.sleep(2)
        envelope_animation()

        choice = input("\nWould you like to decrypt the message (y/n)? ")
        if choice.lower() == 'y':
            print(f"\nPrivate Key: {private_key}")
            print(f"\nPublic Key: {public_key}")
            encrypted_message_str, received_hash = combined_message.rsplit("||", 1)
            recalculated_hash = hash_message(encrypted_message_str)
            if recalculated_hash == received_hash:
                message_received = decrypt(private_key, encrypted_message_str)
                print("\nDecrypted message (Integrity Verified):", message_received)
            else:
                print("\nWarning: Message integrity could not be verified! The message may have been tampered with.")
        else:
            print("\nOkay!")

        choice2 = input("\nEncryption complete. Do you wish to encrypt another message (y/n)? ")
        if choice2.lower() == 'n':
            print("\nThank you.")
            break

if __name__ == "__main__":
    main()