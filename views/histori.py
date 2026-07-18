import streamlit as st

from src.theme import render_hero

render_hero(
    "Histori <span class='accent'>Analisis</span>",
    "Daftar gambar yang sudah Anda analisis selama sesi ini beserta hasil prediksinya. "
    "Riwayat hanya tersimpan sementara dan akan terhapus otomatis jika halaman direfresh "
    "atau browser ditutup.",
)

history = st.session_state.get("riwayat", [])

if not history:
    st.markdown(
        """
        <div class="empty-state">
        Belum ada riwayat analisis pada sesi ini.<br>
        Silakan buka halaman <strong>Beranda</strong>, unggah gambar lukisan, lalu klik tombol
        <strong>Analisis Gambar</strong>. Hasil analisisnya akan otomatis tercatat di halaman ini.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    total = len(history)
    st.markdown(f"Total analisis pada sesi ini: **{total} gambar**.")

    if st.button("Hapus Semua Riwayat"):
        st.session_state["riwayat"] = []
        st.rerun()

    for index, item in enumerate(reversed(history)):
        nomor = total - index
        with st.container(border=True):
            col_img, col_info = st.columns([1, 2.6])

            with col_img:
                st.image(item["thumbnail"], use_container_width=True)

            with col_info:
                badge_class = "badge-ai" if item["label"] == "AI Generated" else "badge-human"
                st.markdown(
                    f"<div class='badge {badge_class}'>{item['label']}</div>",
                    unsafe_allow_html=True,
                )
                st.markdown(f"**Tingkat keyakinan: {item['confidence']:.2f}%**")
                st.caption(f"Analisis ke-{nomor} · Nama file: {item['nama_file']} · Waktu: {item['waktu']}")
                st.caption(
                    f"Kemungkinan AI: {item['prob_ai']:.2f}% · "
                    f"Kemungkinan Manusia: {item['prob_human']:.2f}%"
                )
