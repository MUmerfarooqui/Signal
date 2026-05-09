"""
Single-command backend launcher.
Starts Redis, FastAPI, Celery worker, and Celery beat.
Prints "Backend up and running" once all services are healthy.
"""
import signal
import subprocess
import sys
import threading
import time
import urllib.request

import colorama
import redis as redis_lib
from colorama import Fore, Style

colorama.init()

LABELS = {
    "redis":  (Fore.CYAN,    "redis "),
    "web":    (Fore.GREEN,   "web   "),
    "worker": (Fore.YELLOW,  "worker"),
    "beat":   (Fore.MAGENTA, "beat  "),
}

COMMANDS = {
    "redis":  ["docker", "run", "--rm", "-p", "6379:6379", "redis:alpine"],
    "web":    [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
    "worker": [sys.executable, "-m", "celery", "-A", "workers.celery_app", "worker", "--loglevel=warning", "--pool=solo"],
    "beat":   [sys.executable, "-m", "celery", "-A", "workers.celery_app", "beat",   "--loglevel=warning"],
}

processes: dict[str, subprocess.Popen] = {}


def stream(name: str, proc: subprocess.Popen) -> None:
    color, label = LABELS[name]
    for line in proc.stdout:
        text = line.decode(errors="replace").rstrip()
        if text:
            print(f"{color}[{label}]{Style.RESET_ALL} {text}", flush=True)


def wait_until_ready() -> None:
    deadline = time.time() + 60
    redis_ok = web_ok = False

    while time.time() < deadline:
        time.sleep(1)

        if not redis_ok:
            try:
                r = redis_lib.Redis.from_url("redis://localhost:6379", socket_connect_timeout=1)
                r.ping()
                redis_ok = True
            except Exception:
                pass

        if not web_ok:
            try:
                urllib.request.urlopen("http://localhost:8000/health", timeout=1)
                web_ok = True
            except Exception:
                pass

        if redis_ok and web_ok:
            print(
                f"\n{Style.BRIGHT}{Fore.GREEN}✓ Backend up and running{Style.RESET_ALL}\n",
                flush=True,
            )
            return

    print(f"{Fore.RED}⚠ Timed out waiting for services to start{Style.RESET_ALL}", flush=True)


def shutdown(sig=None, frame=None) -> None:
    print(f"\n{Fore.RED}Shutting down...{Style.RESET_ALL}", flush=True)
    for proc in processes.values():
        try:
            proc.terminate()
        except Exception:
            pass
    sys.exit(0)


def main() -> None:
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    for name, cmd in COMMANDS.items():
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        processes[name] = proc
        threading.Thread(target=stream, args=(name, proc), daemon=True).start()

    threading.Thread(target=wait_until_ready, daemon=True).start()

    # Block until all processes exit (they won't unless something crashes)
    for proc in processes.values():
        proc.wait()


if __name__ == "__main__":
    main()
