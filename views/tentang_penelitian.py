import streamlit as st

from src.config import (
    ART_STYLES,
    DATASET_INFO,
    METRICS,
    NPM,
    PEMBIMBING,
    PENULIS,
    PLOTS,
    PRODI,
    TAHUN,
    TRAINING_INFO,
    UNIVERSITAS,
    get_model_size_mb,
)
from src.theme import render_divider, render_hero

render_hero(
    "Tentang <span class='accent'>Penelitian</span>",
    "Profil penelitian, cara kerja model, dan panduan menggunakan aplikasi ini.",
)

tab_profil, tab_model, tab_panduan = st.tabs(["Profil Penelitian", "Tentang Model", "Panduan Penggunaan"])

# ---------- TAB: PROFIL PENELITIAN ----------
with tab_profil:
    st.markdown(
        f"""
        <div class="card">
        <h3>Identitas Penelitian</h3>
        <table style="width:100%; color:#0F172A;">
        <tr><td>Nama</td><td style="text-align:right;">{PENULIS}</td></tr>
        <tr><td>NPM</td><td style="text-align:right;">{NPM}</td></tr>
        <tr><td>Pembimbing</td><td style="text-align:right;">{PEMBIMBING}</td></tr>
        <tr><td>Program Studi</td><td style="text-align:right;">{PRODI}</td></tr>
        <tr><td>Universitas</td><td style="text-align:right;">{UNIVERSITAS}</td></tr>
        <tr><td>Tahun</td><td style="text-align:right;">{TAHUN}</td></tr>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="card">
        <h3>Judul Penelitian</h3>
        <p>Implementasi Transfer Learning ResNet-50 untuk Klasifikasi Citra Karya Seni Lukis Hasil Buatan AI
        dan Manusia pada Aplikasi Web</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tags_html = "".join(f"<span class='style-tag'>{style}</span>" for style in ART_STYLES)
    st.markdown(
        f"""
        <div class="card">
        <h3>Gaya Seni yang Didukung</h3>
        <p class="secondary-text">
        Model paling akurat ketika digunakan pada lukisan dari sepuluh gaya seni berikut, karena hanya
        gaya gaya inilah yang dipelajari model selama proses latihan.
        </p>
        {tags_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- TAB: TENTANG MODEL ----------
with tab_model:
    st.markdown(
        "Bagian ini menjelaskan model kecerdasan buatan yang dipakai oleh aplikasi ini, mulai dari "
        "seberapa baik kinerjanya, bagaimana cara kerjanya, dari mana data latihannya, hingga apa saja "
        "keterbatasannya. Beberapa istilah teknis sengaja diberi penjelasan sederhana agar mudah dipahami."
    )

    model_size = get_model_size_mb()
    model_size_text = f"{model_size:.0f} MB" if model_size else "tidak diketahui"

    st.markdown(
        f"""
        <div class="card">
        <h3>Seberapa Baik Model Ini</h3>
        <p class="secondary-text">
        Angka angka di bawah ini diperoleh dari pengujian model terhadap ribuan gambar yang belum pernah
        dilihat sebelumnya. Semakin mendekati 100% atau 1, semakin baik kinerja model.
        </p>
        <table style="width:100%; color:#0F172A;">
        <tr><td>Akurasi keseluruhan (seberapa sering prediksi model benar)</td><td style="text-align:right;">{METRICS['accuracy']:.2f}%</td></tr>
        <tr><td>Ketepatan saat menebak AI (precision AI)</td><td style="text-align:right;">{METRICS['precision_ai']:.2f}</td></tr>
        <tr><td>Ketepatan saat menebak Manusia (precision Human)</td><td style="text-align:right;">{METRICS['precision_human']:.2f}</td></tr>
        <tr><td>Kemampuan menemukan gambar AI yang sebenarnya (recall AI)</td><td style="text-align:right;">{METRICS['recall_ai']:.2f}</td></tr>
        <tr><td>Kemampuan menemukan gambar Manusia yang sebenarnya (recall Human)</td><td style="text-align:right;">{METRICS['recall_human']:.2f}</td></tr>
        <tr><td>Skor gabungan ketepatan dan kemampuan menemukan, untuk AI (F1 AI)</td><td style="text-align:right;">{METRICS['f1_ai']:.2f}</td></tr>
        <tr><td>Skor gabungan ketepatan dan kemampuan menemukan, untuk Manusia (F1 Human)</td><td style="text-align:right;">{METRICS['f1_human']:.2f}</td></tr>
        <tr><td>Kemampuan model membedakan AI dan Manusia secara umum (AUC-ROC)</td><td style="text-align:right;">{METRICS['auc_roc']:.4f}</td></tr>
        <tr><td>Skor rata rata ketepatan model (Average Precision)</td><td style="text-align:right;">{METRICS['average_precision']:.4f}</td></tr>
        </table>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_roc, col_pr = st.columns(2)
    with col_roc:
        st.image(
            PLOTS["roc"],
            caption="Kurva ROC: makin garis mendekati pojok kiri atas, makin baik model membedakan AI dan Manusia.",
            use_container_width=True,
        )
    with col_pr:
        st.image(
            PLOTS["pr"],
            caption="Kurva Precision-Recall: menunjukkan keseimbangan antara ketepatan dan kemampuan model menemukan gambar yang benar.",
            use_container_width=True,
        )

    st.markdown(
        "Confusion matrix di bawah ini merinci jumlah prediksi benar dan salah pada data uji. "
        "Perbandingan sebelum dan sesudah fine-tuning menunjukkan bahwa melatih ulang sebagian lapisan "
        "ResNet-50 membuat model semakin jarang salah menebak."
    )
    col_cm1, col_cm2 = st.columns(2)
    with col_cm1:
        st.image(
            PLOTS["cm_sebelum"],
            caption="Confusion matrix sebelum fine-tuning (tahap feature extraction).",
            use_container_width=True,
        )
    with col_cm2:
        st.image(
            PLOTS["cm_setelah"],
            caption="Confusion matrix setelah fine-tuning (model akhir yang dipakai aplikasi ini).",
            use_container_width=True,
        )

    render_divider()

    st.markdown(
        """
        <div class="card">
        <h3>Bagaimana Model Melihat Gambar (Grad-CAM)</h3>
        <p class="secondary-text">
        Grad-CAM adalah teknik untuk mengintip bagian gambar mana yang paling diperhatikan model saat
        mengambil keputusan. Area berwarna merah dan kuning adalah bagian yang paling berpengaruh
        terhadap prediksi, sedangkan area biru hampir tidak berpengaruh. Visualisasi yang sama juga
        ditampilkan secara langsung setiap kali Anda menganalisis gambar di halaman Beranda.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_gc1, col_gc2 = st.columns(2)
    with col_gc1:
        st.image(
            PLOTS["gradcam_ai"],
            caption="Contoh Grad-CAM pada gambar buatan AI dari data uji.",
            use_container_width=True,
        )
    with col_gc2:
        st.image(
            PLOTS["gradcam_human"],
            caption="Contoh Grad-CAM pada gambar buatan manusia dari data uji.",
            use_container_width=True,
        )

    render_divider()

    st.markdown(
        f"""
        <div class="card">
        <h3>Bagaimana Model Ini Bekerja</h3>
        <p class="secondary-text">
        Model menggunakan teknik yang disebut transfer learning, yaitu memanfaatkan model yang sudah
        pernah dilatih mengenali jutaan gambar umum, lalu dilatih ulang secara khusus agar bisa membedakan
        lukisan buatan AI dan buatan manusia. Susunan teknisnya adalah sebagai berikut.
        </p>
        <ul>
        <li>ResNet-50, model pengenal gambar yang sudah terlatih pada jutaan foto umum (ImageNet)</li>
        <li>Lapisan peringkas fitur gambar (GlobalAveragePooling2D)</li>
        <li>Lapisan pemroses tambahan berisi 256 neuron (Dense 256, aktivasi relu)</li>
        <li>Lapisan pencegah model terlalu hafal data latihan (Dropout 0,5)</li>
        <li>Lapisan keputusan akhir yang menghasilkan satu angka antara 0 dan 1 (Dense 1, aktivasi sigmoid)</li>
        <li>Ukuran berkas model akhir: sekitar {model_size_text}</li>
        <li>Proses pelatihan dijalankan di {TRAINING_INFO['platform']} menggunakan GPU {TRAINING_INFO['gpu']}</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.image(
        PLOTS["kurva_training"],
        caption=(
            "Kurva pelatihan model pada tahap feature extraction, yaitu tahap awal ketika hanya lapisan "
            "tambahan yang dilatih. Setelah tahap ini, sebagian lapisan ResNet-50 dilatih ulang "
            "(fine-tuning) untuk menghasilkan model akhir."
        ),
        use_container_width=True,
    )

    st.markdown(
        f"""
        <div class="card">
        <h3>Data yang Digunakan untuk Melatih Model</h3>
        <ul>
        <li>Nama kumpulan data: {DATASET_INFO['nama']}</li>
        <li>Total gambar yang dipakai: {DATASET_INFO['total_gambar']}</li>
        <li>Rinciannya: {DATASET_INFO['rincian']}</li>
        <li>Pembagian data: {DATASET_INFO['split']}</li>
        <li>Sumber data: {DATASET_INFO['sumber']}</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.image(
        PLOTS["distribusi"],
        caption="Jumlah gambar AI dan Manusia pada setiap bagian data (training, validasi, dan test) selalu seimbang 50:50.",
        use_container_width=True,
    )

    st.image(
        PLOTS["sampel"],
        caption="Contoh gambar lukisan buatan AI dan buatan manusia dari data training.",
        use_container_width=True,
    )

    with st.expander("Lihat contoh teknik augmentasi data (untuk memperbanyak variasi data latihan)"):
        st.markdown(
            "Augmentasi data adalah teknik membuat variasi baru dari gambar yang sudah ada (dengan cara "
            "dirotasi, dibalik, atau diperbesar/diperkecil) agar model belajar dari lebih banyak variasi "
            "tanpa perlu menambah data asli."
        )
        st.image(PLOTS["augmentasi_ai"], caption="Contoh augmentasi pada gambar buatan AI.", use_container_width=True)
        st.image(PLOTS["augmentasi_human"], caption="Contoh augmentasi pada gambar buatan manusia.", use_container_width=True)

    render_divider()

    st.markdown(
        """
        <div class="card">
        <h3>Keterbatasan Model</h3>
        <p class="secondary-text">
        Seperti model kecerdasan buatan pada umumnya, model ini punya batasan yang penting untuk
        diketahui sebelum Anda mempercayai hasilnya sepenuhnya.
        </p>
        <ul>
        <li>Model hanya dilatih dengan sepuluh gaya lukisan tertentu dari kumpulan data AI-ArtBench,
        sehingga belum tentu akurat untuk gaya lukisan lain.</li>
        <li>Gambar yang bukan lukisan, misalnya foto atau ilustrasi digital modern, berisiko menghasilkan
        prediksi yang kurang akurat.</li>
        <li>Model belum pernah diuji dengan gambar dari alat AI generasi terbaru seperti Midjourney atau
        DALL-E 3, sehingga kemampuannya pada gambar tersebut belum diketahui.</li>
        <li>Sebagian gambar AI dalam data latihan aslinya berukuran besar (768x768 piksel) lalu diperkecil
        menjadi 224x224 piksel, sehingga ada kemungkinan sebagian detail gambar hilang.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.image(
        PLOTS["degradasi"],
        caption=(
            "Ilustrasi penurunan kualitas gambar ketika diperkecil ke ukuran 224x224 piksel sebelum "
            "masuk ke model. Sebagian detail halus bisa hilang dalam proses ini."
        ),
        use_container_width=True,
    )

    st.image(
        PLOTS["misklasifikasi"],
        caption=(
            "Contoh nyata gambar yang salah ditebak oleh model beserta tingkat keyakinannya. Label "
            "'Aktual' adalah kenyataannya, label 'Prediksi' adalah hasil prediksi model. Gambar gambar "
            "ini membantu menunjukkan jenis kesalahan yang masih mungkin terjadi."
        ),
        use_container_width=True,
    )

# ---------- TAB: PANDUAN PENGGUNAAN ----------
with tab_panduan:
    st.markdown(
        "Belum pernah memakai aplikasi seperti ini sebelumnya? Tenang, berikut langkah langkah mudah "
        "untuk mulai menggunakannya."
    )

    steps = [
        ("1", "Siapkan foto atau file gambar lukisan yang ingin dicek, dalam format JPG atau PNG, "
              "dengan ukuran file tidak lebih dari 10MB."),
        ("2", "Buka halaman Beranda, lalu klik area unggah dan pilih gambar tersebut dari komputer Anda."),
        ("3", "Setelah gambar muncul di layar, klik tombol Analisis Gambar dan tunggu sebentar."),
        ("4", "Lihat hasilnya: label AI Generated atau Human Made, persentase tingkat keyakinan sistem, "
              "serta peta Grad-CAM yang menunjukkan bagian gambar yang diperhatikan model."),
        ("5", "Jika muncul peringatan keyakinan rendah (di bawah 60%), anggap hasil prediksi sebagai "
              "perkiraan saja, bukan jawaban pasti."),
    ]

    for number, text in steps:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="step-number">{number}</div>
                <div>{text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="card">
        <h3>Tips untuk Hasil Terbaik</h3>
        <ul>
        <li>Gunakan gambar lukisan dari salah satu sepuluh gaya yang didukung (lihat tab Profil
        Penelitian) agar prediksi model lebih akurat.</li>
        <li>Pilih gambar yang jelas, tidak buram, dan tidak terlalu kecil ukurannya.</li>
        <li>Hindari gambar yang sudah diedit berlebihan, misalnya diberi filter berat atau dipotong
        (crop) terlalu ekstrem.</li>
        <li>Hasil dengan tingkat keyakinan di atas 80% umumnya lebih bisa dipercaya dibanding hasil
        dengan tingkat keyakinan rendah.</li>
        <li>Semua hasil analisis selama sesi berjalan bisa dilihat kembali di halaman Histori.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
