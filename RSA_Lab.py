import math

# ল্যাব শিটে বলা হয়েছে gcd(e, phi) = 1 হতে হবে। 
# তোমার রেফারেন্স কোডেও math.gcd ব্যবহার করা হয়েছে, যা এখানে কার্যকর।

def solve_lab_assignment():
    print("--- RSA Public Exponent Verifier ---")
    
    while True:
        try:
            # ইনপুট ফরম্যাট: p q n (p, q হলো প্রাইম এবং n হলো কতটি e চেক করতে হবে)
            line = input().split()
            if not line:
                continue
            
            p = int(line[0])
            q = int(line[1])
            n_candidates = int(line[2])

            # ইনপুট শেষ করার শর্ত: 0 0 0
            if p == 0 and q == 0 and n_candidates == 0:
                break

            # তোমার রেফারেন্স কোডের মতো phi গণনা
            phi = (p - 1) * (q - 1)

            # n সংখ্যক ক্যান্ডিডেট এক্সপোনেন্ট চেক করা
            for _ in range(n_candidates):
                try:
                    e = int(input())
                    
                    # ল্যাব শিটের শর্ত অনুযায়ী ভ্যালিডেশন:
                    # ১. 1 < e < phi(n)
                    # ২. gcd(e, phi(n)) == 1
                    if 1 < e < phi and math.gcd(e, phi) == 1:
                        print("YES")
                    else:
                        print("NO")
                except ValueError:
                    continue
            
            # টেস্ট কেস শেষে একটি খালি লাইন (ল্যাব শিট অনুযায়ী)
            print()

        except EOFError:
            break
        except Exception as e_msg:
            print(f"Error: {e_msg}")
            break

if __name__ == "__main__":
    solve_lab_assignment()