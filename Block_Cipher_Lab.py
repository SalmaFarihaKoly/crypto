def xor_string(s1: str, s2: str) -> str:
    """XORs two strings of equal length character by character and returns the new string."""
    return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(s1, s2))

def pad_data(text: str, block_size: int = 8) -> str:
    """Pads the plaintext with 'X' to ensure its length is a multiple of the block size."""
    if len(text) % block_size == 0:
        return text
    pad_len = block_size - (len(text) % block_size)
    return text + ('X' * pad_len)

# ==========================================
# CBC Mode Encryption & Decryption
# ==========================================

def cbc_encrypt(plaintext: str, key: str, iv: str, block_size: int = 8) -> list:
    padded_pt = pad_data(plaintext, block_size)
    cipher_blocks = []
    prev_block = iv
    
    print("\n--- Encryption Steps ---")
    for i in range(0, len(padded_pt), block_size):
        p_block = padded_pt[i:i + block_size]
        
        # Step 1: XOR plaintext block with IV or previous ciphertext block
        xored_with_prev = xor_string(p_block, prev_block)
        
        # Step 2: "Encrypt" by XORing with the Key
        c_block = xor_string(xored_with_prev, key)
        
        cipher_blocks.append(c_block)
        print(f"P{(i//block_size)+1}: '{p_block}' -> C{(i//block_size)+1}: '{c_block}'")
        
        # Save the current ciphertext block to use in the next round
        prev_block = c_block 
        
    return cipher_blocks

def cbc_decrypt(cipher_blocks: list, key: str, iv: str) -> str:
    plaintext = ""
    prev_block = iv
    
    print("\n--- Decryption Steps ---")
    for i, c_block in enumerate(cipher_blocks):
        # Step 1: "Decrypt" by XORing with the Key
        decrypted_step = xor_string(c_block, key)
        
        # Step 2: XOR with IV or previous ciphertext block to recover the original plaintext
        p_block = xor_string(decrypted_step, prev_block)
        
        plaintext += p_block
        print(f"C{i+1}: '{c_block}' -> P{i+1}: '{p_block}'")
        
        # Save the current ciphertext block to use in the next round
        prev_block = c_block 
        
    # Remove the 'X' padding characters at the end to return the actual original plaintext
    return plaintext.rstrip('X')

# ==========================================
# ECB Mode Encryption & Decryption
# ==========================================

def ecb_encrypt(plaintext: str, key: str, block_size: int = 8) -> list:
    padded_pt = pad_data(plaintext, block_size)
    cipher_blocks = []
    
    print("\n--- ECB Encryption Steps ---")
    for i in range(0, len(padded_pt), block_size):
        p_block = padded_pt[i:i + block_size]
        
        # ECB-তে সরাসরি Key দিয়ে XOR করা হয় (কোনো IV লাগে না)
        c_block = xor_string(p_block, key)
        
        cipher_blocks.append(c_block)
        print(f"P{(i//block_size)+1}: '{p_block}' -> C{(i//block_size)+1}: '{c_block}'")
        
    return cipher_blocks

def ecb_decrypt(cipher_blocks: list, key: str) -> str:
    plaintext = ""
    
    print("\n--- ECB Decryption Steps ---")
    for i, c_block in enumerate(cipher_blocks):
        # ECB-তে সরাসরি Key দিয়ে XOR করলেই প্লেইনটেক্সট পাওয়া যায়
        p_block = xor_string(c_block, key)
        
        plaintext += p_block
        print(f"C{i+1}: '{c_block}' -> P{i+1}: '{p_block}'")
        
    return plaintext.rstrip('X')

# ==========================================
# CFB Mode Encryption & Decryption
# ==========================================

def cfb_encrypt(plaintext: str, key: str, iv: str, block_size: int = 8) -> list:
    padded_pt = pad_data(plaintext, block_size)
    cipher_blocks = []
    prev_block = iv # শুরুতে IV দিয়ে কাজ শুরু হয়
    
    print("\n--- CFB Encryption Steps ---")
    for i in range(0, len(padded_pt), block_size):
        p_block = padded_pt[i:i + block_size]
        
        # ধাপ ১: আগের সাইফার ব্লক (বা IV) কে Key দিয়ে "Encrypt" করা হয়
        encrypted_prev = xor_string(prev_block, key)
        
        # ধাপ ২: সেই এনক্রিপ্টেড রেজাল্টের সাথে বর্তমান প্লেইনটেক্সট XOR করা হয়
        c_block = xor_string(p_block, encrypted_prev)
        
        cipher_blocks.append(c_block)
        print(f"P{(i//block_size)+1}: '{p_block}' -> C{(i//block_size)+1}: '{c_block}'")
        
        # পরবর্তী ব্লকের জন্য বর্তমান সাইফার ব্লককে সেভ করা হয়
        prev_block = c_block
        
    return cipher_blocks

