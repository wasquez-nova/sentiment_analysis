# =============================================
# DASHBOARD MODÜLÜ
# Kullanıcının yorumları yükleyip analiz
# edebildiği Streamlit web arayüzü.
# =============================================

import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import sys
sys.path.append("/Users/umit/Desktop/sentiment_analysis")
from app.analiz import yorumu_analiz_et

# Sayfa ayarları
st.set_page_config(
    page_title="Türkçe Yorum Analizi",
    page_icon="💬",
    layout="wide"
)

# Tema toggle butonu - sağ üst
if "tema" not in st.session_state:
    st.session_state.tema = "koyu"

col_bos, col_tema = st.columns([11, 1])
with col_tema:
    if st.button("☀️" if st.session_state.tema == "koyu" else "🌙"):
        st.session_state.tema = "acik" if st.session_state.tema == "koyu" else "koyu"
        st.rerun()

if st.session_state.tema == "acik":
    st.markdown("""
    <style>
        .stApp { background-color: #f0f2f6; color: #2c2f3a; }
        div[data-testid="stMetric"] { background-color: #ffffff; border-radius: 12px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        div[data-testid="stFileUploader"] { background-color: #ffffff; border-radius: 12px; }
        .stDataFrame { background-color: #ffffff; border-radius: 12px; }
        .stButton button { border-radius: 8px; }
        h1, h2, h3 { color: #2c2f3a; }
        p, label { color: #3d4155; }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp { background-color: #1a1d27; color: #dde1f0; }
        div[data-testid="stMetric"] { background-color: #23273a; border-radius: 12px; padding: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.2); }
        div[data-testid="stFileUploader"] { background-color: #23273a; border-radius: 12px; }
        .stButton button { border-radius: 8px; }
        h1, h2, h3 { color: #dde1f0; }
        p, label { color: #b0b8d1; }
    </style>
    """, unsafe_allow_html=True)

# Başlık
st.title("💬 Türkçe Ürün Yorumu Duygu Analizi")
st.markdown("Excel veya CSV dosyanızı yükleyin, yorumlarınızı otomatik analiz edelim.")
# Tek yorum test alanı
st.subheader("🔎 Tek Yorum Test Et")
tek_yorum = st.text_area("Analiz etmek istediğiniz yorumu yazın:", placeholder="Örnek: Ürün çok kaliteliydi, kargo da hızlı geldi.")

if st.button("Analiz Et"):
    if tek_yorum.strip():
        with st.spinner("Analiz ediliyor..."):
            sonuc = yorumu_analiz_et(tek_yorum)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if sonuc["duygu"] == "Olumlu":
                st.success(f"✅ Duygu: {sonuc['duygu']}")
            else:
                st.error(f"❌ Duygu: {sonuc['duygu']}")
        with col_b:
            st.info(f"🏷️ Konu: {', '.join(sonuc['konular'])}")
    else:
        st.warning("Lütfen bir yorum girin.")

st.divider()

# Dosya yükleme
uploaded_file = st.file_uploader(
    "Yorum dosyanızı yükleyin",
    type=["csv", "xlsx"],
    help="Dosyanızda 'text' adında bir sütun olmalıdır."
)

if uploaded_file:
    # Dosyayı oku
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success(f"{len(df)} yorum yüklendi!")
    st.dataframe(df.head(5))

    # Analiz butonu
    if st.button("🔍 Analizi Başlat"):
        with st.spinner("Yorumlar analiz ediliyor, lütfen bekleyin..."):
            sonuclar = []
            for yorum in df["text"]:
                sonuc = yorumu_analiz_et(str(yorum))
                sonuclar.append(sonuc)

            sonuc_df = pd.DataFrame(sonuclar)
            st.session_state["sonuc_df"] = sonuc_df

        st.success("Analiz tamamlandı!")
        st.dataframe(sonuc_df)

        # Sonuçlar varsa grafikleri göster
