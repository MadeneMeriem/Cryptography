"""
Hill Cipher Implementation
==========================
An implementation of the Hill cipher using matrix operations in modular arithmetic (mod 27).

The Hill cipher is a polygraphic substitution cipher based on linear algebra.
It encrypts blocks of letters using matrix multiplication.

Author: [Your Name]
License: MIT
"""

import random
import math


def pgcd(a, b):
    """
    Calculate the Greatest Common Divisor (GCD) using Euclidean algorithm.
    
    Args:
        a (int): First number
        b (int): Second number
    
    Returns:
        int: GCD of a and b
    """
    while b != 0:
        a, b = b, a % b
    return a


def inverse_modulaire(a, m):
    """
    Calculate the modular multiplicative inverse of a modulo m using Extended Euclidean Algorithm.
    
    Args:
        a (int): The number to find the inverse of
        m (int): The modulus
    
    Returns:
        int or None: The modular inverse if it exists, None otherwise
    """
    if pgcd(a, m) != 1:
        return None
    
    # Extended Euclidean Algorithm
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    
    return x1 % m0 if x1 > 0 else x1 % m0 + m0


def creer_matrice_identite(n):
    """
    Create an identity matrix of size n x n.
    
    Args:
        n (int): Size of the matrix
    
    Returns:
        list: Identity matrix as a 2D list
    """
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def copier_matrice(matrice):
    """
    Create a deep copy of a matrix.
    
    Args:
        matrice (list): Matrix to copy
    
    Returns:
        list: Copy of the matrix
    """
    return [ligne[:] for ligne in matrice]


def afficher_matrice(matrice, nom="Matrice"):
    """
    Display a matrix in a readable format.
    
    Args:
        matrice (list): Matrix to display
        nom (str): Name/label for the matrix
    """
    print(f"\n{nom}:")
    for ligne in matrice:
        print("  [ " + "  ".join(f"{x:3}" for x in ligne) + " ]")


def inverser_matrice_mod27(matrice):
    """
    Invert a matrix modulo 27 using Gauss-Jordan elimination.
    
    This function uses the Gauss-Jordan method adapted for modular arithmetic.
    It creates an augmented matrix [A|I] and transforms it to [I|A^(-1)].
    
    Args:
        matrice (list): Square matrix to invert (2D list)
    
    Returns:
        list or None: Inverse matrix if it exists, None otherwise
    
    Algorithm:
        1. Create augmented matrix [A|I]
        2. For each column, find a pivot with a modular inverse
        3. Scale the pivot row
        4. Eliminate other rows
        5. Extract the inverse from the right side
    """
    n = len(matrice)
    
    # Create augmented matrix [A | I]
    augmentee = [matrice[i][:] + creer_matrice_identite(n)[i] for i in range(n)]
    
    # Gauss-Jordan elimination
    for col in range(n):
        # Find a pivot row with an invertible element
        pivot_row = -1
        for row in range(col, n):
            element = augmentee[row][col] % 27
            if pgcd(element, 27) == 1:  # Element is invertible mod 27
                pivot_row = row
                break
        
        # If no valid pivot found, matrix is not invertible
        if pivot_row == -1:
            return None
        
        # Swap rows if necessary
        if pivot_row != col:
            augmentee[col], augmentee[pivot_row] = augmentee[pivot_row], augmentee[col]
        
        # Get the pivot element and its inverse
        pivot = augmentee[col][col] % 27
        pivot_inv = inverse_modulaire(pivot, 27)
        
        if pivot_inv is None:
            return None
        
        # Scale the pivot row to make pivot = 1
        for j in range(2 * n):
            augmentee[col][j] = (augmentee[col][j] * pivot_inv) % 27
        
        # Eliminate other rows
        for row in range(n):
            if row != col:
                factor = augmentee[row][col] % 27
                for j in range(2 * n):
                    augmentee[row][j] = (augmentee[row][j] - factor * augmentee[col][j]) % 27
    
    # Extract the inverse matrix from the right side
    inverse = [[augmentee[i][j + n] % 27 for j in range(n)] for i in range(n)]
    
    return inverse


