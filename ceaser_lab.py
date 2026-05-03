import datetime

def caesar_encrypt(plaintext, shift):
    """অক্ষরগুলোকে শিফট করে এনক্রিপ্ট করার ফাংশন"""
    encrypted_text = ""
    for char in plaintext:
        if char.isalpha():
            # বড় হাতের না ছোট হাতের তা নির্ধারণ করা
            start = ord('A') if char.isupper() else ord('a')
            # বর্ণমালার ২৬ অক্ষরের মধ্যে শিফট করা
            shifted_char = chr((ord(char) - start + shift) % 26 + start)
            encrypted_text += shifted_char
        else:
            # স্পেস, @, : বা অন্য চিহ্ন অপরিবর্তিত রাখা
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(ciphertext, shift):
    """ডিক্রিপ্ট করার জন্য এনক্রিপশন ফাংশনকেই নেগেটিভ শিফটে কল করা"""
    return caesar_encrypt(ciphertext, -shift)

def solve_part_a():
    print("--- Task (a): Encrypting Name and Current Time ---")
    
    # ১. নাম ইনপুট
    first_name = input("Enter your first name: ")
    
    # ২. বর্তমান সময় নেওয়া (HH:MMam/pm ফরম্যাটে)
    current_time = datetime.datetime.now().strftime("%I:%M%p").lower()
    
    # ৩. মেসেজ তৈরি করা: first_name@current-time
    plaintext = f"{first_name}@{current_time}"
    print(f"Original Plaintext: {plaintext}")
    
    # ৪. কী হিসেবে অক্ষর ইনপুট নেওয়া (যেমন: T)
    key_char = input("Enter a key letter (A-Z): ").upper()
    shift = ord(key_char) - ord('A') # A=0, B=1, C=2...
    
    # ৫. এনক্রিপশন
    encrypted_msg = caesar_encrypt(plaintext, shift)
    print(f"Using Key {key_char} (Shift {shift}): {encrypted_msg}\n")

def solve_part_b():
    print("--- Task (b): Brute Force Attack ---")
    ciphertext = "VruykmlxvnbmrterTgtefmlTmxVkxtmboxBg Max Ftkdxm Whftbg"
    
    print(f"Target Ciphertext: '{ciphertext}'")
    print("Attempting every possible shift (1-25)...\n")
    
    # ১ থেকে ২৫ পর্যন্ত সব কী চেক করা
    for shift in range(1, 26):
        attempt = caesar_decrypt(ciphertext, shift)
        key_letter = chr(ord('A') + shift) # শিফট ভ্যালুকে অক্ষরে রূপান্তর
        
        # আউটপুট প্রিন্ট করা
        print(f"Key {key_letter} (Shift {shift:02}): {attempt}")
    
    print("\n[Analysis Complete] Check the list to find the readable sentence.")

if __name__ == "__main__":
    # পার্ট (a) রান করা
    solve_part_a()
    
    # পার্ট (b) রান করা
    input("Press Enter to start Brute Force Attack on Part (b)...")
    solve_part_b()