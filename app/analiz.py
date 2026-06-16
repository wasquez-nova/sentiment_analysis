# ANALİZ MODÜLÜ
# BERTurk modelini yükler ve tek bir yorumu
# duygu + konu açısından analiz eder.


import torch
import sys
sys.path.append("/Users/umit/Desktop/sentiment_analysis")

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.konu_tespiti import konu_tespit_et

MODEL_PATH = "model/"

# Tokenizer ve modeli yükle
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()  # Modeli tahmin moduna al

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


def yorumu_analiz_et(yorum: str) -> dict:
    """
    Tek bir Türkçe yorumu analiz eder.
    
    Args:
        yorum: Analiz edilecek metin
    
    Returns:
        yorum, duygu ve konuları içeren sözlük
    """
    # Metni modelin anlayacağı formata çevir
    inputs = tokenizer(
        yorum,
        return_tensors="pt",
        max_length=128,
        truncation=True,
        padding="max_length"
    ).to(device)

    # Tahmin yap
    with torch.no_grad():
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()

    duygu = "Olumlu" if pred == 1 else "Olumsuz"
    
    # Konu tespiti yap
    konular = konu_tespit_et(yorum)

    return {
        "yorum": yorum,
        "duygu": duygu,
        "konular": konular
    }