
def encrypt(message, key_phrase) : 
    encrypted_message = []
    key = [ord(k) for k in key_phrase if k.strip()]
    key_len = len(key)
    if key_len == 0 :
        raise ValueError("Error : key must have at least one non-space character")
    for i, char in enumerate(message) :
        shift = key[i % key_len]
        encrypted_char = chr((ord(char) + shift) % 256)
        encrypted_message.append(encrypted_char)
    return ''.join(encrypted_message)

def decrypt(encrypted_message, key_phrase) :
    decrypted_message = []
    key = [ord(k) for k in key_phrase if k.strip()]
    key_len = len(key)
    if key_len == 0 :
        raise ValueError("Error : key must have at least one non-space character")
    for i, char in enumerate(encrypted_message) :
        shift = key[i % key_len]
        decrypted_char = chr((ord(char) - shift) % 256)
        decrypted_message.append(decrypted_char)
    return ''.join(decrypted_message)

def main() :
    print("Encrypt any message today !")
    message = input("Enter the message you want to encrypt : ")
    key_phrase = input("Enter the key for encryption : ")
    encrypted_message = encrypt(message, key_phrase)
    print("\n Encripted message (raw) : ", encrypted_message)
    print("\n Encrypted message (hex) : ", encrypted_message.encode('utf-8').hex())

    decrypt_choice = input("\n Would you like to decrypt the message to test it? (y/n) : ")
    if decrypt_choice.lower() == 'y' : 
        decrypted_message = decrypt(encrypted_message, key_phrase)
        print("\n Decrypted message : ", decrypted_message)

if __name__ == "__main__":
    main()