def cfb_decrypt(cipher_blocks: list, key: str, iv: str) -> str:
    plaintext = ""
    prev_block = iv
    
    print("\n--- CFB Decryption Steps ---")
    for i, c_block in enumerate(cipher_blocks):
        # ধাপ ১: আগের সাইফার ব্লক (বা IV) কে Key দিয়ে "Encrypt" করা হয় (ঠিক এনক্রিপশনের মতো)
        encrypted_prev = xor_string(prev_block, key)
        
        # ধাপ ২: সেই রেজাল্টের সাথে বর্তমান সাইফার ব্লক XOR করলে প্লেইনটেক্সট পাওয়া যায়
        p_block = xor_string(c_block, encrypted_prev)
        
        plaintext += p_block
        print(f"C{i+1}: '{c_block}' -> P{i+1}: '{p_block}'")
        
        # পরবর্তী ব্লকের জন্য বর্তমান সাইফার ব্লককে সেভ করা হয়
        prev_block = c_block
        
    return plaintext.rstrip('X')


# ==========================================
# OFB Mode Encryption & Decryption
# ==========================================

def ofb_encrypt(plaintext: str, key: str, iv: str, block_size: int = 8) -> list:
    padded_pt = pad_data(plaintext, block_size)
    cipher_blocks = []
    prev_output = iv # এখানে আউটপুট ফিডব্যাক হিসেবে কাজ করে
    
    print("\n--- OFB Encryption Steps ---")
    for i in range(0, len(padded_pt), block_size):
        p_block = padded_pt[i:i + block_size]
        
        # ধাপ ১: আগের আউটপুটকে (বা IV) Key দিয়ে এনক্রিপ্ট করে "Keystream" তৈরি করা হয়
        keystream_block = xor_string(prev_output, key)
        
        # ধাপ ২: সেই Keystream-এর সাথে প্লেইনটেক্সট XOR করে সাইফার তৈরি করা হয়
        c_block = xor_string(p_block, keystream_block)
        
        cipher_blocks.append(c_block)
        print(f"P{(i//block_size)+1}: '{p_block}' -> C{(i//block_size)+1}: '{c_block}'")
        
        # পরবর্তী রাউন্ডের জন্য "এনক্রিপশন আউটপুট" সেভ করা হয় (সাইফারটেক্সট নয়!)
        prev_output = keystream_block
        
    return cipher_blocks

def ofb_decrypt(cipher_blocks: list, key: str, iv: str) -> str:
    plaintext = ""
    prev_output = iv
    
    print("\n--- OFB Decryption Steps ---")
    for i, c_block in enumerate(cipher_blocks):
        # ধাপ ১: একই ভাবে Keystream তৈরি করা হয়
        keystream_block = xor_string(prev_output, key)
        
        # ধাপ ২: সাইফারের সাথে Keystream XOR করলে প্লেইনটেক্সট ফিরে আসে
        p_block = xor_string(c_block, keystream_block)
        
        plaintext += p_block
        print(f"C{i+1}: '{c_block}' -> P{i+1}: '{p_block}'")
        
        # ফিডব্যাক হিসেবে আউটপুট আপডেট করা হয়
        prev_output = keystream_block
        
    return plaintext.rstrip('X')

# ==========================================
# CTR Mode Encryption & Decryption
# ==========================================

def ctr_encrypt(plaintext: str, key: str, nonce: str, block_size: int = 8) -> list:
    # CTR একটি স্ট্রিম সাইফার মোড বলে এতে প্যাডিং বাধ্যতামূলক নয়, 
    # তবে আমরা ব্লক অনুযায়ী দেখানোর জন্য প্যাড করে নিচ্ছি।
    padded_pt = pad_data(plaintext, block_size)
    cipher_blocks = []
    counter = 0 
    
    print("\n--- CTR Encryption Steps ---")
    for i in range(0, len(padded_pt), block_size):
        p_block = padded_pt[i:i + block_size]
        
        # ১. কাউন্টার ব্লক তৈরি (Nonce + Counter)
        # এখানে Nonce এবং Counter-কে মিলিয়ে একটি ৮-অক্ষরের ব্লক বানানো হচ্ছে
        counter_block = (nonce + str(counter).zfill(8-len(nonce)))[:block_size]
        
        # ২. কাউন্টার ব্লককে Key দিয়ে এনক্রিপ্ট করে Keystream তৈরি করা
        keystream = xor_string(counter_block, key)
        
        # ৩. প্লেইনটেক্সট ব্লকের সাথে Keystream XOR করা
        c_block = xor_string(p_block, keystream)
        
        cipher_blocks.append(c_block)
        print(f"Counter {counter} ('{counter_block}') -> C{(i//block_size)+1}: '{c_block}'")
        
        # কাউন্টার ১ বাড়িয়ে দেওয়া (এটিই পরের ব্লকের ইনপুট)
        counter += 1
        
    return cipher_blocks

