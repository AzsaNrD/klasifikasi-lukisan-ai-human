# Klasifikasi Lukisan AI vs Manusia

Aplikasi web untuk mendeteksi apakah sebuah gambar lukisan merupakan hasil buatan AI atau buatan manusia, menggunakan model Transfer Learning ResNet-50. Dibangun dengan Streamlit sebagai bagian dari penulisan ilmiah di Universitas Gunadarma.

## Fitur

- Prediksi AI Generated vs Human Made beserta tingkat keyakinan dan probabilitas tiap kelas
- Input gambar dari file (JPG/PNG, maks 10MB) atau langsung dari kamera
- Visualisasi Grad-CAM yang menunjukkan area gambar yang paling diperhatikan model
- Histori analisis selama sesi berjalan
- Halaman informasi penelitian: metrik evaluasi, dataset, arsitektur model, dan panduan penggunaan

## Model

- Arsitektur: ResNet-50 (transfer learning + fine-tuning), input 224x224
- Dataset: AI-ArtBench (120.000 gambar, 10 gaya seni)
- Akurasi 92,45% dan AUC-ROC 0,9786 pada data uji
- Bobot model diunduh otomatis dari [Hugging Face Hub](https://huggingface.co/azsanrd/resnet50-ai-human-art) saat aplikasi pertama kali dijalankan

## Menjalankan Secara Lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Struktur Proyek

```
app.py                  # entrypoint dan navigasi
views/                  # halaman aplikasi (Beranda, Histori, Tentang Penelitian)
src/                    # konfigurasi, pemuatan model, prediksi, Grad-CAM, tema
assets/baru/            # grafik hasil training dan evaluasi model
.streamlit/config.toml  # tema dan batas ukuran unggahan
```
