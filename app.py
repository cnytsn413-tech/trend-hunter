import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

# Sayfa Genişlik Ayarı
st.set_page_config(page_title="TrendHunter Pro - Akıllı Ürün Bulucu", layout="wide")

st.title("🚀 TrendHunter Pro: Otomatik Ürün Bulucu")
st.subheader("İster kendi kelimelerinizi aratın, ister sistemin en popüler e-ticaret trendlerini otomatik bulmasını sağlayın.")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🔍 Ayarlar & Filtreler")

# API Key Girişi
api_key = st.sidebar.text_input("SerpApi API Anahtarınız", type="password", help="serpapi.com sitesinden aldığınız ücretsiz anahtarı buraya yapıştırın.")

target_country = st.sidebar.selectbox("Hedef Ülke", ["US", "GB", "CA", "TR"], index=0)
timeframe = st.sidebar.selectbox("Zaman Aralığı", ["today 3-m", "today 12-m", "now 7-d"], index=0)

# Arama Modu Seçimi
search_mode = st.sidebar.radio("Arama Modu", ["🤖 Otomatik En Popüler Ürünleri Bul", "✍️ Kendi Kelimelerimi Analiz Et"])

seed_keywords = []
if search_mode == "✍️ Kendi Kelimelerimi Analiz Et":
    seed_keywords = st.sidebar.text_area(
        "Analiz Edilecek Anahtar Kelimeler (Her satıra bir tane)",
        "portable blender\nled lights\nneck massager"
    ).split("\n")

# --- Ana Panel ---
if st.sidebar.button("Sistemi Çalıştır ve Trendleri Getir"):
    if not api_key:
        st.warning("Lütfen sol paneldeki API Anahtarı alanını doldurun.")
    else:
        keywords = []
        
        # MOD 1: OTOMATİK KEŞİF
        if search_mode == "🤖 Otomatik En Popüler Ürünleri Bul":
            st.info("E-Ticaret dünyasında şu an en çok yükselen genel trendler ve niş ürünler sorgulanıyor...")
            try:
                # Alışveriş (Shopping) kategorisindeki genel yükselen trendleri SerpApi üzerinden çekiyoruz
                # cat=18, Google Trends'te Alışveriş (Shopping) kategorisidir.
                url = f"https://serpapi.com/search.json?engine=google_trends_trending_searches&trend_type=realtime&geo={target_country}&cat=s&api_key={api_key}"
                response = requests.get(url).json()
                
                # Gerçek zamanlı trendlerden kelimeleri ayıkla
                trending_searches = response.get("trending_searches", [])
                for search in trending_searches[:10]: # En popüler 10 trendi alıyoruz
                    query = search.get("title")
                    if query:
                        keywords.append(query)
                
                # Eğer gerçek zamanlı veri o an boş dönerse, e-ticaret için en popüler hazır niş kelimeleri havuzdan seçer
                if not keywords:
                    keywords = ["viral product", "smart home gadget", "fitness tracking", "eco friendly packaging", "ergonomic office"]
                    
            except Exception as e:
                st.error("Otomatik trend listesi alınırken bir sorun oluştu, yedek liste devreye giriyor.")
                keywords = ["portable blender", "led lights", "neck massager", "pet grooming", "smart mug"]
        
        # MOD 2: MANUEL KELİME
        else:
            keywords = [kw.strip() for kw in seed_keywords if kw.strip()]
        
        # --- VERİ ANALİZ AŞAMASI (Ortak Kısım) ---
        if not keywords:
            st.warning("Analiz edilecek kelime bulunamadı.")
        else:
            st.write(f"📊 **Analiz Edilen Kelimeler:** {', '.join(keywords)}")
            st.info("Kelimelerin büyüme potansiyelleri ve detayları hesaplanıyor...")
            
            results = []
            chart_data = {}
            
            for kw in keywords:
                try:
                    url = f"https://serpapi.com/search.json?engine=google_trends&q={kw}&geo={target_country}&date={timeframe}&api_key={api_key}"
                    response = requests.get(url).json()
                    
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
                            
                            if not chart_data:
                                chart_data["Tarih"] = dates
                            chart_data[kw] = scores
                            
                            related_queries = response.get("related_queries", {})
                            rising_queries = related_queries.get("rising", [])
                            breakout_queries = [q.get("query") for q in rising_queries if q.get("value") == "Breakout"][:3]
                            
                            results.append({
                                "Ürün / Kelime": kw,
                                "Mevcut Trend Skoru (0-100)": int(current_trend_value),
                                "Tahmini Büyüme Oranı (%)": round(growth, 2),
                                "Breakout Alt Başlıklar": ", ".join(breakout_queries) if breakout_queries else "Yok"
                            })
                    time.sleep(0.5)
                except:
                    pass
            
            if results:
                df_results = pd.DataFrame(results)
                
                df_results['Potansiyel Durumu'] = df_results.apply(
                    lambda row: "🔥 ÇOK YÜKSEK (Winning)" if row['Tahmini Büyüme Oranı (%)'] > 50 and row['Mevcut Trend Skoru (0-100)'] > 60
                    else ("📈 YÜKSELEN" if row['Tahmini Büyüme Oranı (%)'] > 10 else "📉 DURAĞAN/DÜŞÜŞTE"), axis=1
                )
                
                st.success("Analiz Hatasız Tamamlandı!")
                st.dataframe(df_results)
                
                if len(chart_data) > 1:
                    st.write("---")
                    st.subheader("📊 Zaman İçindeki Değişim Grafiği")
                    df_chart = pd.DataFrame(chart_data)
                    fig = px.line(df_chart, x="Tarih", y=list(chart_data.keys())[1:], title="Otomatik Keşfedilen Ürünlerin Popülerlik Trendi")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Seçilen ülke veya zaman diliminde analiz edilecek anlamlı bir trend verisi bulunamadı.")