if "sonuc_df" in st.session_state:
    sonuc_df = st.session_state["sonuc_df"]
    st.divider()
    st.subheader("📊 Analiz Sonuçları")

    # Üst metrikler
    col1, col2, col3 = st.columns(3)
    toplam = len(sonuc_df)
    olumlu = len(sonuc_df[sonuc_df["duygu"] == "Olumlu"])
    olumsuz = len(sonuc_df[sonuc_df["duygu"] == "Olumsuz"])
    memnuniyet = round((olumlu / toplam) * 100, 1)

    col1.metric("Toplam Yorum", toplam)
    col2.metric("Olumlu", olumlu)
    col3.metric("Olumsuz", olumsuz)

    st.divider()

    # Duygu dağılımı pasta grafiği
    col4, col5 = st.columns(2)

    with col4:
        st.subheader("💬 Duygu Dağılımı")
        duygu_sayilari = sonuc_df["duygu"].value_counts().reset_index()
        duygu_sayilari.columns = ["Duygu", "Sayı"]
        fig1 = px.pie(duygu_sayilari, values="Sayı", names="Duygu",
                      color_discrete_map={"Olumlu": "#2ecc71", "Olumsuz": "#e74c3c"})
        st.plotly_chart(fig1, use_container_width=True)

    with col5:
        st.subheader("🏷️ Konu Dağılımı")
        tum_konular = []
        for konular in sonuc_df["konular"]:
            tum_konular.extend(konular)
        konu_df = pd.Series(tum_konular).value_counts().reset_index()
        konu_df.columns = ["Konu", "Sayı"]
        fig2 = px.bar(konu_df, x="Konu", y="Sayı",
                      color="Sayı", color_continuous_scale="blues")
        st.plotly_chart(fig2, use_container_width=True)

    # Memnuniyet skoru
    st.divider()
    st.subheader(f"⭐ Genel Memnuniyet Skoru: %{memnuniyet}")
    st.progress(memnuniyet / 100)

    

    # Konu bazında duygu dağılımı
    st.divider()
    st.subheader("🔍 Konu Bazında Duygu Dağılımı")

    konu_duygu = []
    for _, row in sonuc_df.iterrows():
        for konu in row["konular"]:
            konu_duygu.append({"Konu": konu, "Duygu": row["duygu"]})

    konu_duygu_df = pd.DataFrame(konu_duygu)
    konu_duygu_count = konu_duygu_df.groupby(["Konu", "Duygu"]).size().reset_index(name="Sayı")

    fig4 = px.bar(
        konu_duygu_count, x="Konu", y="Sayı", color="Duygu", barmode="group",
        color_discrete_map={"Olumlu": "#2ecc71", "Olumsuz": "#e74c3c"}
    )
    st.plotly_chart(fig4, use_container_width=True)


    # Otomatik özet metin
    st.divider()
    st.subheader("📝 Genel Değerlendirme")

    # Verileri hesapla
    en_cok_konu = konu_df.iloc[0]["Konu"] if len(konu_df) > 0 else "Genel"
    
    olumsuz_konular = konu_duygu_df[konu_duygu_df["Duygu"] == "Olumsuz"]["Konu"].value_counts()
    en_cok_sikayet = olumsuz_konular.index[0] if len(olumsuz_konular) > 0 else None
    en_cok_sikayet_sayi = olumsuz_konular.iloc[0] if len(olumsuz_konular) > 0 else 0

    olumlu_konular = konu_duygu_df[konu_duygu_df["Duygu"] == "Olumlu"]["Konu"].value_counts()
    en_cok_begeni = olumlu_konular.index[0] if len(olumlu_konular) > 0 else None
    en_cok_begeni_sayi = olumlu_konular.iloc[0] if len(olumlu_konular) > 0 else 0

    # Memnuniyet seviyesi
    if memnuniyet >= 75:
        genel_durum = "oldukça olumlu bir tablo"
        tavsiye = "Mevcut kalite standardını korumanız önerilir."
    elif memnuniyet >= 50:
        genel_durum = "kısmen olumlu bir tablo"
        tavsiye = "Olumsuz geri bildirimlerin üzerine odaklanılması önerilir."
    else:
        genel_durum = "olumsuz bir tablo"
        tavsiye = "Acil iyileştirme adımları atılması önerilir."

    # Özet metni oluştur
    ozet = f"""
    Toplam **{toplam}** müşteri yorumu analiz edildi. Yorumların **%{memnuniyet}'i olumlu**, 
    **%{round(100 - memnuniyet, 1)}'i olumsuz** olarak değerlendirildi. Bu oran genel olarak **{genel_durum}** 
    ortaya koymaktadır.

    Müşterilerin en çok yorum yaptığı konu **{en_cok_konu}** oldu. """

    if en_cok_begeni:
        ozet += f"Olumlu yorumlarda en fazla öne çıkan konu **{en_cok_begeni}** olurken ({en_cok_begeni_sayi} yorum), "
    
    if en_cok_sikayet:
        ozet += f"olumsuz yorumlarda en çok şikayet edilen konu **{en_cok_sikayet}** oldu ({en_cok_sikayet_sayi} yorum). "

    ozet += f"\n\n**Öneri:** {tavsiye}"

    st.info(ozet)

    # Olumlu/olumsuz ayrı tablolar
    st.divider()
    st.subheader("📋 Yorumlar")

    col6, col7 = st.columns(2)

    with col6:
        st.markdown("### ✅ Olumlu Yorumlar")
        olumlu_df = sonuc_df[sonuc_df["duygu"] == "Olumlu"][["yorum", "konular"]].reset_index(drop=True)
        olumlu_df["konular"] = olumlu_df["konular"].apply(lambda x: ", ".join(x))
        st.dataframe(olumlu_df, use_container_width=True)

    with col7:
        st.markdown("### ❌ Olumsuz Yorumlar")
        olumsuz_df = sonuc_df[sonuc_df["duygu"] == "Olumsuz"][["yorum", "konular"]].reset_index(drop=True)
        olumsuz_df["konular"] = olumsuz_df["konular"].apply(lambda x: ", ".join(x))
        st.dataframe(olumsuz_df, use_container_width=True)

    # Kelime bulutu
    st.divider()
    st.subheader("☁️ Kelime Bulutu")

    tum_metin = " ".join(sonuc_df["yorum"].tolist())
    wordcloud = WordCloud(
        width=800, height=400,
        background_color="white",
        colormap="RdYlGn",
        font_path=None
    ).generate(tum_metin)

    fig3, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig3)

    # İndirilebilir rapor
    st.divider()
    st.subheader("📥 Raporu İndir")

    csv = sonuc_df.copy()
    csv["konular"] = csv["konular"].apply(lambda x: ", ".join(x))
    csv_data = csv.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📄 CSV Olarak İndir",
        data=csv_data,
        file_name="analiz_raporu.csv",
        mime="text/csv"
    )

    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    import tempfile
    import os

    def pdf_olustur(sonuc_df, memnuniyet, toplam, olumlu, olumsuz):
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        import urllib.request

        # Türkçe destekleyen font indir
        pdfmetrics.registerFont(TTFont("DejaVu", "/Library/Fonts/Arial Unicode.ttf"))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/Library/Fonts/Arial Unicode.ttf"))

        buffer = io.BytesIO()
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        genislik, yukseklik = A4

        # --- ARKA PLAN ---
        c.setFillColorRGB(0.97, 0.97, 0.97)
        c.rect(0, 0, genislik, yukseklik, fill=1, stroke=0)

        # --- HEADER BANDI ---
        c.setFillColorRGB(0.13, 0.17, 0.27)
        c.rect(0, yukseklik - 90, genislik, 90, fill=1, stroke=0)

        c.setFillColorRGB(1, 1, 1)
        c.setFont("DejaVu-Bold", 18)
        c.drawString(40, yukseklik - 45, "Ürün Yorumu Duygu Analizi")
        c.setFont("DejaVu", 11)
        c.drawString(40, yukseklik - 68, "Müşteri Memnuniyeti Raporu")

        # --- METRİK KARTLAR ---
        def metrik_kart(x, y, baslik, deger, r, g, b):
            c.setFillColorRGB(r, g, b)
            c.roundRect(x, y, 115, 65, 8, fill=1, stroke=0)
            c.setFillColorRGB(1, 1, 1)
            c.setFont("DejaVu-Bold", 22)
            c.drawCentredString(x + 57, y + 28, str(deger))
            c.setFont("DejaVu", 9)
            c.drawCentredString(x + 57, y + 13, baslik)

        metrik_kart(40,  yukseklik - 185, "Toplam Yorum", toplam, 0.2, 0.4, 0.8)
        metrik_kart(165, yukseklik - 185, "Olumlu", olumlu, 0.18, 0.7, 0.44)
        metrik_kart(290, yukseklik - 185, "Olumsuz", olumsuz, 0.9, 0.3, 0.3)
        metrik_kart(415, yukseklik - 185, "Memnuniyet", f"%{memnuniyet}", 0.5, 0.3, 0.8)

        # --- MEMNUNİYET PROGRESS BAR ---
        c.setFillColorRGB(0.13, 0.17, 0.27)
        c.setFont("DejaVu-Bold", 11)
        c.drawString(40, yukseklik - 215, "Genel Memnuniyet Skoru")

        bar_x, bar_y, bar_w, bar_h = 40, yukseklik - 235, 510, 14
        c.setFillColorRGB(0.85, 0.85, 0.85)
        c.roundRect(bar_x, bar_y, bar_w, bar_h, 5, fill=1, stroke=0)
        dolu = bar_w * (memnuniyet / 100)
        c.setFillColorRGB(0.18, 0.7, 0.44)
        c.roundRect(bar_x, bar_y, dolu, bar_h, 5, fill=1, stroke=0)

        c.setFillColorRGB(0.13, 0.17, 0.27)
        c.setFont("DejaVu-Bold", 9)
        c.drawString(bar_x + dolu + 5, bar_y + 3, f"%{memnuniyet}")

        # --- GRAFİKLERİ KAYDET VE PDF'E EKLE ---
        tmp_files = []

        # Duygu pasta grafiği
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches

        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        fig.patch.set_facecolor('#f7f7f7')

        duygu_sayilari = sonuc_df["duygu"].value_counts()
        renkler = ["#2ecc71" if d == "Olumlu" else "#e74c3c" for d in duygu_sayilari.index]
        axes[0].pie(duygu_sayilari.values, labels=duygu_sayilari.index,
                    colors=renkler, autopct='%1.1f%%', startangle=90,
                    textprops={'fontsize': 12})
        axes[0].set_title("Duygu Dagilimi", fontsize=13, fontweight='bold', pad=10)

        # Konu bar grafiği
        tum_konular = []
        for konular in sonuc_df["konular"]:
            tum_konular.extend(konular)
        from collections import Counter
        konu_sayilari = Counter(tum_konular)
        konular_list = list(konu_sayilari.keys())
        sayilar_list = list(konu_sayilari.values())
        bar_colors = ["#3498db", "#e67e22", "#9b59b6", "#1abc9c", "#95a5a6"]
        axes[1].bar(konular_list, sayilar_list, color=bar_colors[:len(konular_list)], edgecolor='white')
        axes[1].set_title("Konu Dagilimi", fontsize=13, fontweight='bold')
        axes[1].set_ylabel("Yorum Sayisi")
        axes[1].set_facecolor('#f7f7f7')

        plt.tight_layout()
        tmp1 = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(tmp1.name, dpi=150, bbox_inches='tight', facecolor='#f7f7f7')
        plt.close()
        tmp_files.append(tmp1.name)
        c.drawImage(tmp1.name, 30, yukseklik - 480, width=530, height=210)

        # --- TABLO BAŞLIĞI ---
        c.setFillColorRGB(0.13, 0.17, 0.27)
        c.rect(30, yukseklik - 510, 530, 22, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("DejaVu-Bold", 10)
        c.drawString(38, yukseklik - 502, "Yorum")
        c.drawString(355, yukseklik - 502, "Duygu")
        c.drawString(430, yukseklik - 502, "Konu")

        # --- TABLO SATIRLARI ---
        y = yukseklik - 528
        for i, (_, row) in enumerate(sonuc_df.iterrows()):
            if y < 40:
                c.showPage()
                c.setFillColorRGB(0.97, 0.97, 0.97)
                c.rect(0, 0, genislik, yukseklik, fill=1, stroke=0)
                y = yukseklik - 40

            # Satır arka planı
            if i % 2 == 0:
                c.setFillColorRGB(1, 1, 1)
            else:
                c.setFillColorRGB(0.93, 0.95, 0.98)
            c.rect(30, y - 5, 530, 17, fill=1, stroke=0)

            yorum_kisalt = str(row["yorum"])[:55] + "..." if len(str(row["yorum"])) > 55 else str(row["yorum"])
            konular = ", ".join(row["konular"]) if isinstance(row["konular"], list) else str(row["konular"])

            if row["duygu"] == "Olumlu":
                c.setFillColorRGB(0.18, 0.7, 0.44)
            else:
                c.setFillColorRGB(0.9, 0.3, 0.3)

            c.setFont("DejaVu-Bold", 8)
            c.drawString(355, y, row["duygu"])

            c.setFillColorRGB(0.13, 0.17, 0.27)
            c.setFont("DejaVu", 8)
            c.drawString(38, y, yorum_kisalt)
            c.drawString(430, y, konular[:22])
            y -= 17

        # --- FOOTER ---
        c.setFillColorRGB(0.13, 0.17, 0.27)
        c.rect(0, 0, genislik, 30, fill=1, stroke=0)
        c.setFillColorRGB(1, 1, 1)
        c.setFont("DejaVu", 8)
        c.drawString(40, 10, "Turkce Urun Yorumu Duygu Analizi Sistemi")
        c.drawRightString(genislik - 40, 10, "BERTurk ile uretilmistir.")

        c.save()
        buffer.seek(0)

        # Geçici dosyaları temizle
        for f in tmp_files:
            os.unlink(f)

        return buffer

    pdf_buffer = pdf_olustur(sonuc_df, memnuniyet, toplam, olumlu, olumsuz)

    st.download_button(
        label="📄 PDF Olarak İndir",
        data=pdf_buffer,
        file_name="analiz_raporu.pdf",
        mime="application/pdf"
    )