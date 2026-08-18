#!/usr/bin/env python3
"""
hashcracking.py — Hesh vositalari to'plami
Muallif: Ruslan Sodiqov | Haad IT Center — RED-0
"""

import hashlib
import bcrypt
import base64
import os
import sys

# ─────────────────────────────────────────────
#  Terminal ranglari
# ─────────────────────────────────────────────
class C:
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    CYAN    = "\033[96m"
    BOLD    = "\033[1m"
    RESET   = "\033[0m"

# ─────────────────────────────────────────────
#  Qo'llab-quvvatlanadigan algoritmlar
# ─────────────────────────────────────────────
HASH_ALGORITHMS = {
    "md5"      : hashlib.md5,
    "sha1"     : hashlib.sha1,
    "sha256"   : hashlib.sha256,
    "sha512"   : hashlib.sha512,
    "sha3_256" : hashlib.sha3_256,
}

# Hash uzunligi (hex belgilar soni) → mumkin bo'lgan tur
HASH_TYPES_BY_LENGTH = {
    32  : "MD5",
    40  : "SHA-1",
    56  : "SHA-224",
    64  : "SHA-256 yoki SHA-3-256",
    96  : "SHA-384",
    128 : "SHA-512",
}

# rockyou.txt standart joylashuvi
SCRIPT_DIR      = os.path.dirname(os.path.abspath(__file__))
DEFAULT_WORDLIST = os.path.join(SCRIPT_DIR, "rockyou.txt")


# ─────────────────────────────────────────────
#  Yordamchi funksiyalar
# ─────────────────────────────────────────────
def banner():
    print(f"""{C.CYAN}{C.BOLD}
╔══════════════════════════════════════════════╗
║          H A S H C R A C K I N G . P Y      ║
║      Hesh vositalari to'plami v2.0           ║
║      Muallif: Ruslan Sodiqov | RED-0         ║
╚══════════════════════════════════════════════╝{C.RESET}
""")


def detect_hash_type(hash_str: str) -> str:
    """Hash uzunligi bo'yicha turini aniqlaydi."""
    length = len(hash_str.strip())
    return HASH_TYPES_BY_LENGTH.get(length, f"Noma'lum ({length} belgi)")


def hash_text(text: str, algorithm: str) -> str:
    """Berilgan matnni ko'rsatilgan algoritm bilan heshlaydi."""
    algo = algorithm.lower()
    if algo not in HASH_ALGORITHMS:
        raise ValueError(f"Noto'g'ri algoritm: {algorithm}")
    h = HASH_ALGORITHMS[algo]()
    h.update(text.encode("utf-8"))
    return h.hexdigest()


def bcrypt_hash(text: str, cost: int = 12) -> str:
    """Matnni bcrypt bilan heshlaydi."""
    cost = max(4, min(cost, 31))          # [4 … 31] oraliqda qisqartirish
    salt  = bcrypt.gensalt(rounds=cost)
    hashed = bcrypt.hashpw(text.encode(), salt)
    return hashed.decode()


def bcrypt_verify(text: str, hashed: str) -> bool:
    """Parolni bcrypt heshi bilan solishtirib tekshiradi."""
    return bcrypt.checkpw(text.encode(), hashed.encode())


def bitlength(hex_digest: str) -> int:
    """Hex digest uzunligidan bit soni."""
    return len(hex_digest) * 4


# ─────────────────────────────────────────────
#  1-bo'lim: Hesh yaratish
# ─────────────────────────────────────────────
def hasher_menu():
    print(f"\n{C.BOLD}=== HESH YARATISH ==={C.RESET}")
    text = input("Matn kiriting: ").strip()
    if not text:
        print(f"{C.RED}[!] Bo'sh matn!{C.RESET}")
        return

    print(f"\n{C.YELLOW}Algoritmni tanlang:{C.RESET}")
    options = list(HASH_ALGORITHMS.keys()) + ["bcrypt"]
    for i, algo in enumerate(options, 1):
        print(f"  {i}. {algo.upper()}")

    try:
        choice = int(input("Raqam: ")) - 1
        if not (0 <= choice < len(options)):
            raise ValueError
    except ValueError:
        print(f"{C.RED}[!] Noto'g'ri tanlov.{C.RESET}")
        return

    selected = options[choice]

    if selected == "bcrypt":
        try:
            cost = int(input("Cost factor (4–31, default 12): ") or "12")
        except ValueError:
            cost = 12
        result = bcrypt_hash(text, cost)
        print(f"\n{C.GREEN}[+] bcrypt heshi:{C.RESET}\n{result}")
    else:
        result = hash_text(text, selected)
        bits   = bitlength(result)
        print(f"\n{C.GREEN}[+] {selected.upper()} heshi ({bits} bit):{C.RESET}")
        print(f"    {result}")


