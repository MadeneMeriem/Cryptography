import random

def mod_inverse(a, p):
   
    if a < 0:
        a = (a % p + p) % p
    
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a % p, p)
    if gcd != 1:
        raise Exception('Modular inverse does not exist')
    return (x % p + p) % p


def ShamirShare(s, k, n):
   
    p = 257
    coefficients = [s]
    
    if k == 3:  
        coefficients.append(1) 
        coefficients.append(9)  
    else:
        for i in range(1, k):
            coefficients.append(random.randint(1, p-1))
    

    shares = []
    for x in range(1, n + 1):

        y = 0
        for i, coef in enumerate(coefficients):
            y += coef * (x ** i)
        y = y % p
        shares.append((x, y))
    
    return shares


def ShamirReconstruct(shares):
   
   
    p = 257  
    k = len(shares)  
    
    
    secret = 0
    
    for i in range(k):
        x_i, y_i = shares[i]
        

        numerator = 1
        denominator = 1
        
        for j in range(k):
            if i != j:
                x_j = shares[j][0]

                numerator = (numerator * (-x_j)) % p
                denominator = (denominator * (x_i - x_j)) % p
    
    
        lagrange_basis = (numerator * mod_inverse(denominator, p)) % p
        

        secret = (secret + y_i * lagrange_basis) % p
    
    return secret


# Parameters
s = 7
k = 3
n = 5

print("Partage de clé shamir")
print("-----------------------------------------")
print("les parametres : s=7, k=3, n=5, p=257 (choisis dans le code)")
print("-----------------------------------------\n")
print("polynom: f(x) = 7 + 1x + 9x^2 (mod 257)\n")


# Generate shares
shares = ShamirShare(s, k, n)
print("Les parties distrubuée:")
print(f"président: {shares[0]}, {shares[1]}")
print(f"membres: {shares[2]}, {shares[3]}, {shares[4]}\n")

# Reconstruct - Case 1
shares_case1 = [shares[2], shares[3], shares[4]]
secret1 = ShamirReconstruct(shares_case1)
print(f"cas 1, 3 membres: {shares_case1}")
print(f"secret reconstruié: {secret1}\n")

# Reconstruct - Case 2
shares_case2 = [shares[0], shares[1], shares[2]]
secret2 = ShamirReconstruct(shares_case2)
print(f"cas 2, 2 membres (président + 1 membre): {shares_case2}")
print(f"secret reconstruié: {secret2}\n")

# Verify
print(f"secret initial: {s}")