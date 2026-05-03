def mod(a, p):
    return (a % p + p) % p

# def mod_inverse(a, p):
#     a = mod(a, p)
#     for i in range(1, p):
#         if mod(a * i, p) == 1:
#             return i
#     return -1

def mod_inverse(a,p):
    a=mod(a,p)
    if a==0:
        return -1
    return pow(a,p-2,p)

class Point:
    def __init__(self, x=0, y=0, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity

    def __str__(self):
        if self.infinity:
            return "Infinity"
        return f"({self.x}, {self.y})"

def infinity_point():
    return Point(infinity=True)

def point_add(P, Q, a, p):
    if P.infinity:
        return Q
    if Q.infinity:
        return P

    # Point at infinity condition
    if P.x == Q.x and mod(P.y + Q.y, p) == 0:
        return infinity_point()

    # Point doubling (P + P)
    if P.x == Q.x and P.y == Q.y:
        num = mod(3 * P.x * P.x + a, p)
        den = mod_inverse(2 * P.y, p)
        if den == -1: return infinity_point()
        lam = mod(num * den, p)
    # Point addition (P + Q)
    else:
        num = mod(Q.y - P.y, p)
        den = mod_inverse(Q.x - P.x, p)
        if den == -1: return infinity_point()
        lam = mod(num * den, p)

    xr = mod(lam * lam - P.x - Q.x, p)
    yr = mod(lam * (P.x - xr) - P.y, p)
    return Point(xr, yr)

# def is_on_curve(P, a, b, p):
#     """Checks if a point P lies on the elliptic curve y^2 = x^3 + ax + b (mod p)"""
#     if P.infinity:
#         return True # Infinity point তাত্ত্বিকভাবে কার্ভের ওপর থাকে
    
#     # বামপক্ষ (LHS) = y^2 mod p
#     lhs = mod(P.y * P.y, p)
    
#     # ডানপক্ষ (RHS) = (x^3 + ax + b) mod p
#     rhs = mod(P.x**3 + a * P.x + b, p)
    
#     return lhs == rhs

def scalar_multiply(P, k, a, p):
    result = infinity_point()
    addend = P
    while k > 0:
        if k & 1:
            result = point_add(result, addend, a, p)
        addend = point_add(addend, addend, a, p)
        k >>= 1
    return result

def compute_order(G, a, p):
    """Calculates the order 'n' of a generator point G."""
    temp = G
    n = 1
    # Keep adding G to itself until it reaches the point at infinity
    while not temp.infinity:
        temp = point_add(temp, G, a, p)
        n += 1
    return n

def solve_ecdh(alpha, beta, p, a, G_point, sample_num):
    print(f"--- Sample {sample_num} Calculation ---")
    
    # Alline-এর পাবলিক কী গণনা
    Pa = scalar_multiply(G_point, alpha, a, p)
    print(f"Alline's Public Key (Pa): {alpha} * {G_point} = {Pa}")

    # Bose-এর পাবলিক কী গণনা
    Pb = scalar_multiply(G_point, beta, a, p)
    print(f"Bose's Public Key (Pb)  : {beta} * {G_point} = {Pb}")

    # শেয়ারড সিক্রেট কী (K) গণনা
    K_alline = scalar_multiply(Pb, alpha, a, p)
    K_bose = scalar_multiply(Pa, beta, a, p)

    print(f"Alline calculates K: {alpha} * {Pb} = {K_alline}")
    print(f"Bose calculates K  : {beta} * {Pa} = {K_bose}")
    
    if str(K_alline) == str(K_bose):
        print(f"Result: Verified! Shared Secret Key K = {K_alline}\n")
    else:
        print("Result: Failed! Keys do not match.\n")
def ecc_decrypt(C1, C2, private_key, a, p):
    # ১. nB * C1 বের করা
    nb_c1 = scalar_multiply(C1, private_key, a, p)
    
    # ২. nB * C1 এর নেগেটিভ পয়েন্ট বের করা (x, -y)
    nb_c1_neg = Point(nb_c1.x, mod(-nb_c1.y, p))
    
    # ৩. P_M = C2 + (-nb_c1)
    recovered_Pm = point_add(C2, nb_c1_neg, a, p)
    return recovered_Pm
# ================= Main Program =================
def main():
    # ==========================================
    # GIVEN PARAMETERS
    # ==========================================
    p = 17
    a = 1
    # b = 2 (Implicit, not needed for addition math)
    G = Point(9, 3)
    P_M = Point(13, 6)
    k = 10
    P_B = Point(10, 3)
    
    
    p1 = 751
    a1 = -1
    G1 = Point(0, 376)
    P_M1 = Point(443, 253)
    k1 = 111
    P_B1 = Point(318, 79)
    
    

    print(f"--- ECC Calculations for E_{p}({a}, 2) ---")

    # 1. Calculate G + P_M
    G_plus_PM = point_add(G, P_M, a, p)
    print("\n1. Calculating G + P_M:")
    print(f"   {G} + {P_M} = {G_plus_PM}")

    # 2. Calculate Ciphertext P_C = [kG, P_M + kP_B]
    print("\n2. Calculating Ciphertext P_C:")

    kG = scalar_multiply(G, k, a, p)
    print(f"   Part 1 (kG)   : {k} * {G} = {kG}")

    kP_B = scalar_multiply(P_B, k, a, p)
    print(f"   Step 2a (kP_B): {k} * {P_B} = {kP_B}")

    P_M_plus_kP_B = point_add(P_M, kP_B, a, p)
    print(f"   Part 2 (P_M + kP_B): {P_M} + {kP_B} = {P_M_plus_kP_B}")

    print(f"\nFINAL ANSWER:")
    print(f"   P_C = [{kG}, {P_M_plus_kP_B}]")
    
    print(f"--- ECC Calculations for E_{p1}({a1}, 188) ---")
    

    # print(f"\n--- Verifying P_M1 on Curve E_{p1}({a1}, {b1}) ---")
    # if is_on_curve(P_M1, a1, b1, p1):
    #     print(f"Result: SUCCESS! Point {P_M1} is on the curve.")
    # else:
    #     print(f"Result: FAILED! Point {P_M1} is NOT on the curve.")
    
    
    # 1. Calculate Order n
    print("\n1. Calculating Order n (This might take a moment...):")
    n = compute_order(G1, a1, p1)
    print(f"   Result: n = {n}")
    
    
    print("\n2. Calculating Ciphertext P_C:")

    kG1 = scalar_multiply(G1, k1, a1, p1)
    print(f"   Part 1 (kG1)   : {k1} * {G1} = {kG1}")

    kP_B1 = scalar_multiply(P_B1, k1, a1, p1)
    print(f"   Step 2a (kP_B1): {k1} * {P_B1} = {kP_B1}")

    P_M_plus_kP_B1 = point_add(P_M1, kP_B1, a1, p1)
    print(f"   Part 2 (P_M1 + kP_B1): {P_M1} + {kP_B1} = {P_M_plus_kP_B1}")

    print(f"\nFINAL ANSWER:")
    print(f"   P_C1 = [{kG1}, {P_M_plus_kP_B1}]")
    
    solve_ecdh(7, 5, p, a, G, 1)
    # ধরো প্রাইভেট কি n_B = 7
    private_key_B = 7 
    C1 = kG
    C2 = P_M_plus_kP_B

    decrypted_point = ecc_decrypt(C1, C2, private_key_B, a, p)
    print(f"Decrypted Point: {decrypted_point}") # এটি (13, 6) আউটপুট দেবে
    

if __name__ == "__main__":
    main()