def generer_matrice_inversible(n, max_tentatives=100):
    """
    Generate a random invertible matrix of size n x n modulo 27.
    
    This function generates random matrices and tests their invertibility.
    If a matrix is not invertible, it generates a new one.
    
    Args:
        n (int): Size of the matrix
        max_tentatives (int): Maximum number of attempts to find an invertible matrix
    
    Returns:
        tuple or None: (matrix, inverse_matrix) if successful, None otherwise
    """
    for tentative in range(max_tentatives):
        # Generate random matrix with values between 0 and 26
        matrice = [[random.randint(0, 26) for _ in range(n)] for _ in range(n)]
        
        # Try to invert it
        inverse = inverser_matrice_mod27(matrice)
        
        if inverse is not None:
            print(f"\n✓ Matrice inversible trouvée après {tentative + 1} tentative(s)")
            return matrice, inverse
    
    print(f"\n✗ Aucune matrice inversible trouvée après {max_tentatives} tentatives")
    return None


def multiplier_matrice_vecteur_mod27(matrice, vecteur):
    """
    Multiply a matrix by a vector modulo 27.
    
    Args:
        matrice (list): Matrix (2D list)
        vecteur (list): Vector (1D list)
    
    Returns:
        list: Result vector
    """
    n = len(matrice)
    resultat = []
    
    for i in range(n):
        somme = 0
        for j in range(n):
            somme += matrice[i][j] * vecteur[j]
        resultat.append(somme % 27)
    
    return resultat


def texte_vers_nombres(texte):
    """
    Convert text to list of numbers (A=0, B=1, ..., Z=25, space=26).
    
    Args:
        texte (str): Input text
    
    Returns:
        list: List of numbers
    """
    texte = texte.upper()
    nombres = []
    
    for char in texte:
        if char == ' ':
            nombres.append(26)
        elif 'A' <= char <= 'Z':
            nombres.append(ord(char) - ord('A'))
        # Skip non-alphabetic characters
    
    return nombres


def nombres_vers_texte(nombres):
    """
    Convert list of numbers back to text.
    
    Args:
        nombres (list): List of numbers
    
    Returns:
        str: Resulting text
    """
    texte = ""
    
    for num in nombres:
        num = num % 27
        if num == 26:
            texte += ' '
        else:
            texte += chr(num + ord('A'))
    
    return texte


def chiffrer_hill(message, matrice_cle):
    """
    Encrypt a message using the Hill cipher.
    
    The message is divided into blocks (size = matrix dimension).
    Each block is treated as a vector and multiplied by the key matrix.
    
    Args:
        message (str): Plaintext message
        matrice_cle (list): Encryption key matrix
    
    Returns:
        str: Encrypted message
    """
    n = len(matrice_cle)
    nombres = texte_vers_nombres(message)
    
    # Pad message if necessary to make length a multiple of n
    while len(nombres) % n != 0:
        nombres.append(26)  # Add spaces for padding
    
    nombres_chiffres = []
    
    # Process message block by block
    for i in range(0, len(nombres), n):
        bloc = nombres[i:i+n]
        bloc_chiffre = multiplier_matrice_vecteur_mod27(matrice_cle, bloc)
        nombres_chiffres.extend(bloc_chiffre)
    
    return nombres_vers_texte(nombres_chiffres)


def dechiffrer_hill(message_chiffre, matrice_cle_inverse):
    """
    Decrypt a message encrypted with the Hill cipher.
    
    Uses the inverse of the key matrix to decrypt.
    
    Args:
        message_chiffre (str): Encrypted message
        matrice_cle_inverse (list): Inverse of the encryption key matrix
    
    Returns:
        str: Decrypted message
    """
    # Decryption is the same as encryption but using the inverse matrix
    return chiffrer_hill(message_chiffre, matrice_cle_inverse)


