import struct

DELTA = 0x9E3779B9
ROUNDS = 32

def to_u32(x):
    return x & 0xffffffff

def xtea_encrypt_block(block, key):
    v0, v1 = struct.unpack(">2I", block)
    k = struct.unpack(">4I", key)
    s = 0
    for _ in range(ROUNDS):
        s = to_u32(s + DELTA)
        v0 = to_u32(v0 + (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (s + k[s & 3]))
        v1 = to_u32(v1 + (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (s + k[(s >> 11) & 3]))
    return struct.pack(">2I", v0, v1)

def xtea_decrypt_block(block, key):
    v0, v1 = struct.unpack(">2I", block)
    k = struct.unpack(">4I", key)
    s = (DELTA * ROUNDS) & 0xffffffff
    for _ in range(ROUNDS):
        v1 = to_u32(v1 - (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (s + k[(s >> 11) & 3]))
        v0 = to_u32(v0 - (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (s + k[s & 3]))
        s = to_u32(s - DELTA)
    return struct.pack(">2I", v0, v1)

def pad(b):
    p = 8 - (len(b) % 8)
    return b + bytes([p]) * p

def unpad(b):
    return b[:-b[-1]]

# ---------------- MODES ----------------

def ecb_encrypt(msg, key):
    msg = pad(msg)
    out = b""
    for i in range(0, len(msg), 8):
        out += xtea_encrypt_block(msg[i:i+8], key)
    return out

def ecb_decrypt(ct, key):
    out = b""
    for i in range(0, len(ct), 8):
        out += xtea_decrypt_block(ct[i:i+8], key)
    return unpad(out)

def cbc_encrypt(msg, key, iv):
    msg = pad(msg)
    out = b""
    prev = iv
    for i in range(0, len(msg), 8):
        block = bytes(a ^ b for a, b in zip(msg[i:i+8], prev))
        enc = xtea_encrypt_block(block, key)
        out += enc
        prev = enc
    return out

def cbc_decrypt(ct, key, iv):
    out = b""
    prev = iv
    for i in range(0, len(ct), 8):
        dec = xtea_decrypt_block(ct[i:i+8], key)
        block = bytes(a ^ b for a, b in zip(dec, prev))
        out += block
        prev = ct[i:i+8]
    return unpad(out)

def ofb_process(data, key, iv):
    out = b""
    feedback = iv
    for i in range(0, len(data), 8):
        stream = xtea_encrypt_block(feedback, key)
        chunk = data[i:i+8]
        out += bytes(a ^ b for a, b in zip(chunk, stream[:len(chunk)]))
        feedback = stream
    return out

def ctr_process(data, key, iv):
    counter = int.from_bytes(iv, "big")
    out = b""
    for i in range(0, len(data), 8):
        block = counter.to_bytes(8, "big")
        stream = xtea_encrypt_block(block, key)
        chunk = data[i:i+8]
        out += bytes(a ^ b for a, b in zip(chunk, stream[:len(chunk)]))
        counter += 1
    return out

# ---------------- USER INTERFACE ----------------

if __name__ == "__main__":
    print("=== XTEA Encrypt/Decrypt ===")

    text = input("Entrez le texte à chiffrer : ").encode()
    key_hex = input("Entrez la clé (32 hex chars = 128 bits) : ")
    key = bytes.fromhex(key_hex)

    mode = input("Mode (ECB / CBC / OFB / CTR) : ").upper()

    if mode in ["CBC", "OFB", "CTR"]:
        iv_hex = input("IV (16 hex chars = 8 bytes) : ")
        iv = bytes.fromhex(iv_hex)
    else:
        iv = None

    # Encryption
    if mode == "ECB":
        ct = ecb_encrypt(text, key)
        pt = ecb_decrypt(ct, key)

    elif mode == "CBC":
        ct = cbc_encrypt(text, key, iv)
        pt = cbc_decrypt(ct, key, iv)

    elif mode == "OFB":
        ct = ofb_process(text, key, iv)
        pt = ofb_process(ct, key, iv)

    elif mode == "CTR":
        ct = ctr_process(text, key, iv)
        pt = ctr_process(ct, key, iv)

    else:
        print("Mode inconnu.")
        exit()

    print("\n--- Résultats ---")
    print("Ciphertext (hex) :", ct.hex())