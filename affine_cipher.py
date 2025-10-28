"""
Affine Cipher Implementation
=============================
An implementation of the Affine cipher with support for the French alphabet (A-Z + space).

The Affine cipher is a type of monoalphabetic substitution cipher where each letter 
is encrypted using a mathematical function: C = (a*M + b) mod 27

Author: [Your Name]
License: MIT
"""

def pgcd(a, b):
    """
    Calculate the Greatest Common Divisor (GCD) using Euclidean algorithm.
    
    Args:
        a (int): First number
        b (int): Second number
    
    Returns:
        int: GCD of a and b
    
    Example:
        >>> pgcd(15, 27)
        3
    """
    while b != 0:
        a, b = b, a % b
    return a


def euclide_etendu(a, m):
    """
    Extended Euclidean Algorithm to find GCD and Bézout coefficients.
    
    This function finds integers x and y such that: a*x + m*y = gcd(a, m)
    
    Args:
        a (int): First number
        m (int): Second number (modulus)
    
    Returns:
        tuple: (gcd, x, y) where gcd is the GCD and x, y are Bézout coefficients
    
    Example:
        >>> euclide_etendu(5, 27)
        (1, 11, -2)  # Because 5*11 + 27*(-2) = 1
    """
    if m == 0:
        return a, 1, 0
    
    gcd, x1, y1 = euclide_etendu(m, a % m)
    x = y1
    y = x1 - (a // m) * y1
    
    return gcd, x, y


def inverse_modulaire(a, m):
    """
    Calculate the modular multiplicative inverse of a modulo m.
    
    The modular inverse a^(-1) is a number such that: (a * a^(-1)) mod m = 1
    This only exists if gcd(a, m) = 1
    
    Args:
        a (int): The number to find the inverse of
        m (int): The modulus
    
    Returns:
        int or None: The modular inverse if it exists, None otherwise
    
    Example:
        >>> inverse_modulaire(5, 27)
        11  # Because (5 * 11) mod 27 = 1
    """
    gcd, x, y = euclide_etendu(a, m)
    
    if gcd != 1:
        return None  # Inverse doesn't exist
    
    return (x % m + m) % m


def chiffrer_affine(message, a, b):
    """
    Encrypt a message using the Affine cipher.
    
    Formula: C = (a * M + b) mod 27
    Where:
        - M is the position of the plaintext letter (A=0, B=1, ..., Z=25, space=26)
        - C is the position of the ciphertext letter
        - a and b are the encryption keys
    
    Args:
        message (str): The plaintext message to encrypt
        a (int): Multiplicative key (must be coprime with 27)
        b (int): Additive key
    
    Returns:
        str or None: Encrypted message, or None if 'a' is not valid
    
    Example:
        >>> chiffrer_affine("HELLO WORLD", 5, 8)
        'RCLLA FADYN'
    """
    # Check if 'a' is coprime with 27 (required for decryption to work)
    if pgcd(a, 27) != 1:
        print(f"ERREUR: a = {a} n'est pas inversible modulo 27")
        return None

    resultat = ""
    message = message.upper()

    for lettre in message:
        # Handle space character (position 26)
        if lettre == ' ':
            M = 26 
        # Handle letters A-Z (positions 0-25)
        elif 'A' <= lettre <= 'Z':
            M = ord(lettre) - ord('A')
        # Keep non-alphabetic characters unchanged
        else:
            resultat += lettre
            continue

        # Apply Affine cipher formula
        C = (a * M + b) % 27

        # Convert back to character
        if C == 26:
            lettre_chiffree = ' '
        else:
            lettre_chiffree = chr(C + ord('A'))

        resultat += lettre_chiffree

    return resultat


def dechiffrer_affine(message_chiffre, a, b):
    """
    Decrypt a message encrypted with the Affine cipher.
    
    Formula: M = a^(-1) * (C - b) mod 27
    Where:
        - C is the position of the ciphertext letter
        - M is the position of the plaintext letter
        - a^(-1) is the modular multiplicative inverse of a
        - b is the additive key
    
    Args:
        message_chiffre (str): The encrypted message to decrypt
        a (int): Multiplicative key (must be coprime with 27)
        b (int): Additive key
    
    Returns:
        str or None: Decrypted message, or None if 'a' is not valid
    
    Example:
        >>> dechiffrer_affine("RCLLA FADYN", 5, 8)
        'HELLO WORLD'
    """
    # Calculate the modular inverse of 'a'
    a_inv = inverse_modulaire(a, 27)
    
    if a_inv is None:
        print(f"\nERREUR: a = {a} n'est pas inversible modulo 27")
        return None
    
    resultat = ""
    message_chiffre = message_chiffre.upper()
    
    for lettre in message_chiffre:
        # Handle space character (position 26)
        if lettre == ' ':
            C = 26
        # Handle letters A-Z (positions 0-25)
        elif 'A' <= lettre <= 'Z':
            C = ord(lettre) - ord('A')
        # Keep non-alphabetic characters unchanged
        else:
            resultat += lettre
            continue

        # Apply Affine decipher formula
        M = (a_inv * (C - b)) % 27

        # Convert back to character
        if M == 26:
            lettre_dechiffree = ' '
        else:
            lettre_dechiffree = chr(M + ord('A'))

        resultat += lettre_dechiffree
    
    return resultat


def main():
    """
    Main function providing an interactive menu for encryption and decryption.
    
    This function creates a command-line interface where users can:
    1. Encrypt messages using custom keys
    2. Decrypt messages using known keys
    3. Exit the program
    """
    print("="*60)
    print("         CHIFFREMENT AFFINE - Alphabet {A, B, ..., Z, espace}")
    print("="*60)
    print("\nFormules:")
    print("  Chiffrement   : C = (a * M + b) mod 27")
    print("  Déchiffrement : M = a^(-1) * (C - b) mod 27")
    print("\nCondition: a doit être inversible modulo 27")
    print("           c'est-à-dire PGCD(a, 27) = 1")
    print("="*60)
    
    while True:
        print("\n" + "-"*60)
        print("MENU PRINCIPAL")
        print("-"*60)
        print("1. Chiffrer un message")
        print("2. Déchiffrer un message")
        print("3. Quitter")
        print("-"*60)
        
        choix = input("\nVotre choix (1, 2 ou 3): ")
        
        if choix == "3":
            print("\nAu revoir!")
            break
        
        if choix not in ["1", "2"]:
            print("\nChoix invalide! Veuillez choisir 1, 2 ou 3.")
            continue
        
        # Get encryption/decryption keys from user
        print("\n--- Entrez la clé (a, b) ---")
        try:
            a = int(input("Valeur de a: "))
            b = int(input("Valeur de b: "))
        except ValueError:
            print("\nERREUR: Veuillez entrer des nombres entiers!")
            continue
        
        # Validate that 'a' is coprime with 27
        if pgcd(a, 27) != 1:
            print(f"\nATTENTION: a = {a} n'est pas inversible modulo 27!")
            print(f"PGCD({a}, 27) = {pgcd(a, 27)}")
            print("Veuillez choisir un autre a.")
            continue
        
        # Get message from user
        message = input("\nEntrez le message: ")
        
        # Encryption mode
        if choix == "1":
            print("\n--- CHIFFREMENT ---")
            resultat = chiffrer_affine(message, a, b)
            if resultat:
                print(f"\nClé utilisée: a = {a}, b = {b}")
                print(f"Message original  : {message}")
                print(f"Message chiffré   : {resultat}")
        
        # Decryption mode
        elif choix == "2":
            print("\n--- DÉCHIFFREMENT ---")
            a_inv = inverse_modulaire(a, 27)
            resultat = dechiffrer_affine(message, a, b)
            if resultat:
                print(f"\nClé utilisée: a = {a}, b = {b}")
                print(f"Inverse de a modulo 27: a^(-1) = {a_inv}")
                print(f"Message chiffré   : {message}")
                print(f"Message déchiffré : {resultat}")


if __name__ == "__main__":
    main()
