"""
=============================================================
  SISTEM MANAJEMEN PERPUSTAKAAN
  Final Project - Aplikasi Manajemen dengan Database Flat File (.CSV)
  Bahasa Pemrograman : Python
  Struktur Data      : Linked List + Stack (Riwayat Pencarian)
  Database           : File CSV
  Operasi            : CRUD (Create, Read, Update, Delete)
  Antarmuka          : Command-Line Interface (CLI)
=============================================================
"""

import csv
import os
from datetime import datetime

# ─────────────────────────────────────────────
#  STRUKTUR DATA 1: LINKED LIST
#  Digunakan untuk menyimpan daftar buku di memori
# ─────────────────────────────────────────────

class Node:
    """Node untuk Linked List"""
    def __init__(self, data):
        self.data = data   # data buku (dict)
        self.next = None   # pointer ke node berikutnya


class LinkedList:
    """Singly Linked List untuk menyimpan koleksi buku"""

    def __init__(self):
        self.head = None
        self._size = 0

    def tambah_di_akhir(self, data: dict):
        """Tambah node baru di akhir list"""
        node_baru = Node(data)
        if self.head is None:
            self.head = node_baru
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node_baru
        self._size += 1

    def hapus_by_id(self, id_buku: str) -> bool:
        """Hapus node berdasarkan ID buku"""
        if self.head is None:
            return False

        # Kasus: node pertama yang dihapus
        if self.head.data['id'] == id_buku:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next:
            if current.next.data['id'] == id_buku:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        return False

    def cari_by_id(self, id_buku: str):
        """Cari node berdasarkan ID, return data dict atau None"""
        current = self.head
        while current:
            if current.data['id'] == id_buku:
                return current.data
            current = current.next
        return None

    def cari_by_judul(self, keyword: str) -> list:
        """Linear search berdasarkan kata kunci judul (case-insensitive)"""
        hasil = []
        current = self.head
        while current:
            if keyword.lower() in current.data['judul'].lower():
                hasil.append(current.data)
            current = current.next
        return hasil

    def ke_list(self) -> list:
        """Konversi linked list ke Python list"""
        hasil = []
        current = self.head
        while current:
            hasil.append(current.data)
            current = current.next
        return hasil

    def __len__(self):
        return self._size

    def sorting_bubble(self, key='judul', ascending=True) -> list:
        """
        Bubble Sort pada linked list berdasarkan key tertentu.
        Return list yang sudah terurut (tidak mengubah linked list asli).
        """
        data = self.ke_list()
        n = len(data)
        for i in range(n - 1):
            for j in range(n - i - 1):
                val_a = data[j][key].lower() if isinstance(data[j][key], str) else data[j][key]
                val_b = data[j+1][key].lower() if isinstance(data[j+1][key], str) else data[j+1][key]
                if (val_a > val_b) if ascending else (val_a < val_b):
                    data[j], data[j+1] = data[j+1], data[j]
        return data


# ─────────────────────────────────────────────
#  STRUKTUR DATA 2: STACK
#  Digunakan untuk menyimpan riwayat pencarian
#  (LIFO - Last In First Out)
# ─────────────────────────────────────────────

class Stack:
    """Stack berbasis list Python untuk riwayat pencarian"""

    def __init__(self, kapasitas=10):
        self._data = []
        self._kapasitas = kapasitas

    def push(self, item):
        """Masukkan item ke atas stack"""
        if len(self._data) >= self._kapasitas:
            self._data.pop(0)   # buang item paling lama jika penuh
        self._data.append(item)

    def pop(self):
        """Keluarkan item teratas dari stack"""
        if self.is_empty():
            return None
        return self._data.pop()

    def peek(self):
        """Lihat item teratas tanpa menghapus"""
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def semua(self) -> list:
        """Return semua item dari paling baru ke paling lama"""
        return list(reversed(self._data))

    def __len__(self):
        return len(self._data)


# ─────────────────────────────────────────────
#  MANAJEMEN FILE CSV
# ─────────────────────────────────────────────

FILE_CSV = "buku.csv"
HEADER_CSV = ['id', 'judul', 'penulis', 'tahun', 'genre', 'stok']


def inisialisasi_csv():
    """Buat file CSV dengan header jika belum ada"""
    if not os.path.exists(FILE_CSV):
        with open(FILE_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=HEADER_CSV)
            writer.writeheader()
        print(f"[INFO] File '{FILE_CSV}' berhasil dibuat.")


