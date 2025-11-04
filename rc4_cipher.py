def gener_stream(key, size):
    # Phase 1: Key Schedule Algorithm
    S = [i for i in range(256)]  # S[i] := i
    j = 0
    
    longueur_cle = len(key)
    
    for i in range(256):
        j = (j + S[i] + key[i % longueur_cle]) % 256
        # échanger(S[i], S[j])
        S[i], S[j] = S[j], S[i]
    
    # Phase 2: Génération du flot pseudo-aléatoire
    i = 0
    j = 0
    flot = []
    
    for _ in range(size):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        # échanger(S[i], S[j])
        S[i], S[j] = S[j], S[i]
        # octet_chiffrement = S[(S[i] + S[j]) mod 256]
        octet_chiffrement = S[(S[i] + S[j]) % 256]
        flot.append(octet_chiffrement)
        
    
    return flot


def chiffrer(data, key):

    if isinstance(data, bytes):
        data = list(data)
    
    # Générer le flot de la même taille que les données
    flot = gener_stream(key, len(data))
    
    # XOR avec le message
    resultat = []
    for octet_message, octet_flot in zip(data, flot):
        resultat.append(octet_message ^ octet_flot)
    
    return bytes(resultat)


def dechiffrer(data, key):
    
    return chiffrer(data, key)


def chiffrer_fichier(fichier_entree, fichier_sortie, key):
    with open(fichier_entree, 'rb') as f:
        contenu = f.read()
    
    chiffre = chiffrer(contenu, key)
    
    with open(fichier_sortie, 'wb') as f:
        f.write(chiffre)
    
    print(f"✓ Fichier chiffré: {fichier_entree} -> {fichier_sortie}")


def dechiffrer_fichier(fichier_entree, fichier_sortie, key):

    with open(fichier_entree, 'rb') as f:
        contenu = f.read()
    
    dechiffre = dechiffrer(contenu, key)
    
    with open(fichier_sortie, 'wb') as f:
        f.write(dechiffre)
    
    print(f"✓ Fichier déchiffré: {fichier_entree} -> {fichier_sortie}")


# Programme principal
if __name__ == "__main__":
    print("=" * 60)
    print("  RC4 - Implémentation de l'algorithme de chiffrement par flot")
    print("=" * 60)
    
    # Demander la clé octet par octet
    print("\n--- Saisie de la clé ---")
    print("Entrez les octets de la clé (valeurs entre 0 et 255)")
    print("Taille recommandée: 16 octets (128 bits) ou 32 octets (256 bits)")
    
    key = []
    while True:
        entree = input(f"Octet {len(key) + 1} (ou appuyez sur Entrée pour terminer): ").strip()
        
        if entree == "":
            if len(key) == 0:
                print("Erreur: La clé doit contenir au moins 1 octet!")
                continue
            break
        
        try:
            octet = int(entree)
            if 0 <= octet <= 255:
                key.append(octet)
                print(f"  → Octet ajouté: {octet}")
            else:
                print("Erreur: L'octet doit être entre 0 et 255!")
        except ValueError:
            print("Erreur: Veuillez entrer un nombre entier!")
    
    print(f"\n✓ Clé enregistrée: {key}")
    print(f"  Taille: {len(key)} octets ({len(key) * 8} bits)")
    
    # Demander la taille du flot
    print("\n--- Génération du flot pseudo-aléatoire ---")
    while True:
        try:
            taille_flot = int(input("Taille du flot à générer (en octets): "))
            if taille_flot > 0:
                break
            else:
                print("Erreur: La taille doit être > 0!")
        except ValueError:
            print("Erreur: Veuillez entrer un nombre entier!")
    
    # Générer et afficher le flot
    flot = gener_stream(key, taille_flot)
    print(f"\n✓ Flot généré ({taille_flot} octets):")
    print(f"  Hexadécimal: {bytes(flot).hex()}")
    print(f"  Premiers octets: {flot[:min(20, len(flot))]}")
    
    # Menu pour chiffrement/déchiffrement de fichiers
    print("\n" + "=" * 60)
    print("--- Chiffrement/Déchiffrement de fichiers ---")
    print("1. Chiffrer un fichier")
    print("2. Déchiffrer un fichier")
    print("3. Test rapide (créer et chiffrer un fichier de test)")
    print("4. Quitter")
    
    choix = input("\nVotre choix: ").strip()
    
    if choix == "1":
        fichier_in = input("Nom du fichier à chiffrer: ").strip()
        fichier_out = input("Nom du fichier de sortie: ").strip()
        try:
            chiffrer_fichier(fichier_in, fichier_out, key)
        except FileNotFoundError:
            print(f"Erreur: Le fichier '{fichier_in}' n'existe pas!")
        except Exception as e:
            print(f"Erreur: {e}")
    
    elif choix == "2":
        fichier_in = input("Nom du fichier à déchiffrer: ").strip()
        fichier_out = input("Nom du fichier de sortie: ").strip()
        try:
            dechiffrer_fichier(fichier_in, fichier_out, key)
        except FileNotFoundError:
            print(f"Erreur: Le fichier '{fichier_in}' n'existe pas!")
        except Exception as e:
            print(f"Erreur: {e}")
    
    elif choix == "3":
        print("\n--- Test rapide ---")
        # Créer un fichier de test
        contenu_test = b"Ceci est un message secret pour tester RC4!\nLigne 2\nLigne 3"
        with open("test_message.txt", "wb") as f:
            f.write(contenu_test)
        print("✓ Fichier de test créé: test_message.txt")
        
        # Chiffrer
        chiffrer_fichier("test_message.txt", "test_chiffre.bin", key)
        
        # Déchiffrer
        dechiffrer_fichier("test_chiffre.bin", "test_dechiffre.txt", key)
        
        # Vérifier
        with open("test_dechiffre.txt", "rb") as f:
            contenu_dechiffre = f.read()
        
        if contenu_test == contenu_dechiffre:
            print("\n✓ TEST RÉUSSI: Le déchiffrement a restauré le message original!")
        else:
            print("\n✗ TEST ÉCHOUÉ: Le message déchiffré est différent!")
    
    print("\n" + "=" * 60)
    print("Programme terminé.")
    print("=" * 60)