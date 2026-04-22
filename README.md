# 🔨 BruteForce Lab

> Credential Testing & Password Attack Research Toolkit | by **Shadow Core**

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python) ![Status](https://img.shields.io/badge/Status-Active-brightgreen)

## Features
- 🔐 **SSH Brute Force** — Multi-threaded SSH credential testing
- 📂 **FTP Brute Force** — FTP login brute force
- 🌐 **HTTP Form Brute** — POST-based web login brute force
- 📝 **Wordlist Generator** — Custom targeted wordlists (name + birth + leet)
- #️⃣ **Hash Cracker** — Crack MD5 / SHA1 / SHA256 hashes

## Installation

```bash
git clone https://github.com/Youssefzdb/bruteforce-lab
cd bruteforce-lab
pip install -r requirements.txt
```

## Usage

```bash
# SSH brute force
python3 main.py ssh --host 192.168.1.1 --users admin --wordlist rockyou.txt

# FTP brute force
python3 main.py ftp --host 192.168.1.1 --users users.txt --wordlist wordlist.txt

# HTTP form brute force
python3 main.py http --url http://target/login --users admin --wordlist wordlist.txt --fail-string "Invalid password"

# Generate targeted wordlist
python3 main.py wordlist --name shadow --birth 01011995 --extra hack cyber --output mylist.txt

# Crack MD5 hash
python3 main.py hash --hash 5f4dcc3b5aa765d61d8327deb882cf99 --type md5 --wordlist rockyou.txt
```

## ⚠️ Disclaimer
For authorized penetration testing and security research only.

## 👤 Author
**Shadow Core** | Penetration Tester
