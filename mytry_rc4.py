def gener_stream(key, size):
    # Phase 1: Key Schedule Algorithm
    S = [i for i in range(256)]
    j = 0
    
    longueur_cle = len(key)
    
    for i in range(256):
        j = (j + S[i] + key[i % longueur_cle]) % 256
        S[i], S[j] = S[j], S[i]
    
    # Phase 2: Génération du flot pseudo-aléatoire
    i = 0
    j = 0
    flot = []
    
    for _ in range(size):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        octet_chiffrement = S[(S[i] + S[j]) % 256]
        flot.append(octet_chiffrement)
    
    return flot


def chiffrer(data, key):
    if isinstance(data, bytes):
        data = list(data)
    
    flot = gener_stream(key, len(data))
    
    resultat = []
    for octet_message, octet_flot in zip(data, flot):
        resultat.append(octet_message ^ octet_flot)
    
    return bytes(resultat)


def dechiffrer(data, key):
    return chiffrer(data, key)


def chiffrer_message(message, key):
    """Chiffre un message texte et retourne le résultat en hexadécimal"""
    message_bytes = message.encode('utf-8')
    chiffre = chiffrer(message_bytes, key)
    return chiffre.hex()


def dechiffrer_message(message_hex, key):
    """Déchiffre un message hexadécimal et retourne le texte"""
    try:
        chiffre = bytes.fromhex(message_hex)
        dechiffre = dechiffrer(chiffre, key)
        return dechiffre.decode('utf-8')
    except Exception as e:
        return f"Erreur de déchiffrement: {e}"


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


def saisir_cle():
    print("\n" + "=" * 60)
    print("SAISIE DE LA CLÉ")
    print("=" * 60)
    print("Entrez les octets de la clé (valeurs entre 0 et 255)")
    print("Taille recommandée: 16 octets (128 bits) ou 32 octets (256 bits)")
    print("Appuyez sur Entrée sans rien taper pour terminer la saisie\n")
    
    key = []
    while True:
        entree = input(f"Octet {len(key) + 1}: ").strip()
        
        if entree == "":
            if len(key) == 0:
                print("⚠ Erreur: La clé doit contenir au moins 1 octet!\n")
                continue
            break
        
        try:
            octet = int(entree)
            if 0 <= octet <= 255:
                key.append(octet)
                print(f"  → Ajouté: {octet}")
            else:
                print("⚠ Erreur: L'octet doit être entre 0 et 255!\n")
        except ValueError:
            print("⚠ Erreur: Veuillez entrer un nombre entier!\n")
    
    print(f"\n✓ Clé enregistrée: {key}")
    print(f"  Taille: {len(key)} octets ({len(key) * 8} bits)")
    
    return key


def generer_et_afficher_flot(key):
    print("\n" + "=" * 60)
    print("GÉNÉRATION DU FLOT PSEUDO-ALÉATOIRE")
    print("=" * 60)
    
    while True:
        try:
            taille_flot = int(input("Taille du flot à générer (en octets): "))
            if taille_flot > 0:
                break
            else:
                print("⚠ Erreur: La taille doit être > 0!\n")
        except ValueError:
            print("⚠ Erreur: Veuillez entrer un nombre entier!\n")
    
    flot = gener_stream(key, taille_flot)
    
    print(f"\n✓ Flot généré ({taille_flot} octets):")
    print(f"\nHexadécimal:")
    print(f"  {bytes(flot).hex()}")
    print(f"\nPremiers octets (max 20):")
    print(f"  {flot[:min(20, len(flot))]}")


def menu_message(key):
    """Menu pour chiffrer/déchiffrer des messages texte"""
    while True:
        print("\n" + "=" * 60)
        print("CHIFFREMENT/DÉCHIFFREMENT DE MESSAGES")
        print("=" * 60)
        print("1. Chiffrer un message")
        print("2. Déchiffrer un message")
        print("3. Retour au menu principal")
        
        choix = input("\nVotre choix: ").strip()
        
        if choix == "1":
            print("\n--- Chiffrement de message ---")
            message = input("Entrez le message à chiffrer: ")
            chiffre = chiffrer_message(message, key)
            print(f"\n✓ Message chiffré (hexadécimal):")
            print(f"  {chiffre}")
        
        elif choix == "2":
            print("\n--- Déchiffrement de message ---")
            message_hex = input("Entrez le message chiffré (hexadécimal): ").strip()
            dechiffre = dechiffrer_message(message_hex, key)
            print(f"\n✓ Message déchiffré:")
            print(f"  {dechiffre}")
        
        elif choix == "3":
            break
        
        else:
            print("⚠ Choix invalide!")


def menu_fichier(key):
    """Menu pour chiffrer/déchiffrer des fichiers"""
    while True:
        print("\n" + "=" * 60)
        print("CHIFFREMENT/DÉCHIFFREMENT DE FICHIERS")
        print("=" * 60)
        print("1. Chiffrer un fichier")
        print("2. Déchiffrer un fichier")
        print("3. Retour au menu principal")
        
        choix = input("\nVotre choix: ").strip()
        
        if choix == "1":
            print("\n--- Chiffrement de fichier ---")
            fichier_in = input("Fichier à chiffrer: ").strip()
            fichier_out = input("Fichier de sortie: ").strip()
            try:
                chiffrer_fichier(fichier_in, fichier_out, key)
            except FileNotFoundError:
                print(f"⚠ Erreur: Le fichier '{fichier_in}' n'existe pas!")
            except Exception as e:
                print(f"⚠ Erreur: {e}")
        
        elif choix == "2":
            print("\n--- Déchiffrement de fichier ---")
            fichier_in = input("Fichier à déchiffrer: ").strip()
            fichier_out = input("Fichier de sortie: ").strip()
            try:
                dechiffrer_fichier(fichier_in, fichier_out, key)
            except FileNotFoundError:
                print(f"⚠ Erreur: Le fichier '{fichier_in}' n'existe pas!")
            except Exception as e:
                print(f"⚠ Erreur: {e}")
        
        elif choix == "3":
            break
        
        else:
            print("⚠ Choix invalide!")


# Programme principal
if __name__ == "__main__":
    print("=" * 60)
    print("     RC4 - ALGORITHME DE CHIFFREMENT PAR FLOT")
    print("=" * 60)
    
    # Saisir la clé une seule fois
    key = saisir_cle()
    
    # Menu principal simplifié
    while True:
        print("\n" + "=" * 60)
        print("MENU PRINCIPAL")
        print("=" * 60)
        print("1. Générer et afficher le flot pseudo-aléatoire")
        print("2. Chiffrer/Déchiffrer un message")
        print("3. Chiffrer/Déchiffrer un fichier")
        print("4. Changer la clé")
        print("5. Quitter")
        
        choix = input("\nVotre choix: ").strip()
        
        if choix == "1":
            generer_et_afficher_flot(key)
        
        elif choix == "2":
            menu_message(key)
        
        elif choix == "3":
            menu_fichier(key)
        
        elif choix == "4":
            key = saisir_cle()
        
        elif choix == "5":
            print("\n" + "=" * 60)
            print("Programme terminé. Au revoir!")
            print("=" * 60)
            break
        
        else:
            print("⚠ Choix invalide!")