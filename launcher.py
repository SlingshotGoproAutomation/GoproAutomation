import os
import sys
import time
import shutil
import subprocess
from pathlib import Path
import psutil

def is_process_running(exe_name):
    for proc in psutil.process_iter(['name']):
        try:
            if proc.info['name'] and proc.info['name'].lower() == exe_name.lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False

def wait_for_exit(exe_name, timeout=60):
    start = time.time()
    while is_process_running(exe_name):
        if time.time() - start > timeout:
            print(f"Timeout waiting for {exe_name} to exit.")
            return False
        time.sleep(1)
    return True

def replace_and_launch():
    # Base dir is wherever the launcher is
    base_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
    dist_dir = base_dir
    old_exe = dist_dir / "Slingshot.exe"
    new_exe = dist_dir / "Slingshot_new.exe"

    if not new_exe.exists():
        print("New executable not found.")
        return

    print("Waiting for Slingshot.exe to exit...")
    if not wait_for_exit("Slingshot.exe"):
        return

    try:
        print("Replacing Slingshot.exe...")
        shutil.move(str(new_exe), str(old_exe))
    except Exception as e:
        print(f"Failed to replace executable: {e}")
        return

    print("Launching updated Slingshot.exe...")
    subprocess.Popen([str(old_exe)], cwd=dist_dir, shell=False)

if __name__ == "__main__":
    replace_and_launch()

