import os
import struct

# ==========================================
# 1. Cryptographic Helper Functions
# ==========================================

def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    """XORs two byte strings of equal length."""
    return bytes(x ^ y for x, y in zip(b1, b2))

def pad(data: bytes, block_size: int = 8) -> bytes:
    """PKCS#7 Padding to ensure data is a multiple of the block size (8 bytes for DES)."""
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def unpad(data: bytes) -> bytes:
    """Removes PKCS#7 Padding."""
    pad_len = data[-1]
    return data[:-pad_len]

# ==========================================
# 2. The Block Cipher Primitive (Mock DES)
# ==========================================

class EducationalDESPrimitive:
    """
    A simplified 64-bit (8-byte) block cipher that mimics the DES interface.
    Real DES requires massive permutation tables. This primitive uses a basic 
    reversible mathematical shift to prove the Modes of Operation work correctly.
    """
    def __init__(self, key: bytes):
        if len(key) != 8:
            raise ValueError("DES key must be exactly 8 bytes (64 bits).")
        self.key = key

    def encrypt_block(self, block: bytes) -> bytes:
        if len(block) != 8:
            raise ValueError("DES operates on strictly 8-byte blocks.")
        # Simple substitution mimicking distinct encryption
        return bytes((b + k) % 256 for b, k in zip(block, self.key))

    def decrypt_block(self, block: bytes) -> bytes:
        if len(block) != 8:
            raise ValueError("DES operates on strictly 8-byte blocks.")
        # Reverse substitution for decryption
        return bytes((b - k) % 256 for b, k in zip(block, self.key))

# ==========================================
# 3. Modes of Operation
# ==========================================

class BlockCipherModes:
    def __init__(self, cipher_primitive):
        self.cipher = cipher_primitive
        self.block_size = 8  # 64 bits for DES

    # ------------------------------------------
    # Electronic Codebook (ECB)
    # ------------------------------------------
    def encrypt_ecb(self, plaintext: bytes) -> bytes:
        plaintext = pad(plaintext, self.block_size)
        ciphertext = bytearray()
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            ciphertext.extend(self.cipher.encrypt_block(block))
        return bytes(ciphertext)

    def decrypt_ecb(self, ciphertext: bytes) -> bytes:
        plaintext = bytearray()
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            plaintext.extend(self.cipher.decrypt_block(block))
        return unpad(bytes(plaintext))

    # ------------------------------------------
    # Cipher Block Chaining (CBC)
    # ------------------------------------------
    def encrypt_cbc(self, plaintext: bytes, iv: bytes) -> bytes:
        plaintext = pad(plaintext, self.block_size)
        ciphertext = bytearray()
        prev_block = iv
        
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            # XOR plaintext with previous ciphertext block (or IV) BEFORE encrypting
            xored_block = xor_bytes(block, prev_block)
            encrypted_block = self.cipher.encrypt_block(xored_block)
            ciphertext.extend(encrypted_block)
            prev_block = encrypted_block
            
        return bytes(ciphertext)

    def decrypt_cbc(self, ciphertext: bytes, iv: bytes) -> bytes:
        plaintext = bytearray()
        prev_block = iv
        
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            # Decrypt the block FIRST, then XOR with previous ciphertext block (or IV)
            decrypted_block = self.cipher.decrypt_block(block)
            plaintext.extend(xor_bytes(decrypted_block, prev_block))
            prev_block = block
            
        return unpad(bytes(plaintext))

    # ------------------------------------------
    # Cipher Feedback (CFB)
    # ------------------------------------------
    def encrypt_cfb(self, plaintext: bytes, iv: bytes) -> bytes:
        # CFB turns a block cipher into a stream cipher; padding is optional but we keep it block-aligned here
        ciphertext = bytearray()
        prev_block = iv
        
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            if len(block) < self.block_size:
                block = block.ljust(self.block_size, b'\x00') # Handle partial final block
                
            # Encrypt the previous ciphertext (or IV)
            keystream = self.cipher.encrypt_block(prev_block)
            # XOR with plaintext to create ciphertext
            encrypted_block = xor_bytes(block, keystream)
            ciphertext.extend(encrypted_block)
            prev_block = encrypted_block
            
        return bytes(ciphertext)[:len(plaintext)] # Trim to original length

    def decrypt_cfb(self, ciphertext: bytes, iv: bytes) -> bytes:
        plaintext = bytearray()
        prev_block = iv
        
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            actual_len = len(block)
            if actual_len < self.block_size:
                block_padded = block.ljust(self.block_size, b'\x00')
            else:
                block_padded = block
                
            # Notice we use ENCRYPT_BLOCK for decryption in CFB mode!
            keystream = self.cipher.encrypt_block(prev_block)
            decrypted_block = xor_bytes(block_padded, keystream)
            plaintext.extend(decrypted_block[:actual_len])
            prev_block = block_padded
            
        return bytes(plaintext)

    # ------------------------------------------
    # Output Feedback (OFB)
    # ------------------------------------------
    def process_ofb(self, data: bytes, iv: bytes) -> bytes:
        # OFB encryption and decryption are identical (Stream Cipher)
        processed_data = bytearray()
        prev_keystream = iv
        
        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            actual_len = len(block)
            
            # The cipher encrypts the previous keystream, independent of plaintext
            prev_keystream = self.cipher.encrypt_block(prev_keystream)
            processed_block = xor_bytes(block, prev_keystream[:actual_len])
            processed_data.extend(processed_block)
            
        return bytes(processed_data)

    # ------------------------------------------
    # Counter (CTR)
    # ------------------------------------------
    def process_ctr(self, data: bytes, nonce: bytes) -> bytes:
        # CTR encryption and decryption are identical (Stream Cipher)
        # Nonce is typically 4 bytes for DES, leaving 4 bytes for the counter
        if len(nonce) != 4:
            raise ValueError("For 64-bit CTR, nonce must be 4 bytes.")
            
        processed_data = bytearray()
        counter = 0
        
        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            actual_len = len(block)
            
            # Pack nonce (4 bytes) and counter (4 bytes) into a 64-bit block
            counter_block = nonce + struct.pack(">I", counter)
            
            # Encrypt the counter block to get the keystream
            keystream = self.cipher.encrypt_block(counter_block)
            processed_block = xor_bytes(block, keystream[:actual_len])
            processed_data.extend(processed_block)
            
            counter += 1 # Increment counter for the next block
            
        return bytes(processed_data)

