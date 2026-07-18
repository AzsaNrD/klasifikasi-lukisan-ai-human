import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #F7F9FC;
    --card-bg: #FFFFFF;
    --accent: #2563EB;
    --accent-dark: #1D4ED8;
    --accent-soft: #EFF4FF;
    --accent-border: #D6E4FF;
    --ink: #0F172A;
    --text-secondary: #5B6472;
    --red: #DC2626;
    --green: #059669;
    --border-soft: #E4E9F0;
    --shadow-card: 0 1px 2px rgba(15, 23, 42, 0.04), 0 12px 32px rgba(15, 23, 42, 0.06);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: var(--bg);
    color: var(--ink);
}

/* Batas lebar konten utama di semua halaman. Padding samping bawaan
   Streamlit membengkak jadi 5rem di layar lebar; ditimpa agar konten
   mendapat lebar 768px yang sesungguhnya. */
[data-testid="stMainBlockContainer"] {
    max-width: 768px;
    margin: 0 auto;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

h1, h2, h3, h4, .app-heading, .gallery-title {
    font-family: 'Sora', sans-serif;
    color: var(--ink);
}

/* ---------- Header dan navbar atas ---------- */
/* Navbar penuh yang bersih: latar putih transparan dengan blur, garis tipis
   di bawah, dan menu berada di tengah. Lebar kontainer navigasi dibiarkan
   default (penuh) karena Streamlit memakainya untuk mengukur kapan menu
   harus dilipat di layar sempit. */
[data-testid="stHeader"] {
    background-color: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--border-soft);
}

/* Ikon Streamlit adalah teks ligature dari font Material Symbols; font ikon
   tidak boleh ikut diganti, kalau tidak nama ikon tampil sebagai teks mentah. */
[data-testid="stHeader"] :not([data-testid="stIconMaterial"]) {
    font-family: 'Inter', sans-serif;
}

/* Sejajarkan deretan menu dengan kolom konten 768px di bawahnya:
   lebar maksimum sama, diposisikan di tengah, menu rata kiri. */
[data-testid="stHeader"] .rc-overflow {
    max-width: 768px;
    margin: 0 auto;
    justify-content: flex-start;
}

/* Kotak kanan header (bekas tombol Deploy) memakan lebar walau kosong dan
   membuat posisi menu tidak simetris, jadi disembunyikan. Kotak kiri TIDAK
   boleh disembunyikan: di layar sempit Streamlit memindahkan navigasi ke
   menu samping dan menaruh tombol pembukanya di kotak kiri tersebut. */
[data-testid="stToolbar"] > div > :last-child:not(.rc-overflow) {
    display: none;
}

/* Link navigasi dibiarkan mengikuti gaya bawaan Streamlit; hanya warna
   menu yang sedang aktif diberi aksen biru. */
[data-testid="stTopNavLink"][aria-current="page"],
[data-testid="stTopNavLink"][aria-current="page"] span {
    color: var(--accent);
}

/* Sembunyikan tombol Deploy dan menu titik tiga di pojok kanan atas.
   Penting: jangan sembunyikan stToolbar, karena elemen itu membungkus seluruh
   isi header termasuk navigasi. Hapus blok ini jika menu developer dibutuhkan. */
[data-testid="stAppDeployButton"],
[data-testid="stMainMenu"] {
    display: none;
}

/* ---------- Hero ---------- */
.hero-chip {
    display: inline-block;
    background: var(--accent-soft);
    color: var(--accent);
    border: 1px solid var(--accent-border);
    border-radius: 999px;
    padding: 0.35rem 1rem;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1.1rem;
}

.gallery-title {
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.12;
    letter-spacing: -0.02em;
    margin-bottom: 0.4rem;
}

.gallery-title .accent {
    color: var(--accent);
}

.gallery-subtitle {
    font-size: 1.05rem;
    color: var(--text-secondary);
    max-width: 720px;
    line-height: 1.7;
    margin: 0.6rem 0 1.8rem 0;
}

/* ---------- Stat cards di beranda ---------- */
.stat-row {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    margin: 0.4rem 0 1.8rem 0;
}

.stat-card {
    flex: 1;
    min-width: 150px;
    background: var(--card-bg);
    border: 1px solid var(--border-soft);
    border-radius: 16px;
    padding: 1.1rem 1.3rem;
    box-shadow: var(--shadow-card);
}

.stat-card .value {
    font-family: 'Sora', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent);
    line-height: 1.15;
}

.stat-card .label {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-secondary);
    margin-top: 0.15rem;
}

/* ---------- Pemisah dekoratif ---------- */
.ornament-divider {
    display: flex;
    align-items: center;
    margin: 2.4rem 0 1.8rem 0;
}

.ornament-divider::before,
.ornament-divider::after {
    content: "";
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-soft));
}

.ornament-divider::after {
    background: linear-gradient(90deg, var(--border-soft), transparent);
}

.ornament-divider span {
    padding: 0 1rem;
    font-size: 0.8rem;
    color: var(--accent);
}

/* ---------- Kartu ---------- */
.card {
    background-color: var(--card-bg);
    border: 1px solid var(--border-soft);
    border-radius: 16px;
    padding: 1.7rem;
    margin-bottom: 1.3rem;
    box-shadow: var(--shadow-card);
}

.card h3 {
    margin-top: 0;
    font-size: 1.3rem;
    color: var(--ink);
}

