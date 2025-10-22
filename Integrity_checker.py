import os
import hashlib
import json
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import time

# -----------------------
# Hash fonksiyonları
# -----------------------
def compute_file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def scan_directory(root_path):
    results = {}
    root_path = os.path.abspath(root_path)
    for dirpath, _, filenames in os.walk(root_path):
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            try:
                rel = os.path.relpath(full, root_path)
                sha = compute_file_sha256(full)
                results[rel] = sha
            except (PermissionError, FileNotFoundError):
                continue
    return results

def load_hash_db(db_path):
    if not os.path.exists(db_path):
        return {}
    with open(db_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_hash_db(db_path, data):
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def compare_hashes(old_hashes, new_hashes):
    changed = []
    new = []
    deleted = []
    for path, sha in new_hashes.items():
        if path not in old_hashes:
            new.append(path)
        elif old_hashes[path] != sha:
            changed.append(path)
    for path in old_hashes:
        if path not in new_hashes:
            deleted.append(path)
    return {"changed": changed, "new": new, "deleted": deleted}

# -----------------------
# GUI Fonksiyonları
# -----------------------
class IntegrityCheckerGUI:
    def __init__(self, master):
        self.master = master
        master.title("File Hash Integrity Checker")
        master.geometry("700x500")
        
        # Seçilen klasör
        self.folder_path = tk.StringVar()
        
        tk.Label(master, text="İzlenecek Klasör:").pack(pady=5)
        tk.Entry(master, textvariable=self.folder_path, width=80).pack(padx=10)
        tk.Button(master, text="Klasör Seç", command=self.select_folder).pack(pady=5)
        tk.Button(master, text="Taramayı Başlat", command=self.start_scan).pack(pady=5)
        
        self.output = scrolledtext.ScrolledText(master, width=80, height=20)
        self.output.pack(padx=10, pady=10)
    
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
    
    def start_scan(self):
        folder = self.folder_path.get()
        if not folder or not os.path.exists(folder):
            messagebox.showerror("Hata", "Lütfen geçerli bir klasör seçin!")
            return
        
        db_path = os.path.join(folder, ".hashes.json")
        old_hashes = load_hash_db(db_path)
        
        start_time = time.time()
        new_hashes = scan_directory(folder)
        duration = time.time() - start_time
        
        report = compare_hashes(old_hashes, new_hashes)
        save_hash_db(db_path, new_hashes)
        
        self.output.delete(1.0, tk.END)
        total_changes = len(report["changed"]) + len(report["new"]) + len(report["deleted"])
        if total_changes == 0:
            self.output.insert(tk.END, "[OK] Hiç değişiklik yok.\n")
        else:
            self.output.insert(tk.END, f"[!] Değişiklik tespit edildi: {total_changes} olay\n")
            if report["changed"]:
                self.output.insert(tk.END, " - Değişen dosyalar:\n")
                for p in report["changed"]:
                    self.output.insert(tk.END, f"    * {p}\n")
            if report["new"]:
                self.output.insert(tk.END, " - Yeni dosyalar:\n")
                for p in report["new"]:
                    self.output.insert(tk.END, f"    * {p}\n")
            if report["deleted"]:
                self.output.insert(tk.END, " - Silinmiş dosyalar:\n")
                for p in report["deleted"]:
                    self.output.insert(tk.END, f"    * {p}\n")
        self.output.insert(tk.END, f"\nTarama tamamlandı ({len(new_hashes)} dosya, {duration:.2f}s). Hash veritabanı: {db_path}\n")

# -----------------------
# Ana Program
# -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = IntegrityCheckerGUI(root)
    root.mainloop()
