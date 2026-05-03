def ceaser_encrypt(plaintext,shift):
    encrypted_text=""
    for char in plaintext:
        if char.isalpha():
            start=ord('A') if char.isupper() else ord('a')
            shifted_char=chr((ord(char)-start+shift)%26+start)
            encrypted_text+=shifted_char
        else:
            encrypted_text+=char
    return encrypted_text

def ceaser_decrypt(cipher_text,shift):
    return ceaser_encrypt(cipher_text,-shift)

def BruteForce_Attack(cipher_text):
    print(f"Brute Force Analysis for Ciphertext:'{cipher_text}'")
    for key in range(1,26):
        decrypted_attempt=ceaser_decrypt(cipher_text,key)
        print(f"key #{key:02}:{decrypted_attempt}")
    print("----------------------------------------")
    
if __name__=="__main__":
    print("===Ceaser Cipher Tools===")
    user_msg=input("Enter your message to encrypt:")
    while True:
        try:
            user_key=int(input("Enter the shift key(1-25):"))
            break
        except ValueError:
            print("Invalid key.Enter an integer.")
    encrypted_msg=ceaser_encrypt(user_msg,user_key)
    print(f"Encrypted result:{encrypted_msg}")
    decrypted_verification=ceaser_decrypt(encrypted_msg,user_key)
    print(f"Decrypted Result:{decrypted_verification}")
    
    print("\nSimulating Brute Force Attack.....")
    input("Press Enter to start attack...")
    BruteForce_Attack(encrypted_msg)