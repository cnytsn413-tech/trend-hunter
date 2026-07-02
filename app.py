import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

# Sayfa Genişlik Ayarı
st.set_page_config(page_title="TrendHunter - E-Ticaret Ürün Bulucu", layout="wide")

st.title("🚀 TrendHunter: Yüksek Potansiyelli Ürün Bulucu")
st.subheader("SerpApi ile Kesintisiz Google Trends Analizi")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🔍 Ayarlar & Filtreler")

# API Key Girişi
api_key = st.sidebar.text_input("SerpApi API Anahtarınız", type="password", help="serpapi.com sitesinden aldığınız ücretsiz anahtarı buraya yapıştırın.")

target_country = st.sidebar.selectbox("Hedef Ülke", ["US", "GB", "CA", "TR"], index=0)
timeframe = st.sidebar.selectbox("Zaman Aralığı", ["today 3-m", "today 12-m", "now 7-d"], index=0)

seed_keywords = st.sidebar.text_area(
    "Analiz Edilecek Anahtar Kelimeler (Her satıra bir tane)",
    "portable blender\nled lights\nneck massager\npet grooming\nsmart mug"
).split("\n")

# --- Ana Panel ---
if st.sidebar.button("Trendleri Analiz Et"):
    keywords = [kw.strip() for kw in seed_keywords if kw.strip()]
    
    if not api_key:
        st.warning("Lütfen sol paneldeki API Anahtarı alanını doldurun.")
    elif not keywords:
        st.warning("Lütfen en az bir anahtar kelime girin.")
    else:
        st.info("Korumalı hat üzerinden Google verileri çekiliyor... Lütfen bekleyin.")
        
        results = []
        chart_data = {}
        
        for kw in keywords:
            try:
                # SerpApi Google Trends Entegrasyonu
                url = f"https://serpapi.com/search.json?engine=google_trends&q={kw}&geo={target_country}&date={timeframe}&api_key={api_key}"
                response = requests.get(url).json()
                
                # Zaman içindeki ilgi verisini işle
                interest_over_time = response.get("interest_over_time", {})
                timeline_data = interest_over_time.get("timeline_data", [])
                
                if timeline_data:
                    scores = [int(day.get("values")[0].get("extracted_value", 0)) for day in timeline_data]
                    dates = [day.get("date") for day in timeline_data]
                    
                    if len(scores) >= 5:
                        recent_score = sum(scores[-3:]) / 3
                        older_score = sum(scores[:5]) / 5
                        growth = ((recent_score - older_score) / (older_score + 1)) * 100
                        current_trend_value = scores[-1]
                        
                        # Grafikte göstermek için veriyi sakla
                        if not chart_data:
                            chart_data["Tarih"] = dates
                        chart_data[kw] = scores
                        
                        # Yükselen ilgili aramalar (Breakout yakalama)
                        related_queries = response.get("related_queries", {})
                        rising_queries = related_queries.get("rising", [])
                        breakout_queries = [q.get("query") for q in rising_queries if q.get("value") == "Breakout"][:3]
                        
                        results.append({
                            "Ürün / Kelime": kw,
                            "Mevcut Trend Skoru (0-100)": int(current_trend_value),
                            "Tahmini Büyüme Oranı (%)": round(growth, 2),
                            "Breakout Alt Başlıklar": ", ".join(breakout_queries) if breakout_queries else "Yok"
                        })
                time.sleep(0.5) # Güvenlik amaçlı kısa bekleme
                
            except Exception as e:
                st.error(f"'{kw}' analiz edilirken bir sorun oluştu.")
        
        if results:
            df_results = pd.DataFrame(results)
            
            df_results['Potansiyel Durumu'] = df_results.apply(
                lambda row: "🔥 ÇOK YÜKSEK (Winning)" if row['Tahmini Büyüme Oranı (%)'] > 50 and row['Mevcut Trend Skoru (0-100)'] > 60
                else ("📈 YÜKSELEN" if row['Tahmini Büyüme Oranı (%)'] > 10 else "📉 DURAĞAN/DÜŞÜŞTE"), axis=1
            )
            
            st.success("Analiz Hatasız Tamamlandı!")
            st.dataframe(df_results)
            
            # --- Grafik Çizimi ---
            if len(chart_data) > 1:
                st.write("---")
                st.subheader("📊 Zaman İçindeki Değişim Grafiği")
                df_chart = pd.DataFrame(chart_data)
                fig = px.line(df_chart, x="Tarih", y=list(chart_data.keys())[1:], title="Ürünlerin Popülerlik Trendi")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Veri bulunamadı. Anahtar kelimeleri veya ülke ayarını kontrol edin.")
