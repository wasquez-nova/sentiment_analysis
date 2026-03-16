# 💬 Türkçe Ürün Yorumu Duygu Analizi ve Akıllı Memnuniyet Takip Sistemi

Türkçe e-ticaret yorumlarını yapay zeka ile analiz eden, yorumları olumlu/olumsuz olarak sınıflandıran ve kullanıcıya görsel bir memnuniyet raporu sunan akıllı bir sistemdir.

## 🎯 Özellikler

- Türkçe yorumları **Olumlu / Olumsuz** olarak sınıflandırır
- Yorumlarda geçen konuları tespit eder: **Kargo, Kalite, Fiyat, Satıcı**
- Toplu analiz: CSV veya Excel dosyası yükleyerek binlerce yorumu tek tıkla analiz eder
- Tek yorum testi: Anlık yorum analizi yapılabilir
- Görsel dashboard: Pasta grafik, bar grafik, kelime bulutu
- Genel memnuniyet skoru ve otomatik özet metin
- Analiz raporunu CSV olarak indirebilme

## 🛠️ Kullanılan Teknolojiler

| Bileşen | Teknoloji |
|---|---|
| Model | BERTurk (dbmdz/bert-base-turkish-cased) |
| Model Eğitimi | Hugging Face Transformers + Fine-tuning |
| Arayüz | Streamlit |
| Grafikler | Plotly + WordCloud |
| Veri İşleme | Pandas |
| Geliştirme | Python 3.12, MacBook M4 Air + Google Colab |

## 📊 Model Performansı

| Metrik | Değer |
|---|---|
| Accuracy | %90.6 |
| F1 Score | 0.91 |
| Eğitim Verisi | 21.398 Türkçe yorum |
| Test Verisi | 5.350 Türkçe yorum |

## 🚀 Kurulum

### Gereksinimler
- Python 3.10+
- pip

### Adımlar

1. Repoyu klonla:
\`\`\`bash
git clone https://github.com/wasquez-nova/sentiment_analysis.git
cd sentiment_analysis
\`\`\`

2. Sanal ortam oluştur ve aktif et:
\`\`\`bash
python -m venv venv
source venv/bin/activate
\`\`\`

3. Kütüphaneleri kur:
\`\`\`bash
pip install transformers torch streamlit pandas plotly wordcloud openpyxl datasets
\`\`\`

4. Uygulamayı başlat:
\`\`\`bash
streamlit run app/dashboard.py
\`\`\`

## 📁 Proje Yapısı

\`\`\`
sentiment_analysis/
├── app/
│   ├── dashboard.py        # Streamlit arayüzü
│   ├── analiz.py           # Duygu analizi modülü
│   └── konu_tespiti.py     # Konu tespiti modülü
├── data/
│   └── yorumlar.csv        # Eğitim veri seti
├── model/                  # Eğitilmiş BERTurk modeli
├── notebooks/
│   └── veri_inceleme.py    # Veri keşif scripti
└── README.md
\`\`\`

## 👤 Geliştirici

**Ümit Çakmak** — Bilgisayar Mühendisliği Bitirme Ödevi, 2025/2026 Bahar