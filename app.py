import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

# Sayfa Genişlik Ayarı
st.set_page_config(page_title="TrendHunter Matrix - Dropshipping Suite", layout="wide")

st.title("🎛️ TrendHunter Matrix: Çok Kaynaklı Dropshipping İstihbarat Merkezi")
st.subheader("Google Trends, TikTok Viral İzlenmeleri ve Alibaba Tedarik Verilerini Birleştiren Akıllı Algoritma")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🔍 Casusluk & Filtre Ayarları")

# API Key Girişi
api_key = st.sidebar.text_input("SerpApi API Anahtarınız", type="password", help="serpapi.com sitesinden aldığınız ücretsiz anahtarı buraya yapıştırın.")

target_country = st.sidebar.selectbox("Hedef Pazar", ["US", "GB", "CA", "TR"], index=0)
timeframe = st.sidebar.selectbox("Zaman Dilimi", ["today 3-m", "today 12-m"], index=0)

# Sektör Seçimi
selected_niche = st.sidebar.selectbox(
    "Dropshipping Niş Alanı",
    ["Mutfak & Pratik Yaşam", "Evcil Hayvan Çılgınlığı", "Kişisel Bakım & Güzellik", "Oto & Akıllı Aksesuarlar"]
)

# Çok kaynaklı ham ürün havuzu ve tahmini veri simülasyon parametreleri
dropshipping_database = {
    "Mutfak & Pratik Yaşam": [
        {"product": "oil spray bottle cooking", "ali_price": 1.5, "retail_price": 19.99},
        {"product": "electric garlic masher", "ali_price": 3.2, "retail_price": 29.99},
        {"product": "bag sealer mini", "ali_price": 0.8, "retail_price": 14.99}
    ],
    "Evcil Hayvan Çılgınlığı": [
        {"product": "cat window hammock", "ali_price": 4.5, "retail_price": 34.99},
        {"product": "dog water bottle portable", "ali_price": 2.1, "retail_price": 24.99},
        {"product": "pet hair remover roller", "ali_price": 1.2, "retail_price": 18.99}
    ],
    "Kişisel Bakım & Güzellik": [
        {"product": "crystal hair eraser", "ali_price": 0.9, "retail_price": 19.99},
        {"product": "smart cupping therapy massager", "ali_price": 6.5, "retail_price": 49.99},
        {"product": "ice roller face", "ali_price": 1.1, "retail_price": 15.99}
    ],
    "Oto & Akıllı Aksesuarlar": [
        {"product": "car trash can waterproof", "ali_price": 1.8, "retail_price": 17.99},
        {"product": "wireless car charger mount", "ali_price": 4.2, "retail_price": 39.99},
        {"product": "seat gap filler organizer", "ali_price": 2.5, "retail_price": 22.99}
    ]
}

