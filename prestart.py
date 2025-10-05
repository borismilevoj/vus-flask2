# prestart.py
import os, shutil

def ensure_var_data():
    os.makedirs("/var/data", exist_ok=True)

def maybe_copy_db():
    target = "/var/data/VUS.db"
    if os.path.exists(target):
        print("prestart: /var/data/VUS.db že obstaja.")
        return
    # poskusi tipične lokacije v appu
    candidates = ["VUS.db", "static/VUS.db", "data/VUS.db"]
    for c in candidates:
        if os.path.exists(c):
            shutil.copy2(c, target)
            print(f"prestart: kopiral {c} -> {target}")
            return
    print("prestart: VUS.db ni najden; preskakujem kopiranje.")

if __name__ == "__main__":
    ensure_var_data()
    maybe_copy_db()
    print("prestart: OK")