def ctr_decrypt(cipher_blocks: list, key: str, nonce: str, block_size: int = 8) -> str:
    # এখানে block_size: int = 8 যোগ করা হয়েছে যাতে ফাংশনটি এটি চিনতে পারে
    plaintext = ""
    counter = 0
    
    print("\n--- CTR Decryption Steps ---")
    for i, c_block in enumerate(cipher_blocks):
        # এখন block_size চিনতে পারায় আর NameError আসবে না
        counter_block = (nonce + str(counter).zfill(8-len(nonce)))[:block_size]
        keystream = xor_string(counter_block, key)
        
        p_block = xor_string(c_block, keystream)
        
        plaintext += p_block
        print(f"C{i+1} XOR Keystream_{counter} -> P{i+1}: '{p_block}'")
        counter += 1
        
    return plaintext.rstrip('X')
# ==========================================
# Main Program (User Input Mode)
# ==========================================
def get_user_input(prompt: str, default_val: str) -> str:
    """Function to take user input. Uses the default value if the user just presses Enter."""
    user_val = input(f"{prompt} (Default: '{default_val}'): ")
    return user_val if user_val else default_val

if __name__ == "__main__":
    print("=========================================")
    print("      CBC Mode XOR Encryption Tool       ")
    print("=========================================\n")
    print("Instructions: Provide your data below. To use the assignment's default data, just press Enter.\n")

    # Take user input
    plaintext = get_user_input("Enter Plaintext", "ICEDEPT@RU")
    
    # IV and Key must be exactly 8 characters
    while True:
        iv = get_user_input("Enter 8-character IV", "ABCDEFGH")
        if len(iv) == 8: break
        print("Invalid input! IV must be exactly 8 characters long.")
        
    while True:
        key = get_user_input("Enter 8-character Key", "12345678")
        if len(key) == 8: break
        print("Invalid input! Key must be exactly 8 characters long.")
    
    print("\n[Input Summary]")
    print(f"Plaintext : {plaintext}")
    print(f"IV        : {iv}")
    print(f"Key       : {key}")
    
    # 1. Encryption
    encrypted_blocks = cbc_encrypt(plaintext, key, iv)
    print("\n[Final Encrypted Output]")
    for i, block in enumerate(encrypted_blocks):
        print(f"C{i+1} = \"{block}\"")
        
    # 2. Decryption
    decrypted_text = cbc_decrypt(encrypted_blocks, key, iv)
    print(f"\n[Final Decrypted Output]")
    print(f"Recovered Plaintext: {decrypted_text}")
    
    # ------------------------------------------
    # ECB Mode Testing
    # ------------------------------------------
    print("\n\n" + "="*20)
    print(" Testing ECB Mode ")
    print("="*20)

    # 1. ECB Encryption
    ecb_encrypted = ecb_encrypt(plaintext, key)
    
    # 2. ECB Decryption
    ecb_decrypted = ecb_decrypt(ecb_encrypted, key)
    print(f"\n[ECB Final Output] Recovered: {ecb_decrypted}")
    
    # ------------------------------------------
    # CFB Mode Testing
    # ------------------------------------------
    print("\n\n" + "="*20)
    print(" Testing CFB Mode ")
    print("="*20)

    # 1. CFB Encryption
    cfb_encrypted = cfb_encrypt(plaintext, key, iv)
    
    # 2. CFB Decryption
    cfb_decrypted = cfb_decrypt(cfb_encrypted, key, iv)
    print(f"\n[CFB Final Output] Recovered: {cfb_decrypted}")
    
    # ------------------------------------------
    # OFB Mode Testing
    # ------------------------------------------
    print("\n\n" + "="*20)
    print(" Testing OFB Mode ")
    print("="*20)

    # 1. OFB Encryption
    ofb_encrypted = ofb_encrypt(plaintext, key, iv)
    
    # 2. OFB Decryption
    ofb_decrypted = ofb_decrypt(ofb_encrypted, key, iv)
    print(f"\n[OFB Final Output] Recovered: {ofb_decrypted}")
    
    # ------------------------------------------
    # CTR Mode Testing
    # ------------------------------------------
    print("\n\n" + "="*20)
    print(" Testing CTR Mode ")
    print("="*20)

    nonce = "ABC" # ৩ অক্ষরের নন্স, বাকি ৫ ঘর কাউন্টার দিয়ে পূরণ হবে
    
    # 1. CTR Encryption
    ctr_encrypted = ctr_encrypt(plaintext, key, nonce)
    
    # 2. CTR Decryption
    ctr_decrypted = ctr_decrypt(ctr_encrypted, key, nonce)
    print(f"\n[CTR Final Output] Recovered: {ctr_decrypted}")