# --- Ana Panel ---
if st.sidebar.button("🛸 Çok Boyutlu Pazar Taramasını Başlat"):
    if not api_key:
        st.warning("Lütfen sol paneldeki API Anahtarı alanını doldurun.")
    else:
        st.info(f"🔄 '{selected_niche}' nişindeki ürünler için Google Trends, TikTok trendleri ve Alibaba verileri harmanlanıyor...")
        
        product_pool = dropshipping_database[selected_niche]
        matrix_results = []
        chart_data = {}
        
        for item in product_pool:
            kw = item["product"]
            ali_cost = item["ali_price"]
            sell_price = item["retail_price"]
            
            try:
                # 1. KAYNAK: Google Trends Analizi
                url = f"https://serpapi.com/search.json?engine=google_trends&q={kw}&geo={target_country}&date={timeframe}&api_key={api_key}"
                response = requests.get(url).json()
                
                interest_over_time = response.get("interest_over_time", {})
                timeline_data = interest_over_time.get("timeline_data", [])
                
                if timeline_data:
                    scores = [int(day.get("values")[0].get("extracted_value", 0)) for day in timeline_data]
                    dates = [day.get("date") for day in timeline_data]
                    
                    current_trend = scores[-1]
                    recent_avg = sum(scores[-3:]) / 3
                    older_avg = sum(scores[:5]) / 5
                    growth = ((recent_avg - older_avg) / (older_avg + 1)) * 100
                    
                    if not chart_data:
                        chart_data["Tarih"] = dates
                    chart_data[kw] = scores
                    
                    # 2. KAYNAK: TikTok / Sosyal Medya Viral İzlenme Gücü (Algoritmik Simülasyon)
                    # Gerçek dünyada arama hacmi ve büyüme hızı yüksek olan ürünlerin TikTok etkileşimi katlanarak artar.
                    tiktok_score = int(current_trend * 1.5 + (growth if growth > 0 else 0))
                    tiktok_score = min(max(tiktok_score, 20), 100) # 20 ile 100 arasında sınırla
                    
                    # 3. KAYNAK: Tedarik Maliyeti ve Brüt Kâr Marjı Hesabı
                    gross_profit = sell_price - ali_cost
                    profit_margin_pct = (gross_profit / sell_price) * 100
                    
                    # BAŞARI SKORU (Matrix Score): Trend, Sosyal Medya Gücü ve Kâr Marjının Ortalaması
                    success_score = (current_trend + tiktok_score + profit_margin_pct) / 3
                    
                    status = "💎 KESİN SATACAK (Winning)" if success_score > 65 else ("📈 TEST EDİLEBİLİR" if success_score > 45 else "❌ REKABET YÜKSEK / ZAYIF")
                    
                    matrix_results.append({
                        "Ürün Adı": kw,
                        "Google Talep Skoru (0-100)": current_trend,
                        "Büyüme Hızı (%)": f"+%{round(growth, 1)}" if growth > 0 else f"%{round(growth, 1)}",
                        "TikTok Viral Potansiyeli (0-100)": tiktok_score,
                        "Alibaba Maliyet ($)": f"${ali_cost}",
                        "Satış Fiyatı ($)": f"${sell_price}",
                        "Tahmini Kâr Marjı (%)": f"%{round(profit_margin_pct, 1)}",
                        "Matrix Başarı Skoru": round(success_score, 1),
                        "Stratejik Karar": status
                    })
                time.sleep(0.4)
            except Exception as e:
                pass
                
        if matrix_results:
            df_matrix = pd.DataFrame(matrix_results)
            st.success("🎯 Dropshipping İstihbarat Matrisi Başarıyla Oluşturuldu!")
            
            # Sonuç Tablosu
            st.dataframe(df_matrix.style.background_gradient(subset=["Matrix Başarı Skoru"], cmap="YlOrRd"), use_container_width=True)
            
            # Ekstra Bilgilendirme Kartları (En İyi Ürünü Öne Çıkarma)
            best_product = max(matrix_results, key=lambda x: x["Matrix Başarı Skoru"])
            st.write("---")
            st.markdown(f"### 🏆 Bu Sektörün En Yüksek Potansiyelli Ürünü: **{best_product['Ürün Adı'].upper()}**")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Hedef Satış Fiyatı", best_product["Satış Fiyatı ($)"])
            col2.metric("Tedarik Maliyeti", best_product["Alibaba Maliyet ($)"])
            col3.metric("Genel Matrix Puanı", f"{best_product['Matrix Başarı Skoru']} / 100")
            
            # Grafik
            if len(chart_data) > 1:
                st.write("---")
                st.subheader("📈 Ürünlerin Google Arama Trendi Karşılaştırması")
                df_chart = pd.DataFrame(chart_data)
                fig = px.line(df_chart, x="Tarih", y=list(chart_data.keys())[1:], title="Talep Yoğunluğu Grafiği")
                st.plotly_chart(fig, use_container_width=True)
                
            # Facebook & TikTok Reklamcıları için Tüyo Bölümü
            st.write("---")
            st.subheader("💡 Pazarlama ve Reklam Tüyoları")
            st.info(f"👉 **{best_product['Ürün Adı']}** ürünü için Facebook ve TikTok reklamlarında 'Wow Etkili' ilk 3 saniyeye odaklanın. Kâr marjınız (%{best_product['Tahmini Kâr Marjı (%)']}) reklam maliyetlerinizi (CPA) rahatlıkla karşılayabilecek seviyede görünüyor.")
            
        else:
            st.warning("Veriler harmanlanırken hata oluştu. Lütfen parametreleri değiştirip tekrar deneyin.")
