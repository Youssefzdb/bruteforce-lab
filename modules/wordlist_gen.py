#!/usr/bin/env python3
"""Custom Wordlist Generator Module"""
from itertools import product
import re

class WordlistGen:
    def __init__(self, name, birth, extra, output, logger):
        self.name = name
        self.birth = birth or ""
        self.extra = extra or []
        self.output = output
        self.logger = logger
        self.words = set()

    def _leet(self, word):
        table = str.maketrans("aeiost", "4310$7")
        return word.translate(table)

    def generate(self):
        base = [self.name, self.name.lower(), self.name.upper(), self.name.capitalize()]
        base += self.extra

        for word in list(base):
            base.append(self._leet(word))

        if self.birth:
            year = self.birth[-4:] if len(self.birth) >= 4 else ""
            day_month = self.birth[:4] if len(self.birth) >= 4 else ""
            for w in list(base):
                if year:
                    self.words.add(w + year)
                    self.words.add(year + w)
                if day_month:
                    self.words.add(w + day_month)

        # Common patterns
        common_suffixes = ["123", "1234", "12345", "!", "@", "#", "2024", "2025", "0000", "999"]
        for w in list(base):
            self.words.add(w)
            for s in common_suffixes:
                self.words.add(w + s)
                self.words.add(s + w)

        # Combos
        if len(base) >= 2:
            for a, b in product(base[:4], base[:4]):
                if a != b:
                    self.words.add(a + b)
                    self.words.add(a + "_" + b)

    def run(self):
        self.logger.info(f"[*] Generating wordlist for: {self.name}")
        self.generate()
        wordlist = sorted(self.words)
        with open(self.output, "w") as f:
            f.write("
".join(wordlist))
        self.logger.success(f"[+] Generated {len(wordlist)} words -> {self.output}")
        return wordlist
