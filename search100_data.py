import streamlit as st
import random

# ─── BST Node ────────────────────────────────────────────────
class Node:
    def __init__(self, nilai, nama, nisn):
        self.nilai = nilai
        self.nama = nama
        self.nisn = nisn
        self.left = None
        self.right = None

# ─── Binary Search Tree ──────────────────────────────────────
class BST:
    def __init__(self):
        self.root = None

    def insert(self, nilai, nama, nisn):
        self.root = self._insert(self.root, nilai, nama, nisn)

    def _insert(self, node, nilai, nama, nisn):
        if node is None:
            return Node(nilai, nama, nisn)
        if nilai < node.nilai:
            node.left = self._insert(node.left, nilai, nama, nisn)
        else:
            node.right = self._insert(node.right, nilai, nama, nisn)
        return node

    def inorder_desc(self):
        """Traverse right → root → left untuk urutan tertinggi ke terendah"""
        result = []
        self._inorder_desc(self.root, result)
        return result

    def _inorder_desc(self, node, result):
        if node is None:
            return
        self._inorder_desc(node.right, result)
        result.append({"nama": node.nama, "nisn": node.nisn, "nilai": node.nilai})
        self._inorder_desc(node.left, result)

    def search(self, keyword):
        """Cari semua siswa yang cocok dengan nama/NISN"""
        all_data = self.inorder_desc()
        keyword = keyword.lower()
        return [s for s in all_data if keyword in s["nama"].lower() or keyword in s["nisn"]]

# ─── Generate 100 Siswa MI ───────────────────────────────────
NAMA_DEPAN = [
    "Ahmad", "Muhammad", "Fatimah", "Aisyah", "Siti", "Nur", "Abdul",
    "Rizky", "Dini", "Putri", "Zahra", "Hafidz", "Bilal", "Umar",
    "Salma", "Hana", "Ilham", "Yusuf", "Nadia", "Rafi"
]
NAMA_BELAKANG = [
    "Ramadhan", "Hidayat", "Rahmawati", "Kurniawan", "Santoso", "Wijaya",
    "Pratama", "Setiawan", "Nugroho", "Saputra", "Permata", "Hasanah",
    "Firmansyah", "Maulana", "Azzahra", "Kusuma", "Fauzi", "Hakim",
    "Islami", "Rahmat"
]
KELAS = ["4A", "4B", "5A", "5B", "6A", "6B"]

def generate_siswa(n=100):
    random.seed(42)
    siswa = []
    used_nisn = set()
    for i in range(n):
        nama = f"{random.choice(NAMA_DEPAN)} {random.choice(NAMA_BELAKANG)}"
        while True:
            nisn = f"{random.randint(1000000000, 9999999999)}"
            if nisn not in used_nisn:
                used_nisn.add(nisn)
                break
        nilai = random.randint(55, 100)
        kelas = random.choice(KELAS)
        siswa.append({"nama": nama, "nisn": nisn, "nilai": nilai, "kelas": kelas})
    return siswa

# ─── Build BST ───────────────────────────────────────────────
@st.cache_resource
def build_bst():
    bst = BST()
    data = generate_siswa(100)
    for s in data:
        bst.insert(s["nilai"], s["nama"], s["nisn"])
    # Simpan kelas terpisah untuk lookup
    kelas_map = {s["nisn"]: s["kelas"] for s in data}
    return bst, kelas_map

# ─── Streamlit UI ────────────────────────────────────────────
st.set_page_config(
    page_title="Pencarian Siswa MI",
    page_icon="🏫",
    layout="wide",
)

# ─── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
    min-height: 100vh;
}