.card h3::after {
    content: "";
    display: block;
    width: 44px;
    height: 3px;
    border-radius: 3px;
    background: linear-gradient(90deg, var(--accent), transparent);
    margin-top: 0.5rem;
}

.accent-text { color: var(--accent); }
.secondary-text { color: var(--text-secondary); }

.disclaimer-box {
    background: var(--accent-soft);
    border: 1px solid var(--accent-border);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    color: #1E3A8A;
    margin-bottom: 1.5rem;
    font-size: 0.95rem;
    line-height: 1.6;
}

.small-disclaimer {
    background-color: transparent;
    border: 1px dashed var(--border-soft);
    border-radius: 12px;
    padding: 0.8rem 1rem;
    color: var(--text-secondary);
    font-size: 0.83rem;
    font-style: normal;
    margin-top: 1rem;
}

.empty-state {
    background-color: var(--card-bg);
    border: 1.5px dashed var(--border-soft);
    border-radius: 16px;
    padding: 2.4rem 1.6rem;
    text-align: center;
    color: var(--text-secondary);
    line-height: 1.7;
}

/* ---------- Badge hasil prediksi ---------- */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
    border-radius: 999px;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    padding: 0.6rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.10);
}

.badge::before {
    content: "";
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: currentColor;
    opacity: 0.85;
}

.badge-ai {
    background: linear-gradient(135deg, #DC2626, #F05252);
    color: #FEF2F2;
}

.badge-human {
    background: linear-gradient(135deg, #059669, #34D399);
    color: #ECFDF5;
}

.confidence-number {
    font-family: 'Sora', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.1;
}

.exhibit-label {
    color: var(--text-secondary);
    font-size: 0.88rem;
    margin-top: -0.2rem;
}

/* ---------- Gambar ---------- */
[data-testid="stImage"] img {
    border-radius: 14px;
    border: 1px solid var(--border-soft);
    box-shadow: var(--shadow-card);
    background-color: #ffffff;
}

[data-testid="stImage"] figcaption {
    color: var(--text-secondary) !important;
    text-align: center;
    font-size: 0.83rem;
    margin-top: 0.5rem;
}

/* ---------- Kartu hasil prediksi ---------- */
.st-key-result-card {
    background-color: var(--card-bg);
    border: 1px solid var(--border-soft) !important;
    border-radius: 20px;
    box-shadow: 0 2px 4px rgba(15, 23, 42, 0.04), 0 20px 48px rgba(15, 23, 42, 0.08);
    padding: 0.8rem 0.8rem 1.2rem 0.8rem;
}

/* ---------- Step card panduan ---------- */
.step-card {
    background-color: var(--card-bg);
    border: 1px solid var(--border-soft);
    border-radius: 14px;
    padding: 1.15rem 1.3rem;
    margin-bottom: 0.9rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    box-shadow: var(--shadow-card);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.step-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(15, 23, 42, 0.06), 0 18px 40px rgba(15, 23, 42, 0.09);
}

.step-number {
    font-family: 'Sora', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--accent);
    background: var(--accent-soft);
    border-radius: 10px;
    min-width: 2.4rem;
    height: 2.4rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ---------- Tag gaya seni ---------- */
.style-tag {
    display: inline-block;
    background-color: var(--accent-soft);
    border: 1px solid var(--accent-border);
    color: var(--accent-dark);
    border-radius: 999px;
    padding: 0.3rem 0.95rem;
    margin: 0.18rem;
    font-size: 0.85rem;
    font-weight: 500;
}

/* ---------- Tombol ---------- */
div.stButton > button {
    background-color: var(--accent);
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    letter-spacing: 0.02em;
    padding: 0.65rem 1.7rem;
    transition: all 0.2s ease;
    box-shadow: 0 6px 16px rgba(37, 99, 235, 0.25);
}

div.stButton > button:hover {
    background-color: var(--accent-dark);
    color: #FFFFFF;
    transform: translateY(-2px);
    box-shadow: 0 10px 24px rgba(37, 99, 235, 0.35);
}

div.stButton > button:disabled {
    background-color: var(--border-soft);
    color: var(--text-secondary);
    box-shadow: none;
}

/* ---------- Uploader ---------- */
[data-testid="stFileUploaderDropzone"] {
    background-color: var(--card-bg);
    border: 1.5px dashed #BFCBE0;
    border-radius: 16px;
}

/* ---------- Tabs ---------- */
[data-testid="stTabs"] button[aria-selected="true"] {
    color: var(--accent);
}

hr { border-color: var(--border-soft); }
</style>
"""


def apply_theme():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_divider(symbol: str = "◆"):
    st.markdown(
        f'<div class="ornament-divider"><span>{symbol}</span></div>',
        unsafe_allow_html=True,
    )


def render_hero(title_html: str, subtitle: str, chip: str | None = None):
    if chip:
        st.markdown(f"<span class='hero-chip'>{chip}</span>", unsafe_allow_html=True)
    st.markdown(f"<div class='gallery-title'>{title_html}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='gallery-subtitle'>{subtitle}</div>", unsafe_allow_html=True)


def render_stat_row(stats: list[tuple[str, str]]):
    cards = "".join(
        f"<div class='stat-card'><div class='value'>{value}</div><div class='label'>{label}</div></div>"
        for value, label in stats
    )
    st.markdown(f"<div class='stat-row'>{cards}</div>", unsafe_allow_html=True)
