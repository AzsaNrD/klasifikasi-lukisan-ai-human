from datetime import datetime

import streamlit as st
from PIL import Image

from src.config import ALLOWED_FORMATS, IMG_SIZE, MAX_FILE_SIZE_MB, METRICS
from src.model import compute_gradcam, predict
from src.theme import render_divider, render_hero, render_stat_row

render_hero(
    "Pendeteksi Gambar <span class='accent'>Lukisan Buatan AI</span>",
    "Beberapa tahun belakangan, teknologi kecerdasan buatan berkembang sangat pesat, termasuk untuk "
    "membuat gambar dari teks lewat model text-to-image seperti DALL-E, Midjourney, dan Stable "
    "Diffusion. Hasilnya bisa sangat mirip dengan lukisan buatan tangan manusia, dan tidak jarang "
    "disalahgunakan, misalnya dijual sebagai karya tangan asli tanpa pemberitahuan. Aplikasi ini "
    "membantu Anda memeriksa apakah sebuah gambar lukisan merupakan hasil buatan AI atau buatan "
    "manusia, menggunakan model Transfer Learning ResNet-50, lengkap dengan tingkat keyakinan dan "
    "peta area gambar yang diperhatikan model.",
    chip="Skripsi · Sistem Informasi · Universitas Gunadarma 2026",
)

render_stat_row([
    (f"{METRICS['accuracy']:.2f}%".replace(".", ","), "Akurasi model"),
    (f"{METRICS['auc_roc']:.4f}".replace(".", ","), "AUC-ROC"),
    ("120.000", "Gambar data latih"),
    ("10", "Gaya seni didukung"),
])

st.markdown(
    """
    <div class="disclaimer-box">
    <strong>Perhatian:</strong> sistem ini paling akurat untuk lukisan dari sepuluh gaya seni tertentu
    (lihat halaman Tentang untuk daftarnya, misalnya Realism, Baroque, Impressionism, dan lainnya).
    Jika Anda mengunggah foto biasa, ilustrasi digital modern, atau gambar yang bukan lukisan,
    hasil prediksi mungkin kurang akurat karena di luar kemampuan model.
    </div>
    """,
    unsafe_allow_html=True,
)

sumber = st.radio(
    "Sumber gambar",
    ["Unggah dari file", "Ambil dari kamera"],
    horizontal=True,
    help=(
        "Pilih Unggah dari file untuk memakai gambar dari galeri atau komputer Anda. "
        "Pilih Ambil dari kamera untuk memotret lukisan langsung dari kamera perangkat."
    ),
)

if sumber == "Unggah dari file":
    uploaded_file = st.file_uploader(
        "Unggah Gambar Karya Seni",
        type=ALLOWED_FORMATS,
        help="Format yang diterima: JPG dan PNG. Ukuran file maksimal 10MB.",
    )
else:
    uploaded_file = st.camera_input(
        "Arahkan kamera ke lukisan, lalu klik tombol untuk mengambil foto",
        help=(
            "Browser akan meminta izin mengakses kamera terlebih dahulu. "
            "Jika kamera tidak muncul, pastikan izin kamera sudah diberikan."
        ),
    )

valid_file = False
image = None

if uploaded_file is not None:
    file_size_mb = uploaded_file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(
            f"Ukuran file Anda {file_size_mb:.1f}MB, melebihi batas maksimal {MAX_FILE_SIZE_MB}MB. "
            "Silakan kompres atau gunakan gambar dengan ukuran file yang lebih kecil."
        )
    else:
        image = Image.open(uploaded_file)
        valid_file = True
        if sumber == "Unggah dari file":
            st.image(image, caption="Gambar yang diunggah", width=400)

analyze_clicked = st.button("Analisis Gambar", disabled=not valid_file)