/* Header banner */
.header-banner {
    background: linear-gradient(90deg, #1a6b3c 0%, #27ae60 50%, #1a6b3c 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    box-shadow: 0 8px 32px rgba(39,174,96,0.25);
    display: flex;
    align-items: center;
    gap: 20px;
}
.header-title {
    font-family: 'Amiri', serif;
    font-size: 2.2rem;
    color: #f0fff4;
    font-weight: 700;
    margin: 0;
    line-height: 1.2;
}
.header-sub {
    font-size: 0.95rem;
    color: #a8f5c0;
    margin: 4px 0 0 0;
}

/* Metric cards */
.metric-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 24px;
}
.metric-card {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 18px 20px;
    text-align: center;
    backdrop-filter: blur(8px);
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #4ade80;
}
.metric-label {
    font-size: 0.78rem;
    color: #94a3b8;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Search box */
.search-container {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 22px 26px;
    margin-bottom: 22px;
    backdrop-filter: blur(10px);
}

/* Table */
.table-wrap {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 16px;
    overflow: hidden;
    backdrop-filter: blur(10px);
}
.table-header {
    background: rgba(39,174,96,0.3);
    padding: 14px 20px;
    font-size: 0.85rem;
    font-weight: 800;
    color: #a8f5c0;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}
.student-row {
    display: grid;
    grid-template-columns: 60px 55px 1fr 150px 100px 130px;
    align-items: center;
    padding: 12px 20px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    transition: background 0.2s;
    color: #e2e8f0;
    font-size: 0.9rem;
}
.student-row:hover {
    background: rgba(74,222,128,0.07);
}
.student-row:last-child { border-bottom: none; }

/* Rank badge */
.rank-badge {
    width: 36px; height: 36px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 0.85rem;
}
.rank-1  { background: linear-gradient(135deg,#ffd700,#ffb300); color:#1a1a00; }
.rank-2  { background: linear-gradient(135deg,#c0c0c0,#a0a0a0); color:#1a1a1a; }
.rank-3  { background: linear-gradient(135deg,#cd7f32,#a0522d); color:#fff; }
.rank-top { background: rgba(74,222,128,0.2); border:1px solid #4ade80; color:#4ade80; }
.rank-mid { background: rgba(251,191,36,0.15); border:1px solid #fbbf24; color:#fbbf24; }
.rank-low { background: rgba(248,113,113,0.15); border:1px solid #f87171; color:#f87171; }

/* Nilai badge */
.nilai-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.88rem;
}
.nilai-a  { background:rgba(74,222,128,0.2); color:#4ade80; border:1px solid #4ade80; }
.nilai-b  { background:rgba(96,165,250,0.2); color:#60a5fa; border:1px solid #60a5fa; }
.nilai-c  { background:rgba(251,191,36,0.2); color:#fbbf24; border:1px solid #fbbf24; }
.nilai-d  { background:rgba(248,113,113,0.2); color:#f87171; border:1px solid #f87171; }

/* Progress bar */
.bar-wrap { background:rgba(255,255,255,0.08); border-radius:4px; height:8px; width:100%; }
.bar-fill { height:8px; border-radius:4px; }

/* Info box */
.info-box {
    background: rgba(39,174,96,0.1);
    border: 1px solid rgba(39,174,96,0.3);
    border-radius: 12px;
    padding: 14px 20px;
    color: #a8f5c0;
    font-size: 0.88rem;
    margin-bottom: 18px;
}

/* Streamlit overrides */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 1rem !important;
    padding: 10px 16px !important;
}
div[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #f1f5f9 !important;
}
label { color: #94a3b8 !important; font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

# ─── Build Data ───────────────────────────────────────────────
bst, kelas_map = build_bst()
all_data = bst.inorder_desc()

# Tambah kelas & rank
for i, s in enumerate(all_data):
    s["rank"] = i + 1
    s["kelas"] = kelas_map.get(s["nisn"], "-")

# ─── Header ──────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <div style="font-size:3rem">🕌</div>
  <div>
    <p class="header-title">Mesin Pencari Siswa MI</p>
    <p class="header-sub">Sistem Perankingan Nilai UAS · Binary Search Tree · 100 Siswa</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Metrics ─────────────────────────────────────────────────
values = [s["nilai"] for s in all_data]
avg_val = sum(values) / len(values)
st.markdown(f"""
<div class="metric-row">
  <div class="metric-card">
    <div class="metric-value">100</div>
    <div class="metric-label">Total Siswa</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">{values[0]}</div>
    <div class="metric-label">Nilai Tertinggi</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">{values[-1]}</div>
    <div class="metric-label">Nilai Terendah</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">{avg_val:.1f}</div>
    <div class="metric-label">Rata-rata Nilai</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Search & Filter ─────────────────────────────────────────
st.markdown('<div class="search-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 1.5, 1.5])
with col1:
    query = st.text_input("🔍 Cari Nama Siswa atau NISN", placeholder="Contoh: Ahmad, Fatimah, 1234...")
with col2:
    kelas_filter = st.selectbox("Kelas", ["Semua"] + sorted(set(kelas_map.values())))
with col3:
    predikat_filter = st.selectbox("Predikat", ["Semua", "A (90–100)", "B (80–89)", "C (70–79)", "D (<70)"])
st.markdown('</div>', unsafe_allow_html=True)

# ─── Filter Logic ────────────────────────────────────────────
if query.strip():
    hasil = bst.search(query.strip())
    for s in hasil:
        s["rank"] = next((r["rank"] for r in all_data if r["nisn"] == s["nisn"]), "-")
        s["kelas"] = kelas_map.get(s["nisn"], "-")
else:
    hasil = all_data.copy()

if kelas_filter != "Semua":
    hasil = [s for s in hasil if s["kelas"] == kelas_filter]

if predikat_filter != "Semua":
    if "A" in predikat_filter:
        hasil = [s for s in hasil if s["nilai"] >= 90]
    elif "B" in predikat_filter:
        hasil = [s for s in hasil if 80 <= s["nilai"] <= 89]
    elif "C" in predikat_filter:
        hasil = [s for s in hasil if 70 <= s["nilai"] <= 79]
    elif "D" in predikat_filter:
        hasil = [s for s in hasil if s["nilai"] < 70]

# ─── Info ────────────────────────────────────────────────────
st.markdown(f"""
<div class="info-box">
  🌳 Data diurutkan menggunakan <strong>In-order Traversal (Kanan → Akar → Kiri)</strong> pada Binary Search Tree (BST) 
  sehingga menghasilkan urutan <strong>nilai UAS dari tertinggi ke terendah</strong>.
  Menampilkan <strong>{len(hasil)}</strong> dari 100 siswa.
</div>
""", unsafe_allow_html=True)

# ─── Helper functions ─────────────────────────────────────────
def get_rank_class(rank):
    if rank == 1: return "rank-1"
    if rank == 2: return "rank-2"
    if rank == 3: return "rank-3"
    if rank <= 30: return "rank-top"
    if rank <= 70: return "rank-mid"
    return "rank-low"

def get_nilai_class(nilai):
    if nilai >= 90: return "nilai-a"
    if nilai >= 80: return "nilai-b"
    if nilai >= 70: return "nilai-c"
    return "nilai-d"

def get_predikat(nilai):
    if nilai >= 90: return "A"
    if nilai >= 80: return "B"
    if nilai >= 70: return "C"
    return "D"

def get_bar_color(nilai):
    if nilai >= 90: return "#4ade80"
    if nilai >= 80: return "#60a5fa"
    if nilai >= 70: return "#fbbf24"
    return "#f87171"

# ─── Table ───────────────────────────────────────────────────
st.markdown("""
<div class="table-wrap">
  <div class="table-header" style="display:grid; grid-template-columns:60px 55px 1fr 150px 100px 130px; gap:0;">
    <span>Rank</span><span>No</span><span>Nama Siswa</span>
    <span>NISN</span><span>Kelas</span><span>Nilai UAS</span>
  </div>
""", unsafe_allow_html=True)

if not hasil:
    st.markdown('<div style="padding:40px;text-align:center;color:#64748b;font-size:1rem;">Tidak ada siswa ditemukan 😔</div>', unsafe_allow_html=True)
else:
    for i, s in enumerate(hasil, 1):
        rank = s["rank"]
        rc = get_rank_class(rank)
        nc = get_nilai_class(s["nilai"])
        pred = get_predikat(s["nilai"])
        bc = get_bar_color(s["nilai"])
        pct = (s["nilai"] / 100) * 100

        st.markdown(f"""
        <div class="student-row">
          <div><span class="rank-badge {rc}">{rank}</span></div>
          <div style="color:#64748b;font-size:0.82rem;">{i}</div>
          <div>
            <div style="font-weight:700;color:#f1f5f9;">{s['nama']}</div>
            <div class="bar-wrap" style="margin-top:5px;">
              <div class="bar-fill" style="width:{pct}%;background:{bc};"></div>
            </div>
          </div>
          <div style="font-size:0.8rem;color:#64748b;font-family:monospace;">{s['nisn']}</div>
          <div><span style="background:rgba(255,255,255,0.08);border-radius:6px;padding:3px 10px;font-size:0.85rem;color:#cbd5e1;">{s['kelas']}</span></div>
          <div>
            <span class="nilai-badge {nc}">{s['nilai']} · {pred}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:30px 0 10px;color:#334155;font-size:0.82rem;">
  Sistem Informasi Akademik MI · Binary Search Tree (BST) · Algoritma In-order Traversal Descending
</div>
""", unsafe_allow_html=True)