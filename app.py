import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time
import random

# Sayfa Genişlik Ayarı
st.set_page_config(page_title="TrendHunter Pro - Mikro Niş Ürün Bulucu", layout="wide")

st.title("🚀 TrendHunter Pro: Yapay Zeka Destekli Mikro-Niş Ürün Bulucu")
st.subheader("Herkesin bildiği jenerik ürünleri değil, gizli kalmış derin e-ticaret nişlerini keşfedin.")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🔍 Ayarlar & Filtreler")

# API Key Girişi
api_key = st.sidebar.text_input("SerpApi API Anahtarınız", type="password", help="serpapi.com sitesinden aldığınız ücretsiz anahtarı buraya yapıştırın.")

target_country = st.sidebar.selectbox("Hedef Ülke", ["US", "GB", "CA", "TR"], index=0)
timeframe = st.sidebar.selectbox("Zaman Aralığı", ["today 3-m", "today 12-m", "now 7-d"], index=0)

# Niş Kategorileri
ecommerce_category = st.sidebar.selectbox(
    "Odaklanmak İstediğiniz Sektör",
    ["Ev & Yaşam Gadgetları", "Mutfak / Pratik Yaşam", "Evcil Hayvan Ürünleri", "Kişisel Bakım & Sağlık", "Araba / Araç Aksesuarları"]
)

# Arka planda jenerik kelimeleri derin nişlere dönüştüren havuz
nich_pool = {
    "Ev & Yaşam Gadgetları": [
        "sunset lamp bluetooth", "anti gravity humidifier", "motion sensor under cabinet lights", 
        "crystal hair eraser", "levitating moon lamp", "flame air diffuser"
    ],
    "Mutfak / Pratik Yaşam": [
        "electric garlic masher", "oil spray bottle cooking", "automatic jar opener", 
        "bag sealer mini", "cereal dispenser wall mounted", "rapid egg cooker"
    ],
    "Evcil Hayvan Ürünleri": [
        "dog water bottle portable", "cat water fountain wireless", "pet hair remover roller", 
        "self cleaning grooming brush", "dog seat cover car", "cat window hammock"
    ],
    "Kişisel Bakım & Sağlık": [
        "neck stretcher chronic pain", "electric scalp massager", "posture corrector adjustable", 
        "ice roller face", "smart cupping therapy massager", "teeth whitening kit led"
    ],
    "Araba / Araç Aksesuarları": [
        "car trash can waterproof", "wireless car charger mount", "car dent repair puller", 
        "seat gap filler organizer", "hud display car speed", "car windshield sun shade umbrella"
    ]
}

# --- Ana Panel ---
if st.sidebar.button("🔥 Mikro-Niş Ürünleri Tıkla ve Analiz Et"):
    if not api_key:
        st.warning("Lütfen sol paneldeki API Anahtarı alanını doldurun.")
    else:
        st.info(f"🔮 '{ecommerce_category}' sektörüne ait derin pazar verileri ve alt nişler analiz ediliyor...")
        
        # Seçilen kategoriden derin ürün fikirlerini çekiyoruz
        base_keywords = nich_pool[ecommerce_category]
        keywords = []
        
        # Her bir derin niş kelimenin Google Trends'teki yükselen alışveriş alt kelimelerini (Breakout) topluyoruz
        for base_kw in base_keywords:
            try:
                url = f"https://serpapi.com/search.json?engine=google_trends&q={base_kw}&geo={target_country}&date={timeframe}&api_key={api_key}"
                response = requests.get(url).json()
                
                related_queries = response.get("related_queries", {})
                rising_queries = related_queries.get("rising", [])
                
                # Eğer o niş kelimede o an patlayan (Breakout) veya %300+ büyüyen çok spesifik alt sorgular varsa onları yakala
                found_sub_niche = False
                for q in rising_queries:
                    val = str(q.get("value", ""))
                    if "Breakout" in val or (val.replace('%','').replace('+','').isdigit() and int(val.replace('%','').replace('+','')) > 300):
                        keywords.append(q.get("query"))
                        found_sub_niche = True
                
                # Eğer spesifik alt arama o anlık yoksa ana niş kelimeyi listeye dahil et
                if not found_sub_niche:
                    keywords.append(base_kw)
                    
                time.sleep(0.3)
            except:
                keywords.append(base_kw)
        
        # Benzersiz olanları filtrele ve ilk 6-7 tanesini derin analize al
        keywords = list(set(keywords))[:7]
        
        # --- VERİ ANALİZ AŞAMASI ---
        st.write(f"🎯 **Sizin için Keşfedilen Mikro-Niş Ürünler:** {', '.join([f'`{k}`' for k in keywords])}")
        
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
                        
                        # TikTok veya Facebook reklamlarında aranabilecek hedef etiket önerisi
                        results.append({
                            "Spesifik Ürün / Niş": kw,
                            "Anlık Talep Gücü (0-100)": int(current_trend_value),
                            "Son Dönem Büyüme Hızı (%)": f"+%{round(growth, 1)}" if growth > 0 else f"%{round(growth, 1)}",
                            "E-Ticaret Potansiyeli": "🔥 KAZANAN (Winning Product)" if growth > 40 and current_trend_value > 50 
                                                     else ("📈 YÜKSELEN TREND" if growth > 10 else "🔍 SABİT PAZAR")
                        })
                time.sleep(0.4)
            except:
                pass
        
        if results:
            df_results = pd.DataFrame(results)
            st.success("Derinlemesine Mikro-Niş Analizi Tamamlandı!")
            st.dataframe(df_results, use_container_width=True)
            
            if len(chart_data) > 1:
                st.write("---")
                st.subheader("📊 Niş Ürünlerin Talep Karşılaştırma Grafiği")
                df_chart = pd.DataFrame(chart_data)
                fig = px.line(df_chart, x="Tarih", y=list(chart_data.keys())[1:], title="Mikro-Nişlerin Güncel Rekabet ve Talep Trendi")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Veriler işlenirken bir kısıtlama oluştu. Lütfen birkaç saniye sonra tekrar deneyin.")
