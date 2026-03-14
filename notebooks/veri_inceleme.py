from datasets import load_dataset
import pandas as pd

dataset = load_dataset("winvoker/turkish-sentiment-analysis-dataset")

df = pd.DataFrame(dataset["train"])

# Sadece ürün yorumları ve Positive/Negative
df = df[df["dataset"] == "urun_yorumlari"]
df = df[df["label"] != "Notr"]

# Dengeleme: her kategoriden 13.374 örnek alalım
positive = df[df["label"] == "Positive"].sample(13374, random_state=42)
negative = df[df["label"] == "Negative"].sample(13374, random_state=42)

# Birleştir ve karıştır
df_balanced = pd.concat([positive, negative]).sample(frac=1, random_state=42).reset_index(drop=True)

# Sadece text ve label sütunlarını tutalım
df_balanced = df_balanced[["text", "label"]]

# Label'ları sayıya çevirelim (model sayı anlar)
# Positive → 1, Negative → 0
df_balanced["label"] = df_balanced["label"].map({"Positive": 1, "Negative": 0})

# data klasörüne kaydedelim
df_balanced.to_csv("data/yorumlar.csv", index=False)

print(f"Toplam: {len(df_balanced)} yorum kaydedildi.")
print(df_balanced["label"].value_counts())
print("---")
print("İlk 3 örnek:")
print(df_balanced.head(3))