# ==========================================
# 4. Execution & Testing
# ==========================================

if __name__ == "__main__":
    # Setup
    key = b"SECRETKY" # 8 bytes for DES
    iv = os.urandom(8) # 8 byte Initialization Vector
    nonce = os.urandom(4) # 4 byte Nonce for CTR mode
    
    plaintext = b"Cryptography is the ultimate math puzzle!"
    
    print(f"--- Original Plaintext: {plaintext} ---\n")
    
    des_primitive = EducationalDESPrimitive(key)
    modes = BlockCipherModes(des_primitive)

    # 1. ECB
    print("[*] Testing ECB Mode")
    c_ecb = modes.encrypt_ecb(plaintext)
    p_ecb = modes.decrypt_ecb(c_ecb)
    print(f"    Ciphertext (hex): {c_ecb.hex()}")
    print(f"    Decrypted: {p_ecb}\n")

    # 2. CBC
    print("[*] Testing CBC Mode")
    c_cbc = modes.encrypt_cbc(plaintext, iv)
    p_cbc = modes.decrypt_cbc(c_cbc, iv)
    print(f"    Ciphertext (hex): {c_cbc.hex()}")
    print(f"    Decrypted: {p_cbc}\n")

    # 3. CFB
    print("[*] Testing CFB Mode")
    c_cfb = modes.encrypt_cfb(plaintext, iv)
    p_cfb = modes.decrypt_cfb(c_cfb, iv)
    print(f"    Ciphertext (hex): {c_cfb.hex()}")
    print(f"    Decrypted: {p_cfb}\n")

    # 4. OFB (Encrypt and Decrypt use the same function)
    print("[*] Testing OFB Mode")
    c_ofb = modes.process_ofb(plaintext, iv)
    p_ofb = modes.process_ofb(c_ofb, iv)
    print(f"    Ciphertext (hex): {c_ofb.hex()}")
    print(f"    Decrypted: {p_ofb}\n")

    # 5. CTR (Encrypt and Decrypt use the same function)
    print("[*] Testing CTR Mode")
    c_ctr = modes.process_ctr(plaintext, nonce)
    p_ctr = modes.process_ctr(c_ctr, nonce)
    print(f"    Ciphertext (hex): {c_ctr.hex()}")
    print(f"    Decrypted: {p_ctr}\n")