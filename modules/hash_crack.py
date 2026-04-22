#!/usr/bin/env python3
"""Hash Cracker Module (MD5 / SHA1 / SHA256)"""
import hashlib

class HashCracker:
    def __init__(self, target_hash, hash_type, wordlist, logger):
        self.target = target_hash.lower().strip()
        self.hash_type = hash_type
        self.wordlist = wordlist
        self.logger = logger

    def _hash(self, word):
        h = hashlib.new(self.hash_type)
        h.update(word.encode("utf-8", errors="ignore"))
        return h.hexdigest()

    def run(self):
        self.logger.info(f"[*] Cracking {self.hash_type.upper()} hash: {self.target}")
        try:
            with open(self.wordlist) as f:
                words = [l.strip() for l in f if l.strip()]
        except FileNotFoundError:
            self.logger.error(f"Wordlist not found: {self.wordlist}")
            return None

        self.logger.info(f"[*] Trying {len(words)} passwords...")
        for word in words:
            if self._hash(word) == self.target:
                self.logger.success(f"[CRACKED] {self.target} = '{word}'")
                return word
            variations = [word, word.lower(), word.upper(), word.capitalize()]
            for v in variations:
                if self._hash(v) == self.target:
                    self.logger.success(f"[CRACKED] {self.target} = '{v}'")
                    return v

        self.logger.warning("[-] Hash not cracked with given wordlist")
        return None
