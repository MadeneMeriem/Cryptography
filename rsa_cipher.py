import hashlib
import os


def blake2s_hash(data):
   

    if isinstance(data, str):
        data = data.encode('utf-8')
    

    hash_obj = hashlib.blake2s()
    

    hash_obj.update(data)
    

    return hash_obj.hexdigest()



def hmac_blake2s(key, message):
   
    ipad = bytes([0x36] * 64)  
    opad = bytes([0x5C] * 64)  
    

    if isinstance(key, str):
        key = key.encode('utf-8')
    

    if isinstance(message, str):
        message = message.encode('utf-8')
    

    if len(key) > 64:

        key = bytes.fromhex(blake2s_hash(key))
    

    key = key + bytes(64 - len(key))
    
    # Calculer K ⊕ ipad (XOR entre la clé et ipad)
    key_ipad = bytes([k ^ i for k, i in zip(key, ipad)])
    
    # Calculer K ⊕ opad (XOR entre la clé et opad)
    key_opad = bytes([k ^ o for k, o in zip(key, opad)])
    
    # Calculer le haché interne: BLAKE2((K ⊕ ipad)||m)
    inner_hash = blake2s_hash(key_ipad + message)
    
    # Calculer le haché externe: BLAKE2((K ⊕ opad)||inner_hash)
    outer_hash = blake2s_hash(key_opad + bytes.fromhex(inner_hash))
    

    return outer_hash




def chiffrer_fichier(nom_fichier, mot_de_passe, mode_operation):
    
    # Lire le contenu du fichier
    with open(nom_fichier, 'rb') as f:
        contenu = f.read()
    
    # Dériver une clé de chiffrement du mot de passe avec BLAKE2s
    cle_chiffrement = blake2s_hash(mot_de_passe)
    
    # Simuler le chiffrement (simplifié pour ce TP)
    # Dans une vraie implémentation, utiliser AES-CBC ou AES-CTR
    # Ici, nous XORons avec la clé répétée (juste pour la démonstration)
    cle_bytes = bytes.fromhex(cle_chiffrement)
    
    # Chiffrer en XORant le contenu avec la clé répétée
    contenu_chiffre = bytes([contenu[i] ^ cle_bytes[i % len(cle_bytes)] 
                             for i in range(len(contenu))])
    
    # Calculer le tag d'intégrité avec HMAC-BLAKE2s sur le fichier chiffré
    tag_integrite = hmac_blake2s(cle_chiffrement, contenu_chiffre)
    
    # Sauvegarder le fichier chiffré
    nom_fichier_chiffre = nom_fichier + '.enc'
    with open(nom_fichier_chiffre, 'wb') as f:
        f.write(contenu_chiffre)
    
    # Sauvegarder le tag d'intégrité
    nom_fichier_tag = nom_fichier + '.tag'
    with open(nom_fichier_tag, 'w') as f:
        f.write(tag_integrite)
    
    print(f"✓ Fichier chiffré: {nom_fichier_chiffre}")
    print(f"✓ Tag d'intégrité: {nom_fichier_tag}")
    print(f"✓ Mode: {mode_operation}")
    
    return nom_fichier_chiffre, tag_integrite


# ========== OBJECTIF 4: Déchiffrement du fichier ==========

def dechiffrer_fichier(nom_fichier_chiffre, mot_de_passe, tag_attendu):
    """
    Déchiffre un fichier et vérifie son intégrité avec HMAC
    
    Args:
        nom_fichier_chiffre: chemin du fichier chiffré
        mot_de_passe: mot de passe pour générer la clé
        tag_attendu: tag d'intégrité attendu
    
    Returns:
        bool: True si succès, False sinon
    """
    # Lire le fichier chiffré
    with open(nom_fichier_chiffre, 'rb') as f:
        contenu_chiffre = f.read()
    
    # Dériver la clé de chiffrement du mot de passe avec BLAKE2s
    cle_chiffrement = blake2s_hash(mot_de_passe)
    
    # Calculer le tag d'intégrité du fichier chiffré
    tag_calcule = hmac_blake2s(cle_chiffrement, contenu_chiffre)
    
    # Vérifier l'intégrité en comparant les tags
    if tag_calcule != tag_attendu:
        print("❌ ERREUR: Le fichier est corrompu ou le mot de passe est incorrect!")
        return False
    
    print("✓ Tag d'intégrité vérifié avec succès")
    
    # Déchiffrer le contenu (inverse du chiffrement XOR)
    cle_bytes = bytes.fromhex(cle_chiffrement)
    contenu_dechiffre = bytes([contenu_chiffre[i] ^ cle_bytes[i % len(cle_bytes)] 
                               for i in range(len(contenu_chiffre))])
    
    # Sauvegarder le fichier déchiffré
    nom_fichier_dechiffre = nom_fichier_chiffre.replace('.enc', '.dec')
    with open(nom_fichier_dechiffre, 'wb') as f:
        f.write(contenu_dechiffre)
    
    print(f"✓ Fichier déchiffré: {nom_fichier_dechiffre}")
    
    return True


# ========== PROGRAMME PRINCIPAL - INTERACTIF ==========

def menu_principal():
    """
    Affiche le menu principal et gère l'interaction avec l'utilisateur
    """
    while True:
        print("\n" + "=" * 60)
        print("TP: Fonctions de Hachage et MACs")
        print("=" * 60)
        print("\nMenu Principal:")
        print("1. Tester la fonction BLAKE2s")
        print("2. Tester la fonction HMAC-BLAKE2s")
        print("3. Chiffrer un fichier")
        print("4. Déchiffrer un fichier")
        print("5. Quitter")
        print("=" * 60)
        
        # Lire le choix de l'utilisateur
        choix = input("\nEntrez votre choix (1-5): ").strip()
        
        # Traiter le choix de l'utilisateur
        if choix == '1':
            test_blake2s()
        elif choix == '2':
            test_hmac()
        elif choix == '3':
            interface_chiffrement()
        elif choix == '4':
            interface_dechiffrement()
        elif choix == '5':
            print("\n✓ Au revoir!")
            break
        else:
            print("\n❌ Choix invalide! Veuillez entrer un nombre entre 1 et 5.")


