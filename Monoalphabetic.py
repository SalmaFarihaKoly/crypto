import random
import math
import re
from collections import Counter

# ==========================================
# 1. Scoring Data (Language Model)
# ==========================================
L_SCORES = {'A': 2.6, 'B': 0.5, 'C': 0.9, 'D': 1.3, 'E': 3.0, 'F': 0.6, 'G': 0.7, 'H': 1.0, 'I': 2.3, 'J': 0.1, 'K': 0.3, 'L': 1.5, 'M': 0.8, 'N': 2.0, 'O': 2.2, 'P': 0.7, 'Q': 0.1, 'R': 2.0, 'S': 1.9, 'T': 2.4, 'U': 0.8, 'V': 0.3, 'W': 0.4, 'X': 0.2, 'Y': 0.6, 'Z': 0.1}
BIGRAMS = {"TH":3.5,"HE":3.2,"IN":2.8,"ER":2.6,"AN":2.6,"RE":2.4,"ON":2.4,"AT":2.3,"EN":2.2,"ND":2.2,"TI":2.0,"ES":2.0,"OR":2.0,"TE":1.9,"OF":1.9,"ED":1.8,"IS":1.8,"IT":1.8,"AL":1.7,"AR":1.7,"ST":1.7,"TO":1.7,"NT":1.6,"NG":1.6,"SE":1.5,"HA":1.5,"AS":1.5,"OU":1.4,"IO":1.2,"LE":1.2,"VE":1.2}
TRIGRAMS = {"THE":6.0,"AND":5.0,"ING":4.5,"HER":3.7,"ERE":3.2,"ENT":3.2,"THA":3.0,"NTH":2.8,"WAS":2.6,"ETH":2.6,"FOR":2.5,"HAT":2.5,"HIS":2.4,"ION":2.4,"TIO":2.3,"VER":2.2,"TER":2.2,"RES":2.1,"EST":2.1,"ATI":2.1,"OTH":2.0}
WORDS = {"THE","AND","TO","OF","IN","IS","IT","THAT","FOR","ON","WITH","AS","WAS","BE","ARE","THIS","HAVE","FROM","OR","ONE","HAD","NOT","BY","BUT","WHAT","ALL","WERE","WHEN","WE"}

WORD_PATTERN = re.compile(r'[A-Z]+')

# ==========================================
# 2. Helpers
# ==========================================
def decrypt_with_key(cipher, key_list):
    """Decrypts the text using a list of 26 mapped letters."""
    mapping = str.maketrans("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "".join(key_list))
    return cipher.translate(mapping)

def score_text(plain):
    """Scores the plaintext based on English likelihood."""
    sc = 0.0
    t = "".join(c for c in plain if c.isalpha()) # Only letters
    
    # 1. Letter frequencies
    for c in t: sc += L_SCORES.get(c, 0)
        
    # 2. Bigrams & 3. Trigrams
    for i in range(len(t) - 1): sc += BIGRAMS.get(t[i:i+2], 0)
    for i in range(len(t) - 2): sc += TRIGRAMS.get(t[i:i+3], 0)
        
    # 4. Word bonuses
    for w in WORD_PATTERN.findall(plain):
        if w in WORDS: sc += 8.0 + len(w)
            
    # 5. Q penalty (Q must be followed by U)
    for i in range(len(t)):
        if t[i] == 'Q' and (i + 1 >= len(t) or t[i+1] != 'U'):
            sc -= 8.0
            
    return sc

def get_initial_key(cipher):
    """Generates initial key guess based on pure frequency."""
    t = "".join(c for c in cipher if c.isalpha())
    sorted_cipher = [char for char, _ in Counter(t).most_common()]
    
    # Add missing letters to the end
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if c not in sorted_cipher: sorted_cipher.append(c)
            
    EN_FREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ"
    key_list = ['A'] * 26
    for c_char, p_char in zip(sorted_cipher, EN_FREQ):
        key_list[ord(c_char) - 65] = p_char
        
    return key_list

def print_key(key_list):
    print("\nKey mapping (Cipher -> Plain):")
    print("CIPHER: " + " ".join("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
    print("PLAIN : " + " ".join(key_list))

# ==========================================
# 3. Main Algorithm (Simulated Annealing)
# ==========================================
def break_cipher(cipher, restarts=5, steps=30000):
    cipher = cipher.upper()
    base_key = get_initial_key(cipher)
    
    best_key = list(base_key)
    best_plain = decrypt_with_key(cipher, best_key)
    best_score = score_text(best_plain)
    
    print("Working on breaking the cipher (This might take a few seconds)...\n")
    
    for r in range(restarts):
        cur_key = list(base_key)
        
        # Randomize start to escape local maxima
        for _ in range(60):
            a, b = random.sample(range(26), 2)
            cur_key[a], cur_key[b] = cur_key[b], cur_key[a]
            
        cur_plain = decrypt_with_key(cipher, cur_key)
        cur_score = score_text(cur_plain)
        
        T = 20.0 # Initial Temperature
        
        for _ in range(steps):
            nxt_key = list(cur_key)
            a, b = random.sample(range(26), 2)
            nxt_key[a], nxt_key[b] = nxt_key[b], nxt_key[a] # Swap two random letters
            
            nxt_plain = decrypt_with_key(cipher, nxt_key)
            nxt_score = score_text(nxt_plain)
            
            # Simulated Annealing Logic: Accept better scores automatically. 
            # Accept worse scores occasionally based on temperature (prob).
            if nxt_score > cur_score or random.random() < math.exp((nxt_score - cur_score) / T):
                cur_key, cur_score, cur_plain = nxt_key, nxt_score, nxt_plain
                
                # Track global best
                if cur_score > best_score:
                    best_score, best_key, best_plain = cur_score, list(cur_key), cur_plain
                    
            # Cool down the temperature slowly
            T = max(0.05, T * 0.99995)
            
        print(f"Restart {r+1}/{restarts} done. Score = {best_score:.2f}")

    print("\n================ BEST DECRYPTION ================")
    print(best_plain)
    print_key(best_key)

# --- Execution Block ---
if __name__ == "__main__":
    print("Paste ciphertext. (Type 'END' on a new line to finish):")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == "END": break
            lines.append(line)
        except EOFError:
            break
            
    ciphertext = "\n".join(lines)
    
    if ciphertext.strip():
        break_cipher(ciphertext)
    else:
        print("No ciphertext provided!")