if analyze_clicked and valid_file:
    with st.spinner("Memproses gambar dan melakukan prediksi..."):
        result = predict(image)
        try:
            gradcam_image = compute_gradcam(image, result["raw_prob"])
        except Exception:
            gradcam_image = None

    thumbnail = image.copy()
    thumbnail.thumbnail((320, 320))
    st.session_state.setdefault("riwayat", []).append({
        "thumbnail": thumbnail,
        "nama_file": uploaded_file.name,
        "label": result["label"],
        "confidence": result["confidence"],
        "prob_ai": result["prob_ai"],
        "prob_human": result["prob_human"],
        "waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    })

    render_divider()

    with st.container(border=True, key="result-card"):
        col1, col2 = st.columns([1, 1.1])

        with col1:
            st.image(image, caption="Gambar yang dianalisis", use_container_width=True)

        with col2:
            badge_class = "badge-ai" if result["label"] == "AI Generated" else "badge-human"
            badge_text = "AI Generated" if result["label"] == "AI Generated" else "Human Made"
            st.markdown(f"<div class='badge {badge_class}'>{badge_text}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='confidence-number'>{result['confidence']:.2f}%</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p class='exhibit-label'>Tingkat keyakinan sistem terhadap prediksi di atas</p>",
                unsafe_allow_html=True,
            )

            st.markdown(
                "Di bawah ini adalah seberapa besar kemungkinan gambar termasuk masing masing kategori "
                "menurut sistem. Kedua angka ini bila dijumlahkan akan menjadi 100%."
            )

            st.markdown("**Kemungkinan dibuat oleh AI**")
            st.progress(min(max(result["prob_ai"] / 100, 0.0), 1.0))
            st.caption(f"{result['prob_ai']:.2f}%")

            st.markdown("**Kemungkinan dibuat oleh Manusia**")
            st.progress(min(max(result["prob_human"] / 100, 0.0), 1.0))
            st.caption(f"{result['prob_human']:.2f}%")

            confidence_ratio = result["confidence"] / 100
            if confidence_ratio < 0.60:
                st.warning(
                    "Keyakinan sistem terhadap prediksi ini masih di bawah 60%, artinya sistem cukup ragu. "
                    "Bisa jadi gambar yang Anda unggah bukan termasuk gaya lukisan yang dikenali model."
                )
            elif confidence_ratio < 0.80:
                st.info(
                    "Keyakinan sistem terhadap prediksi ini cukup baik (60% sampai 80%), sehingga hasilnya "
                    "cukup bisa dipercaya."
                )
            else:
                st.success(
                    "Keyakinan sistem terhadap prediksi ini sangat tinggi (di atas 80%), sehingga hasilnya "
                    "sangat bisa dipercaya."
                )

        if gradcam_image is not None:
            st.markdown("#### Bagian Gambar yang Diperhatikan Model (Grad-CAM)")
            st.markdown(
                "Visualisasi di bawah ini disebut Grad-CAM. Area berwarna merah dan kuning adalah bagian "
                "gambar yang paling diperhatikan model saat mengambil keputusan, sedangkan area biru "
                "hampir tidak berpengaruh terhadap hasil prediksi."
            )
            gcol1, gcol2 = st.columns(2)
            with gcol1:
                st.image(image, caption="Gambar asli", use_container_width=True)
            with gcol2:
                st.image(
                    gradcam_image,
                    caption="Peta perhatian model (merah = paling diperhatikan)",
                    use_container_width=True,
                )
        else:
            st.info(
                "Visualisasi Grad-CAM tidak dapat dibuat untuk gambar ini, namun hasil prediksi di atas "
                "tetap berlaku."
            )

        with st.expander("Detail Teknis (untuk yang ingin tahu lebih dalam)"):
            st.write(
                f"Nilai mentah yang dihasilkan model (disebut nilai sigmoid): `{result['raw_prob']:.4f}`. "
                "Nilai ini berkisar antara 0 dan 1."
            )
            st.write(
                "**Apa itu threshold?** Threshold adalah batas angka yang dipakai sistem untuk "
                "memutuskan suatu gambar masuk kategori AI atau Manusia. Pada aplikasi ini, threshold "
                "yang dipakai adalah **0.5**. Jika nilai mentah di atas kurang dari atau sama dengan "
                "0.5, gambar dianggap **dibuat oleh AI**. Jika nilai mentah lebih besar dari 0.5, "
                "gambar dianggap **dibuat oleh Manusia**. Semakin jauh nilai dari batas 0.5 ini "
                "(mendekati 0 atau mendekati 1), semakin yakin sistem terhadap prediksinya."
            )
            st.markdown("---")
            st.write(f"Nama file: `{uploaded_file.name}`")
            st.write(f"Ukuran file: `{uploaded_file.size / 1024:.1f} KB`")
            st.write(f"Dimensi asli: `{image.width} x {image.height} piksel`")
            st.write(
                f"Dimensi setelah diproses sistem: `{IMG_SIZE[0]} x {IMG_SIZE[1]} piksel` "
                "(semua gambar diubah ukurannya ke ukuran ini sebelum dianalisis oleh model)."
            )

        st.markdown(
            """
            <div class="small-disclaimer">
            Catatan: hasil prediksi ini hanya bersifat perkiraan dari sistem dan tidak dapat dijadikan
            satu satunya bukti atau dasar penilaian resmi mengenai keaslian sebuah karya seni. Hasil
            analisis ini juga tercatat di halaman Histori selama sesi masih berjalan.
            </div>
            """,
            unsafe_allow_html=True,
        )