def test_blake2s():
    """
    Interface pour tester la fonction BLAKE2s
    """
    print("\n" + "-" * 60)
    print("Test de la fonction BLAKE2s")
    print("-" * 60)
    
    # Demander à l'utilisateur d'entrer un texte
    texte = input("\nEntrez le texte à hacher: ")
    
    # Calculer le haché
    hash_resultat = blake2s_hash(texte)
    
    # Afficher le résultat
    print(f"\nTexte original: {texte}")
    print(f"Haché BLAKE2s (256 bits): {hash_resultat}")
    
    # Attendre que l'utilisateur appuie sur Entrée
    input("\nAppuyez sur Entrée pour continuer...")


def test_hmac():
    """
    Interface pour tester la fonction HMAC-BLAKE2s
    """
    print("\n" + "-" * 60)
    print("Test de la fonction HMAC-BLAKE2s")
    print("-" * 60)
    
    # Demander la clé à l'utilisateur
    cle = input("\nEntrez la clé secrète: ")
    
    # Demander le message à l'utilisateur
    message = input("Entrez le message à authentifier: ")
    
    # Calculer le HMAC
    hmac_resultat = hmac_blake2s(cle, message)
    
    # Afficher le résultat
    print(f"\nClé: {cle}")
    print(f"Message: {message}")
    print(f"HMAC-BLAKE2s: {hmac_resultat}")
    
    # Attendre que l'utilisateur appuie sur Entrée
    input("\nAppuyez sur Entrée pour continuer...")


def interface_chiffrement():
    """
    Interface interactive pour chiffrer un fichier
    """
    print("\n" + "-" * 60)
    print("Chiffrement de fichier avec authentification")
    print("-" * 60)
    
    # Demander le chemin du fichier à l'utilisateur
    nom_fichier = input("\nEntrez le chemin du fichier à chiffrer: ").strip()
    
    # Vérifier si le fichier existe
    if not os.path.exists(nom_fichier):
        print(f"\n❌ ERREUR: Le fichier '{nom_fichier}' n'existe pas!")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Demander le mode opératoire
    print("\nChoisissez le mode opératoire:")
    print("1. CBC")
    print("2. CTR")
    mode_choix = input("Entrez votre choix (1 ou 2): ").strip()
    
    # Déterminer le mode
    if mode_choix == '1':
        mode = "CBC"
    elif mode_choix == '2':
        mode = "CTR"
    else:
        print("\n❌ Choix invalide! Mode CBC sera utilisé par défaut.")
        mode = "CBC"
    
    # Demander le mot de passe
    mot_de_passe = input("\nEntrez le mot de passe pour le chiffrement: ")
    
    # Confirmer le mot de passe
    confirmation = input("Confirmez le mot de passe: ")
    
    # Vérifier que les mots de passe correspondent
    if mot_de_passe != confirmation:
        print("\n❌ ERREUR: Les mots de passe ne correspondent pas!")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Chiffrer le fichier
    print(f"\n⏳ Chiffrement en cours...")
    try:
        fichier_chiffre, tag = chiffrer_fichier(nom_fichier, mot_de_passe, mode)
        print(f"\n✓ Chiffrement réussi!")
        print(f"✓ Tag d'intégrité: {tag}")
    except Exception as e:
        print(f"\n❌ ERREUR lors du chiffrement: {e}")
    
    # Attendre que l'utilisateur appuie sur Entrée
    input("\nAppuyez sur Entrée pour continuer...")


def interface_dechiffrement():
    """
    Interface interactive pour déchiffrer un fichier
    """
    print("\n" + "-" * 60)
    print("Déchiffrement de fichier avec vérification d'intégrité")
    print("-" * 60)
    
    # Demander le chemin du fichier chiffré
    nom_fichier_chiffre = input("\nEntrez le chemin du fichier chiffré (.enc): ").strip()
    
    # Vérifier si le fichier existe
    if not os.path.exists(nom_fichier_chiffre):
        print(f"\n❌ ERREUR: Le fichier '{nom_fichier_chiffre}' n'existe pas!")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Déterminer le nom du fichier tag
    nom_fichier_tag = nom_fichier_chiffre.replace('.enc', '.tag')
    
    # Vérifier si le fichier tag existe
    if not os.path.exists(nom_fichier_tag):
        print(f"\n❌ ERREUR: Le fichier tag '{nom_fichier_tag}' n'existe pas!")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    # Lire le tag d'intégrité
    with open(nom_fichier_tag, 'r') as f:
        tag_attendu = f.read().strip()
    
    print(f"\n✓ Tag d'intégrité lu: {tag_attendu}")
    
    # Demander le mot de passe
    mot_de_passe = input("\nEntrez le mot de passe pour le déchiffrement: ")
    
    # Déchiffrer le fichier
    print(f"\n⏳ Déchiffrement en cours...")
    try:
        succes = dechiffrer_fichier(nom_fichier_chiffre, mot_de_passe, tag_attendu)
        if succes:
            print(f"\n✓ Déchiffrement réussi!")
    except Exception as e:
        print(f"\n❌ ERREUR lors du déchiffrement: {e}")
    
    # Attendre que l'utilisateur appuie sur Entrée
    input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    # Lancer le menu principal
    menu_principal()