def baca_csv() -> LinkedList:
    """Baca semua data dari CSV ke dalam Linked List"""
    ll = LinkedList()
    if not os.path.exists(FILE_CSV):
        return ll
    with open(FILE_CSV, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for baris in reader:
            ll.tambah_di_akhir(baris)
    return ll


def tulis_csv(linked_list: LinkedList):
    """Tulis seluruh Linked List ke file CSV"""
    data = linked_list.ke_list()
    with open(FILE_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADER_CSV)
        writer.writeheader()
        writer.writerows(data)


def generate_id(linked_list: LinkedList) -> str:
    """Generate ID buku otomatis format 001, 002, 003, dst."""
    data = linked_list.ke_list()
    if not data:
        return "001"
    try:
        id_angka = [int(d['id']) for d in data]
        return f"{(max(id_angka) + 1):03d}"
    except ValueError:
        return f"{(len(data) + 1):03d}"


# ─────────────────────────────────────────────
#  OPERASI CRUD
# ─────────────────────────────────────────────

def tambah_buku(linked_list: LinkedList):
    """CREATE - Tambah buku baru"""
    print("\n" + "─"*40)
    print("  TAMBAH BUKU BARU")
    print("─"*40)
    judul   = input("  Judul buku   : ").strip()
    penulis = input("  Penulis      : ").strip()
    tahun   = input("  Tahun terbit : ").strip()
    genre   = input("  Genre        : ").strip()
    stok    = input("  Stok         : ").strip()

    if not all([judul, penulis, tahun, genre, stok]):
        print("[ERROR] Semua field harus diisi!")
        return

    if not stok.isdigit():
        print("[ERROR] Stok harus berupa angka!")
        return

    id_baru = generate_id(linked_list)
    buku_baru = {
        'id'     : id_baru,
        'judul'  : judul,
        'penulis': penulis,
        'tahun'  : tahun,
        'genre'  : genre,
        'stok'   : stok
    }
    linked_list.tambah_di_akhir(buku_baru)
    tulis_csv(linked_list)
    print(f"\n[SUKSES] Buku '{judul}' berhasil ditambahkan dengan ID: {id_baru}")


def tampilkan_semua(linked_list: LinkedList, data_list: list = None):
    """READ - Tampilkan semua buku"""
    data = data_list if data_list is not None else linked_list.ke_list()
    print("\n" + "─"*75)
    print(f"  {'ID':<8} {'JUDUL':<28} {'PENULIS':<20} {'THN':<6} {'GENRE':<10} {'STOK'}")
    print("─"*75)
    if not data:
        print("  (Belum ada data buku)")
    else:
        for buku in data:
            print(f"  {buku['id']:<8} {buku['judul'][:27]:<28} {buku['penulis'][:19]:<20} "
                  f"{buku['tahun']:<6} {buku['genre'][:9]:<10} {buku['stok']}")
    print("─"*75)
    print(f"  Total: {len(data)} buku")


def update_buku(linked_list: LinkedList):
    """UPDATE - Perbarui data buku berdasarkan ID"""
    print("\n" + "─"*40)
    print("  UPDATE DATA BUKU")
    print("─"*40)
    id_cari = input("  Masukkan ID buku yang akan diubah: ").strip()
    buku = linked_list.cari_by_id(id_cari)

    if not buku:
        print(f"[ERROR] Buku dengan ID '{id_cari}' tidak ditemukan.")
        return

    print(f"\n  Data saat ini:")
    print(f"  Judul   : {buku['judul']}")
    print(f"  Penulis : {buku['penulis']}")
    print(f"  Tahun   : {buku['tahun']}")
    print(f"  Genre   : {buku['genre']}")
    print(f"  Stok    : {buku['stok']}")
    print("\n  (Tekan ENTER untuk melewati field yang tidak ingin diubah)")

    judul   = input(f"  Judul baru   [{buku['judul']}] : ").strip()
    penulis = input(f"  Penulis baru [{buku['penulis']}] : ").strip()
    tahun   = input(f"  Tahun baru   [{buku['tahun']}] : ").strip()
    genre   = input(f"  Genre baru   [{buku['genre']}] : ").strip()
    stok    = input(f"  Stok baru    [{buku['stok']}] : ").strip()

    if stok and not stok.isdigit():
        print("[ERROR] Stok harus berupa angka!")
        return

    # Update data di node linked list
    if judul  : buku['judul']   = judul
    if penulis: buku['penulis'] = penulis
    if tahun  : buku['tahun']   = tahun
    if genre  : buku['genre']   = genre
    if stok   : buku['stok']    = stok

    tulis_csv(linked_list)
    print(f"\n[SUKSES] Data buku ID '{id_cari}' berhasil diperbarui.")


def hapus_buku(linked_list: LinkedList):
    """DELETE - Hapus buku berdasarkan ID"""
    print("\n" + "─"*40)
    print("  HAPUS BUKU")
    print("─"*40)
    id_hapus = input("  Masukkan ID buku yang akan dihapus: ").strip()
    buku = linked_list.cari_by_id(id_hapus)

    if not buku:
        print(f"[ERROR] Buku dengan ID '{id_hapus}' tidak ditemukan.")
        return

    konfirmasi = input(f"  Yakin ingin menghapus '{buku['judul']}'? (y/n): ").strip().lower()
    if konfirmasi == 'y':
        linked_list.hapus_by_id(id_hapus)
        tulis_csv(linked_list)
        print(f"\n[SUKSES] Buku '{buku['judul']}' berhasil dihapus.")
    else:
        print("  Penghapusan dibatalkan.")


# ─────────────────────────────────────────────
#  FITUR TAMBAHAN: PENCARIAN & SORTING
# ─────────────────────────────────────────────

def cari_buku(linked_list: LinkedList, riwayat: Stack):
    """Pencarian buku berdasarkan judul (Linear Search)"""
    print("\n" + "─"*40)
    print("  CARI BUKU")
    print("─"*40)
    keyword = input("  Masukkan kata kunci judul: ").strip()
    if not keyword:
        print("[ERROR] Kata kunci tidak boleh kosong!")
        return

    riwayat.push(f"{keyword} ({datetime.now().strftime('%H:%M:%S')})")
    hasil = linked_list.cari_by_judul(keyword)

    if hasil:
        print(f"\n  Ditemukan {len(hasil)} buku dengan kata kunci '{keyword}':")
        tampilkan_semua(linked_list, hasil)
    else:
        print(f"\n  Tidak ditemukan buku dengan kata kunci '{keyword}'.")


def tampilkan_riwayat(riwayat: Stack):
    """Tampilkan riwayat pencarian dari Stack"""
    print("\n" + "─"*40)
    print("  RIWAYAT PENCARIAN (Stack - LIFO)")
    print("─"*40)
    if riwayat.is_empty():
        print("  (Belum ada riwayat pencarian)")
    else:
        for i, item in enumerate(riwayat.semua(), 1):
            print(f"  {i}. {item}")


def sorting_buku(linked_list: LinkedList):
    """Sorting buku menggunakan Bubble Sort"""
    print("\n" + "─"*40)
    print("  URUTKAN BUKU (Bubble Sort)")
    print("─"*40)
    print("  Urutkan berdasarkan:")
    print("  1. Judul (A-Z)")
    print("  2. Judul (Z-A)")
    print("  3. Tahun Terbit (Terlama-Terbaru)")
    print("  4. Tahun Terbit (Terbaru-Terlama)")
    pilihan = input("  Pilih [1-4]: ").strip()

    mapping = {
        '1': ('judul', True),
        '2': ('judul', False),
        '3': ('tahun', True),
        '4': ('tahun', False),
    }
    if pilihan not in mapping:
        print("[ERROR] Pilihan tidak valid.")
        return

    key, ascending = mapping[pilihan]
    hasil = linked_list.sorting_bubble(key, ascending)
    arah = "A→Z / Terlama→Terbaru" if ascending else "Z→A / Terbaru→Terlama"
    print(f"\n  Hasil sorting berdasarkan '{key}' ({arah}):")
    tampilkan_semua(linked_list, hasil)


# ─────────────────────────────────────────────
#  MAIN PROGRAM & MENU
# ─────────────────────────────────────────────

def tampilkan_menu():
    print("\n" + "="*45)
    print("   📚  SISTEM MANAJEMEN PERPUSTAKAAN  📚")
    print("="*45)
    print("  [1] Lihat Semua Buku")
    print("  [2] Tambah Buku Baru")
    print("  [3] Update Data Buku")
    print("  [4] Hapus Buku")
    print("  [5] Cari Buku (Linear Search)")
    print("  [6] Urutkan Buku (Bubble Sort)")
    print("  [7] Riwayat Pencarian (Stack)")
    print("  [0] Keluar")
    print("="*45)


def main():
    inisialisasi_csv()
    linked_list = baca_csv()  # Load data CSV ke Linked List
    riwayat = Stack(kapasitas=10)  # Stack untuk riwayat pencarian

    print("\n  Sistem berhasil dimuat.")
    print(f"  Total buku tersimpan: {len(linked_list)}")

    while True:
        tampilkan_menu()
        pilihan = input("  Pilih menu [0-7]: ").strip()

        if pilihan == '1':
            tampilkan_semua(linked_list)
        elif pilihan == '2':
            tambah_buku(linked_list)
        elif pilihan == '3':
            update_buku(linked_list)
        elif pilihan == '4':
            hapus_buku(linked_list)
        elif pilihan == '5':
            cari_buku(linked_list, riwayat)
        elif pilihan == '6':
            sorting_buku(linked_list)
        elif pilihan == '7':
            tampilkan_riwayat(riwayat)
        elif pilihan == '0':
            print("\n  Terima kasih! Program selesai.\n")
            break
        else:
            print("\n[ERROR] Pilihan tidak valid. Masukkan angka 0-7.")


if __name__ == "__main__":
    main()