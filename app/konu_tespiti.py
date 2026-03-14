# =============================================
# KONU TESPİTİ MODÜLÜ
# Keyword-based yaklaşımla yorumdaki konuları
# tespit eder: Kargo, Kalite, Fiyat, Satıcı
# =============================================

# Her kategori için anahtar kelime listesi
KONU_KEYWORDS = {
    "Kargo": [
        "kargo", "teslimat", "kurye", "gönderim", "paket", "kutu",
        "geç geldi", "hızlı geldi", "teslim", "dağıtım", "gönderi",
        "gecikti", "geç teslim", "hızlı teslimat", "aynı gün",
        "ertesi gün", "zamanında", "bekledim", "gelmedi",
        "kayboldu", "hasarlı paket", "ezilmiş", "ıslak geldi",
        "yanlış adres", "teslim edilmedi", "kapıda ödeme",
        "kargoda bekledi", "şubede bekliyor"
    ],
    "Kalite": [
        "kalite", "bozuk", "sağlam", "dayanıklı", "kırık", "defolu",
        "kaliteli", "kalitesiz", "malzeme", "yapı", "işçilik",
        "mükemmel", "berbat", "harika", "rezalet", "sağlamlık",
        "bozuldu", "çabuk bozul", "kısa sürede bozul", "çürük",
        "çalışmıyor", "çalışmadı", "açılmıyor", "yanmış", "patlak",
        "hatalı", "eksik parça", "kusurlu", "orijinal değil",
        "sahte", "taklit", "plastik gibi", "ucuz malzeme",
        "sağlam değil", "kötü kalite", "iyi kalite", "üst kalite",
        "beklentimi karşıladı", "beklentimi karşılamadı",
        "hayal kırıklığı", "memnun kaldım", "pişman oldum",
        "tavsiye ederim", "tavsiye etmem", "kesinlikle almayın"
    ],
    "Fiyat": [
        "fiyat", "ucuz", "pahalı", "ücret", "değer", "para",
        "fiyatına göre", "ekonomik", "hesaplı", "fiyat/performans",
        "kampanya", "indirim", "değmez", "değer mi", "bütçe dostu",
        "makul fiyat", "fahiş fiyat", "piyasaya göre",
        "daha ucuz", "daha pahalı", "para tuzağı",
        "ödediğime değdi", "ödediğime değmedi", "fiyatı yüksek",
        "fiyatı uygun", "fiyatı makul", "para israfı"
    ],
    "Satıcı": [
        "satıcı", "mağaza", "firma", "şirket", "müşteri hizmetleri",
        "iade", "garanti", "destek", "iletişim", "ilgili", "çözüm",
        "müşteri temsilcisi", "geri dönmedi", "yanıt vermedi",
        "hızlı yanıt", "ilgilendi", "ilgilenmedi", "çözdü",
        "çözmedi", "iade ettim", "iade kabul", "iade reddedildi",
        "garanti kapsamında", "garanti dışı", "yetkili servis",
        "sahte ürün gönderdi", "eksik gönderdi", "yanlış ürün",
        "teşekkürler", "teşekkür ederim", "güvenilir satıcı",
        "güvenilmez", "tekrar alırım", "tekrar almam"
    ]
}


def konu_tespit_et(yorum: str) -> list:
    """
    Verilen yorumda geçen konuları tespit eder.
    Bir yorum birden fazla konuya ait olabilir.
    Hiçbir konu bulunamazsa 'Genel' döndürür.
    
    Args:
        yorum: Analiz edilecek metin
    
    Returns:
        Tespit edilen konu listesi
    """
    yorum_lower = yorum.lower()
    bulunan_konular = []

    for konu, kelimeler in KONU_KEYWORDS.items():
        for kelime in kelimeler:
            if kelime in yorum_lower:
                bulunan_konular.append(konu)
                break  # Bu konudan kelime bulundu, sonrakine geç

    # Hiç konu bulunamazsa Genel olarak etiketle
    if not bulunan_konular:
        bulunan_konular = ["Genel"]

    return bulunan_konular