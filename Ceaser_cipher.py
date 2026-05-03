def caesar_encrypt(plaintext, shift):
    """
    Encrypts the plaintext using the Caesar Cipher technique.
    """
    encrypted_text = ""
    for char in plaintext:
        if char.isalpha():
            # Determine if the character is uppercase or lowercase
            start = ord('A') if char.isupper() else ord('a')
            
            # Apply the shift with modulo 26
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            encrypted_text += shifted_char
        else:
            # Keep non-alphabetic characters (spaces, numbers, punctuation) unchanged
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(ciphertext, shift):
    """
    Decrypts the ciphertext using a known shift key.
    """
    return caesar_encrypt(ciphertext, -shift)

def brute_force_attack(ciphertext):
    """
    Performs a brute-force analysis by attempting every possible shift (1-25).
    """
    print(f"\n--- Brute Force Analysis for Ciphertext: '{ciphertext}' ---")
    # Try every possible key from 1 to 25
    for key in range(1, 26):
        decrypted_attempt = caesar_decrypt(ciphertext, key)
        print(f"Key #{key:02}: {decrypted_attempt}")
    print("-------------------------------------------------------")

# --- Main Execution Block ---
if __name__ == "__main__":
    print("=== Caesar Cipher Tool ===")
    
    # 1. Take User Input
    user_message = input("Enter the message to encrypt: ")
    
    # Input validation for the key to ensure it's a number
    while True:
        try:
            user_key = int(input("Enter the shift key (1-25): "))
            break
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # 2. Perform Encryption
    encrypted_msg = caesar_encrypt(user_message, user_key)
    print(f"\n[+] Encrypted Result: {encrypted_msg}")

    # 3. Perform Decryption (Verification)
    # We decrypt the result just to prove the math works
    decrypted_verification = caesar_decrypt(encrypted_msg, user_key)
    print(f"[+] Decryption Check: {decrypted_verification}")

    # 4. Study: Brute-Force Attack
    # Now we simulate an attacker who intercepted 'encrypted_msg'
    print("\n[!] Simulating Brute-Force Attack on your message...")
    input("Press Enter to start the attack...")
    brute_force_attack(encrypted_msg)