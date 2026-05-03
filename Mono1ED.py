import string
import random


# স্ট্যান্ডার্ড ইংরেজি বর্ণমালা (A-Z)
ALPHABET = string.ascii_uppercase

# ==========================================
# 1. Key Generation
# ==========================================
def generate_key():
    """A-Z পর্যন্ত অক্ষরগুলোকে এলোমেলো করে একটি Key ডিকশনারি বানায়"""
    shuffled = list(ALPHABET)
    random.shuffle(shuffled)
    # আসল অক্ষরের সাথে এলোমেলো অক্ষরের জোড়া (Mapping) তৈরি করা হলো
    return dict(zip(ALPHABET, shuffled))

# ==========================================
# 2. Encryption
# ==========================================
def encrypt(text, key):
    """আসল মেসেজকে (Plaintext) গোপন মেসেজে (Ciphertext) রূপান্তর করে"""
    ciphertext = ""
    for char in text.upper():
        # অক্ষর হলে Key অনুযায়ী পরিবর্তন করবে, নাহলে (স্পেস/কমা) যা আছে তাই রাখবে
        ciphertext += key.get(char, char) if char in ALPHABET else char
    return ciphertext

# ==========================================
# 3. Decryption
# ==========================================
def decrypt(ciphertext, key):
    """গোপন মেসেজকে (Ciphertext) পুনরায় আসল মেসেজে (Plaintext) রূপান্তর করে"""
    # এনক্রিপশনের Key-টাকে উল্টো করে ডিক্রিপশন Key বানানো হলো (Value -> Key)
    inv_key = {v: k for k, v in key.items()}
    
    plaintext = ""
    for char in ciphertext.upper():
        plaintext += inv_key.get(char, char) if char in ALPHABET else char
    return plaintext

# ==========================================
# Main Execution Block
# ==========================================
if __name__ == "__main__":
    print("=== Simple Mono-alphabetic Cipher ===")
    
    # ১. চাবি তৈরি করা
    secret_key = generate_key()
    
    # ২. ইউজারের কাছ থেকে ইনপুট নেওয়া
    message = input("Enter your message: ")
    
    # ৩. এনক্রিপ্ট করা
    encrypted_msg = encrypt(message, secret_key)
    print(f"\n[+] Encrypted Message: {encrypted_msg}")
    
    # ৪. ডিক্রিপ্ট করা
    decrypted_msg = decrypt(encrypted_msg, secret_key)
    print(f"[+] Decrypted Message: {decrypted_msg}")