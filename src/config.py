import os

MODEL_PATH = "models/model_resnet50_finetuned.h5"
HF_REPO_ID = "azsanrd/resnet50-ai-human-art"
HF_MODEL_FILENAME = "model_resnet50_finetuned.h5"
IMG_SIZE = (224, 224)
MAX_FILE_SIZE_MB = 10
ALLOWED_FORMATS = ["jpg", "jpeg", "png"]
PLOTS_DIR = "assets/baru"

PLOTS = {
    "distribusi": f"{PLOTS_DIR}/Distribusi Dataset.jpg",
    "sampel": f"{PLOTS_DIR}/Sampel Gambar Dataset.jpg",
    "augmentasi_ai": f"{PLOTS_DIR}/Visualisasi Augmentasi Kelas AI.jpg",
    "augmentasi_human": f"{PLOTS_DIR}/Visualisasi Augmentasi Kelas Human.jpg",
    "kurva_training": f"{PLOTS_DIR}/Kurva Training Tahap Feature Extraction.jpg",
    "cm_sebelum": f"{PLOTS_DIR}/Confusion Matrix Sebelum Fine Tuning.jpg",
    "cm_setelah": f"{PLOTS_DIR}/Confusion Matrix Setelah Fine Tuning.jpg",
    "roc": f"{PLOTS_DIR}/ROC Curve.jpg",
    "pr": f"{PLOTS_DIR}/Precision Recall Curve.jpg",
    "misklasifikasi": f"{PLOTS_DIR}/Analisis Kesalahan Klasifikasi.jpg",
    "gradcam_ai": f"{PLOTS_DIR}/Grad-Cam AI Generated.jpg",
    "gradcam_human": f"{PLOTS_DIR}/Grad-Cam Human Generated.jpg",
    "degradasi": f"{PLOTS_DIR}/Visualisasi Degradasi Kualitas Gambar.jpg",
}

ART_STYLES = [
    "Art Nouveau", "Baroque", "Expressionism", "Impressionism",
    "Post Impressionism", "Realism", "Renaissance", "Romanticism",
    "Surrealism", "Ukiyo-e",
]

PENULIS = "Azsa Nurwahyudi"
NPM = "10122257"
PEMBIMBING = "Dr. Syamsi Ruhama, SKom., MMSI."
PRODI = "Sistem Informasi"
UNIVERSITAS = "Gunadarma"
TAHUN = "2026"

METRICS = {
    "accuracy": 92.45,
    "precision_ai": 0.92,
    "recall_ai": 0.94,
    "f1_ai": 0.93,
    "precision_human": 0.93,
    "recall_human": 0.91,
    "f1_human": 0.92,
    "auc_roc": 0.9786,
    "average_precision": 0.9779,
}

DATASET_INFO = {
    "nama": "AI-ArtBench",
    "total_gambar": "120.000 gambar lukisan",
    "rincian": (
        "60.000 gambar buatan AI (30.000 dari teknik Latent Diffusion dan 30.000 dari teknik Standard "
        "Diffusion), serta 60.000 gambar buatan manusia"
    ),
    "split": "80% untuk melatih model, 10% untuk mengecek selama proses latihan, dan 10% untuk menguji model di akhir",
    "sumber": "Silva dan kawan kawan, tahun 2024",
}

TRAINING_INFO = {
    "platform": "Google Colab",
    "gpu": "NVIDIA L4",
}


def get_model_size_mb() -> float:
    try:
        return os.path.getsize(MODEL_PATH) / (1024 * 1024)
    except OSError:
        # Saat deploy, model diunduh dari Hugging Face Hub (bukan di MODEL_PATH),
        # jadi pakai ukuran file yang diketahui sebagai fallback.
        return 189.0