def main():
    """
    Main function providing an interactive menu for Hill cipher operations.
    """
    print("="*70)
    print("           CHIFFREMENT DE HILL - Matrices modulo 27")
    print("="*70)
    print("\nLe chiffrement de Hill utilise des matrices pour chiffrer des blocs")
    print("de lettres. L'alphabet utilisé: {A-Z, espace} = 27 caractères")
    print("="*70)
    
    matrice_cle = None
    matrice_inverse = None
    taille_matrice = None
    
    while True:
        print("\n" + "-"*70)
        print("MENU PRINCIPAL")
        print("-"*70)
        print("1. Générer une nouvelle matrice de chiffrement")
        print("2. Chiffrer un message")
        print("3. Déchiffrer un message")
        print("4. Afficher la matrice actuelle")
        print("5. Quitter")
        print("-"*70)
        
        choix = input("\nVotre choix (1-5): ")
        
        if choix == "5":
            print("\nAu revoir!")
            break
        
        if choix == "1":
            # Generate new key matrix
            print("\n--- GÉNÉRATION DE MATRICE ---")
            try:
                taille = int(input("Taille de la matrice (ex: 2 pour 2x2, 3 pour 3x3): "))
                if taille < 2:
                    print("La taille doit être au moins 2!")
                    continue
            except ValueError:
                print("Veuillez entrer un nombre entier!")
                continue
            
            print(f"\nGénération d'une matrice {taille}x{taille} inversible modulo 27...")
            resultat = generer_matrice_inversible(taille)
            
            if resultat:
                matrice_cle, matrice_inverse = resultat
                taille_matrice = taille
                afficher_matrice(matrice_cle, "Matrice de chiffrement (K)")
                afficher_matrice(matrice_inverse, "Matrice inverse (K^-1)")
                print("\n✓ Matrices générées avec succès!")
            else:
                print("\n✗ Échec de la génération de matrice")
        
        elif choix == "2":
            # Encrypt message
            if matrice_cle is None:
                print("\n⚠ Veuillez d'abord générer une matrice (option 1)")
                continue
            
            print("\n--- CHIFFREMENT ---")
            message = input("Entrez le message à chiffrer: ")
            
            if not message:
                print("Message vide!")
                continue
            
            message_chiffre = chiffrer_hill(message, matrice_cle)
            
            print(f"\nMessage original  : {message}")
            print(f"Message chiffré   : {message_chiffre}")
            print(f"Taille de bloc    : {taille_matrice} caractères")
        
        elif choix == "3":
            # Decrypt message
            if matrice_inverse is None:
                print("\n⚠ Veuillez d'abord générer une matrice (option 1)")
                continue
            
            print("\n--- DÉCHIFFREMENT ---")
            message_chiffre = input("Entrez le message à déchiffrer: ")
            
            if not message_chiffre:
                print("Message vide!")
                continue
            
            message_dechiffre = dechiffrer_hill(message_chiffre, matrice_inverse)
            
            print(f"\nMessage chiffré   : {message_chiffre}")
            print(f"Message déchiffré : {message_dechiffre}")
            print(f"Taille de bloc    : {taille_matrice} caractères")
        
        elif choix == "4":
            # Display current matrices
            if matrice_cle is None:
                print("\n⚠ Aucune matrice n'a été générée")
                continue
            
            print(f"\n--- MATRICES ACTUELLES (taille {taille_matrice}x{taille_matrice}) ---")
            afficher_matrice(matrice_cle, "Matrice de chiffrement (K)")
            afficher_matrice(matrice_inverse, "Matrice inverse (K^-1)")
        
        else:
            print("\n✗ Choix invalide! Veuillez choisir entre 1 et 5.")


if __name__ == "__main__":
    main()