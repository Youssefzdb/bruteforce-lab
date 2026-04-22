#!/usr/bin/env python3
"""
BruteForce Lab v1.0 — Credential Testing & Password Attack Research Tool
Author: Shadow Core
For authorized security testing only
"""
import argparse, sys
from modules.ssh_brute import SSHBrute
from modules.ftp_brute import FTPBrute
from modules.http_brute import HTTPBrute
from modules.wordlist_gen import WordlistGen
from modules.hash_crack import HashCracker
from utils.banner import banner
from utils.logger import Logger

def main():
    banner()
    p = argparse.ArgumentParser(description="BruteForce Lab — Credential Testing Toolkit")
    sub = p.add_subparsers(dest="module")

    ssh = sub.add_parser("ssh", help="SSH Brute Force")
    ssh.add_argument("--host", required=True)
    ssh.add_argument("--port", type=int, default=22)
    ssh.add_argument("--users", required=True, help="Username or userlist file")
    ssh.add_argument("--wordlist", required=True, help="Password wordlist file")
    ssh.add_argument("--threads", type=int, default=5)

    ftp = sub.add_parser("ftp", help="FTP Brute Force")
    ftp.add_argument("--host", required=True)
    ftp.add_argument("--port", type=int, default=21)
    ftp.add_argument("--users", required=True)
    ftp.add_argument("--wordlist", required=True)

    http = sub.add_parser("http", help="HTTP Form Brute Force")
    http.add_argument("--url", required=True)
    http.add_argument("--users", required=True)
    http.add_argument("--wordlist", required=True)
    http.add_argument("--user-field", default="username")
    http.add_argument("--pass-field", default="password")
    http.add_argument("--fail-string", required=True, help="String present on failed login")

    wl = sub.add_parser("wordlist", help="Generate custom wordlists")
    wl.add_argument("--name", required=True, help="Target name/keyword")
    wl.add_argument("--birth", help="Birthdate (DDMMYYYY)")
    wl.add_argument("--extra", nargs="+", help="Extra keywords")
    wl.add_argument("--output", default="wordlist.txt")

    hc = sub.add_parser("hash", help="Hash Cracker (MD5/SHA1/SHA256)")
    hc.add_argument("--hash", required=True, help="Hash to crack")
    hc.add_argument("--type", choices=["md5","sha1","sha256"], default="md5")
    hc.add_argument("--wordlist", required=True)

    p.add_argument("--verbose", "-v", action="store_true")
    args = p.parse_args()

    if not args.module:
        p.print_help(); sys.exit(0)

    log = Logger(args.verbose if hasattr(args, "verbose") else False)

    if args.module == "ssh":
        SSHBrute(args.host, args.port, args.users, args.wordlist, args.threads, log).run()
    elif args.module == "ftp":
        FTPBrute(args.host, args.port, args.users, args.wordlist, log).run()
    elif args.module == "http":
        HTTPBrute(args.url, args.users, args.wordlist, args.user_field, args.pass_field, args.fail_string, log).run()
    elif args.module == "wordlist":
        WordlistGen(args.name, args.birth, args.extra, args.output, log).run()
    elif args.module == "hash":
        HashCracker(args.hash, args.type, args.wordlist, log).run()

if __name__ == "__main__":
    main()
