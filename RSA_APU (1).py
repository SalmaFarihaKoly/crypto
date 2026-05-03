import math

def get_private_key(e, phi):
    # Calculate d (modular inverse of e mod phi)
    return pow(e, -1, phi)

def number_to_text(n):
    # Converts a number to text based on the 01=A, 27=Space rule
    s = str(n)
    if len(s) % 2 != 0: s = '0' + s # Pad with leading zero if needed
    
    text = ""
    for i in range(0, len(s), 2):
        val = int(s[i:i+2])
        if 1 <= val <= 26:
            text += chr(ord('A') + val - 1)
        elif val == 27:
            text += " "
    return text

def rsa_task():
    # Given Values
    p = int(input("Enter prime p: "))
    q = int(input("Enter prime q: "))
    e,n = map(int, input("Enter public key (e n): ").split(','))
    c_example = int(input("Enter the cipher: "))
    
    # i. Key Generation
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # ii. Private Key calculation
    d = get_private_key(e, phi)
    print(f"Public Key (PU): {{e={e}, n={n}}}")
    print(f"Private Key (PR): {{d={d}, n={n}}}")

    # iii. Decryption
    # formula: M = C^d mod n
    m_decrypted = pow(c_example, d, n)
    print(f"\nDecrypted Number: {m_decrypted}")
    print(f"Decrypted Text: {number_to_text(m_decrypted)}")

    # iv. Encryption of Initials (Example: Initial 'K' is 11)
    # formula: C = M^e mod n
   # Change this part in your code:
    initials_input = input("Enter the numeric value of your initials (e.g., 718 for GR): ")
    initial_val = int(initials_input) 

    # The code then calculates C = M^e mod n
    c_encrypted = pow(initial_val, e, n)
    print(f"\nEncrypted value (C): {c_encrypted}")

if __name__ == "__main__":
    rsa_task()