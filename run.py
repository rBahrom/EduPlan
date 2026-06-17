#!/usr/bin/env python3
"""EduPlan'ni bitta komanda bilan ishga tushirish.

Backend (FastAPI, :8070) va frontend (Vite, :5173) ni bir vaqtda ishga tushiradi.
Ctrl+C bosilganda ikkalasini ham to'g'ri to'xtatadi.

Foydalanish:
    .venv/bin/python run.py
yoki:
    python run.py
"""

import os
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FROND = ROOT / "frond"

# Backend uchun .venv ichidagi python'ni ishlatamiz (mavjud bo'lsa)
VENV_PY = ROOT / ".venv" / "bin" / "python"
PYTHON = str(VENV_PY) if VENV_PY.exists() else sys.executable

# npm'ni topamiz (Windows'da npm.cmd bo'ladi)
NPM = "npm.cmd" if os.name == "nt" else "npm"

processes = []


def start(name, cmd, cwd):
    print(f"[run] {name} ishga tushmoqda: {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, cwd=cwd)
    processes.append((name, proc))
    return proc


def shutdown(*_):
    print("\n[run] To'xtatilmoqda...")
    for name, proc in processes:
        if proc.poll() is None:
            print(f"[run] {name} to'xtatilmoqda")
            proc.terminate()
    for _, proc in processes:
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    start(
        "backend",
        [PYTHON, "-m", "uvicorn", "main:app", "--reload", "--port", "8070"],
        cwd=ROOT,
    )
    start(
        "frontend",
        [NPM, "run", "dev"],
        cwd=FROND,
    )

    print("[run] Backend: http://localhost:8070  |  Frontend: http://localhost:5173")
    print("[run] To'xtatish uchun Ctrl+C bosing.")

    # Birorta jarayon o'lib qolsa, hammasini to'xtatamiz
    while True:
        for name, proc in processes:
            code = proc.poll()
            if code is not None:
                print(f"[run] {name} kutilmaganda to'xtadi (code={code}).")
                shutdown()
        try:
            for _, proc in processes:
                proc.wait(timeout=1)
        except subprocess.TimeoutExpired:
            continue


if __name__ == "__main__":
    main()