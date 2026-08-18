# 🔐 HashCracking.py

> Hesh vositalari to'plami

---

## 📌 Loyiha haqida

`HashCracking.py` — kriptografiya va parol xavfsizligini o'rganish uchun yozilgan Python vositasi.  
MD5, SHA, bcrypt algoritmlarini qo'llab-quvvatlaydi va dictionary attack imkonini beradi.

---

## ⚙️ Imkoniyatlar

| Bo'lim | Tavsif |
|--------|--------|
| 🔑 Hesh yaratish | MD5, SHA-1, SHA-256, SHA-512, SHA3-256, bcrypt |
| 🔍 Dictionary Attack | Wordlist (rockyou.txt) orqali hash crack qilish |
| 🧩 Hash Identifier | Hash uzunligi bo'yicha turini aniqlash |
| 📦 Base64 | Encode va decode |
| ✅ bcrypt tekshirish | Parolni bcrypt heshi bilan solishtirish |

---

## 🚀 Ishga tushirish

```bash
# Kutubxonani o'rnatish
pip install bcrypt

# Dasturni ishga tushirish
python3 HashCracking.py
```

---

## 🖥️ Namuna

```
╔══════════════════════════════════════════════╗
║          H A S H C R A C K I N G . P Y      ║
║      Hesh vositalari to'plami v2.0           ║
║      Muallif: Ruslan Sodiqov | RED-0         ║
╚══════════════════════════════════════════════╝

─── ASOSIY MENYU ───
  1. Hesh yaratish
  2. Lug'at hujumi
  3. Hash turini aniqlash
  4. Base64 encode / decode
  5. bcrypt tekshirish
  0. Chiqish
```

---

## 🛠️ Texnologiyalar

- **Python 3**
- `hashlib` — MD5, SHA algoritmlari
- `bcrypt` — kuchli parol heshi
- `base64` — encoding/decoding
- `os`, `sys` — fayl va tizim boshqaruvi

---

## 📚 Maqsad

Bu loyiha **Haad IT Center RED-0** (Offensive Security) dasturi doirasida  
kriptografiya modulini o'rganish jarayonida yaratilgan.

---

## 📄 Litsenziya

Faqat ta'lim maqsadida. Noqonuniy maqsadlarda ishlatish taqiqlanadi.