# ─────────────────────────────────────────────
#  2-bo'lim: Dictionary attack (lug'at hujumi)
# ─────────────────────────────────────────────
def dictionary_attack():
    print(f"\n{C.BOLD}=== LUG'AT HUJUMI (Dictionary Attack) ==={C.RESET}")
    target = input("Maqsad hash: ").strip()
    if not target:
        print(f"{C.RED}[!] Hash bo'sh!{C.RESET}")
        return

    detected = detect_hash_type(target)
    print(f"{C.CYAN}[i] Aniqlangan tur: {detected}{C.RESET}")

    print(f"\nAlgoritmni tanlang:")
    algos = list(HASH_ALGORITHMS.keys())
    for i, a in enumerate(algos, 1):
        print(f"  {i}. {a.upper()}")
    try:
        algo_idx = int(input("Raqam: ")) - 1
        algo = algos[algo_idx]
    except (ValueError, IndexError):
        print(f"{C.RED}[!] Noto'g'ri tanlov.{C.RESET}")
        return

    wordlist = input(f"Wordlist yo'li [{DEFAULT_WORDLIST}]: ").strip() or DEFAULT_WORDLIST

    if not os.path.isfile(wordlist):
        print(f"{C.RED}[!] Fayl topilmadi: {wordlist}{C.RESET}")
        return

    print(f"\n{C.YELLOW}[*] Hujum boshlandi…{C.RESET}")
    found    = False
    checked  = 0

    try:
        with open(wordlist, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                word = line.rstrip("\n")
                candidate = hash_text(word, algo)
                checked  += 1

                if checked % 100_000 == 0:
                    print(f"    {C.CYAN}{checked:,} so'z tekshirildi…{C.RESET}", end="\r")

                if candidate == target:
                    print(f"\n{C.GREEN}[+] TOPILDI! Parol: {C.BOLD}{word}{C.RESET}")
                    found = True
                    break
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}[!] Foydalanuvchi to'xtatdi.{C.RESET}")

    if not found:
        print(f"\n{C.RED}[-] Parol lug'atda topilmadi. ({checked:,} ta tekshirildi){C.RESET}")


# ─────────────────────────────────────────────
#  3-bo'lim: Hash turini aniqlash
# ─────────────────────────────────────────────
def identify_hash():
    print(f"\n{C.BOLD}=== HASH IDENTIFIKATOR ==={C.RESET}")
    h = input("Hash kiriting: ").strip()
    if not h:
        print(f"{C.RED}[!] Bo'sh hash!{C.RESET}")
        return
    tur    = detect_hash_type(h)
    bits   = len(h) * 4
    print(f"{C.GREEN}[+] Taxminiy tur : {tur}{C.RESET}")
    print(f"    Uzunlik      : {len(h)} belgi → {bits} bit")


# ─────────────────────────────────────────────
#  4-bo'lim: Base64 encoding / decoding
# ─────────────────────────────────────────────
def base64_menu():
    print(f"\n{C.BOLD}=== BASE64 ==={C.RESET}")
    print("  1. Encode (matni → Base64)")
    print("  2. Decode (Base64 → matn)")
    choice = input("Tanlov: ").strip()

    if choice == "1":
        text  = input("Matn: ").strip()
        result = base64.b64encode(text.encode()).decode()
        print(f"{C.GREEN}[+] Base64: {result}{C.RESET}")
    elif choice == "2":
        data = input("Base64: ").strip()
        try:
            result = base64.b64decode(data).decode()
            print(f"{C.GREEN}[+] Matn: {result}{C.RESET}")
        except Exception as e:
            print(f"{C.RED}[!] Xato: {e}{C.RESET}")
    else:
        print(f"{C.RED}[!] Noto'g'ri tanlov.{C.RESET}")


# ─────────────────────────────────────────────
#  5-bo'lim: bcrypt tekshirish
# ─────────────────────────────────────────────
def bcrypt_check_menu():
    print(f"\n{C.BOLD}=== BCRYPT TEKSHIRISH ==={C.RESET}")
    plain  = input("Parol: ").strip()
    hashed = input("bcrypt heshi: ").strip()
    if bcrypt_verify(plain, hashed):
        print(f"{C.GREEN}[+] Mos keldi! Parol to'g'ri.{C.RESET}")
    else:
        print(f"{C.RED}[-] Mos kelmadi.{C.RESET}")


# ─────────────────────────────────────────────
#  Asosiy menyu
# ─────────────────────────────────────────────
def main():
    banner()
    menu = {
        "1": ("Hesh yaratish",          hasher_menu),
        "2": ("Lug'at hujumi",          dictionary_attack),
        "3": ("Hash turini aniqlash",   identify_hash),
        "4": ("Base64 encode / decode", base64_menu),
        "5": ("bcrypt tekshirish",      bcrypt_check_menu),
        "0": ("Chiqish",                None),
    }

    while True:
        print(f"\n{C.BOLD}─── ASOSIY MENYU ───{C.RESET}")
        for key, (label, _) in menu.items():
            print(f"  {C.CYAN}{key}{C.RESET}. {label}")

        choice = input("\nTanlov: ").strip()

        if choice == "0":
            print(f"{C.YELLOW}Xayr!{C.RESET}")
            sys.exit(0)
        elif choice in menu:
            menu[choice][1]()
        else:
            print(f"{C.RED}[!] Noto'g'ri tanlov, qayta urining.{C.RESET}")


if __name__ == "__main__":
    main()
