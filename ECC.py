
def mod(a, p):
    return (a % p + p) % p

def mod_inverse(a, p):
    a = mod(a, p)
    for i in range(1, p):
        if mod(a * i, p) == 1:
            return i
    return -1

class Point:
    def __init__(self, x=0, y=0, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity

    def __str__(self):
        if self.infinity:
            return "Infinity"
        return f"({self.x},{self.y})"

def infinity_point():
    return Point(infinity=True)

def is_on_curve(P, a, b, p):
    if P.infinity:
        return True
    return mod(P.y * P.y, p) == mod(P.x * P.x * P.x + a * P.x + b, p)

def point_add(P, Q, a, p):
    if P.infinity:
        return Q
    if Q.infinity:
        return P

    if P.x == Q.x and mod(P.y + Q.y, p) == 0:
        return Point(infinity=True)

    if P.x == Q.x and P.y == Q.y:
        num = mod(3 * P.x * P.x + a, p)
        den = pow(2*P.y, p-2, p)
        lam = mod(num * den, p)
    else:
        num = mod(Q.y - P.y, p)
        den = mod_inverse(Q.x - P.x, p)
        lam = mod(num * den, p)

    xr = mod(lam * lam - P.x - Q.x, p)
    yr = mod(lam * (P.x - xr) - P.y, p)
    return Point(xr, yr)

def scalar_multiply(P, k, a, p):
    result = infinity_point()
    while k > 0:
        if k & 1:
            result = point_add(result, P, a, p)
        P = point_add(P, P, a, p)
        k >>= 1
    return result

def compute_order(G, a, p):
    temp = G
    n = 1
    while not temp.infinity:
        temp = point_add(temp, G, a, p)
        n += 1
    return n

def find_affine_points(a, b, p):
    points = []
    for x in range(p):
        rhs = mod(x**3 + a*x + b, p)
        for y in range(p):
            if mod(y*y, p) == rhs:
                points.append(Point(x, y))
    return points

def xor_encrypt_decrypt(msg, key):
    return ''.join(chr(ord(c) ^ (key % 256)) for c in msg)

# ================= Main Program =================
def main():
    a = int(input("Enter curve parameter a: "))
    b = int(input("Enter curve parameter b: "))
    p = int(input("Enter prime p: "))

    if mod(4*a*a*a + 27*b*b, p) == 0:
        print("Invalid curve!")
        return

    # Display all affine points
    points = find_affine_points(a, b, p)
    print("\nAffine points on curve:")
    for pt in points:
        print(pt, end=" ")
    print(f"\nTotal points: {len(points)}\n")

    # Generator input
    while True:
        gx = int(input("Enter Generator Gx: "))
        gy = int(input("Enter Generator Gy: "))
        G = Point(gx, gy)
        if is_on_curve(G, a, b, p):
            break
        print("Point is NOT on curve. Try again.")

    n = compute_order(G, a, p)
    print(f"Order of Generator (n) = {n}")

    # Private keys
    alpha = int(input(f"Enter Alice private key (1 <= alpha < {n}): "))
    beta = int(input(f"Enter Bob private key (1 <= beta < {n}): "))

    # Public keys
    PA = scalar_multiply(G, alpha, a, p)
    PB = scalar_multiply(G, beta, a, p)

    print(f"\nAlice Public Key: {PA}")
    print(f"Bob Public Key: {PB}")

    # Shared secret
    sharedA = scalar_multiply(PB, alpha, a, p)
    sharedB = scalar_multiply(PA, beta, a, p)

    print(f"\nShared Secret (Alice): {sharedA}")
    print(f"Shared Secret (Bob):   {sharedB}")

    if sharedA.x == sharedB.x and sharedA.y == sharedB.y:
        print("\nKey Exchange Successful!")
    else:
        print("\nKey Exchange Failed!")
        return

    symmetric_key = sharedA.x

    message = input("\nEnter Message: ")
    encrypted = xor_encrypt_decrypt(message, symmetric_key)
    print(f"Encrypted: {encrypted}")
    decrypted = xor_encrypt_decrypt(encrypted, symmetric_key)
    print(f"Decrypted: {decrypted}")

if __name__ == "__main__":
    main()