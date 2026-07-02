import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
import plotly.express as px
import time

# Sayfa Genişlik Ayarı
st.set_page_config(page_title="TrendHunter - E-Ticaret Ürün Bulucu", layout="wide")

# Google Trends Bağlantısı
@st.cache_resource
def get_pytrends():
    return TrendReq(hl='en-US', tz=360, retries=5, backoff_factor=1)

pytrends = get_pytrends()

st.title("🚀 TrendHunter: Yüksek Potansiyelli Ürün Bulucu")
st.subheader("Google Trends verilerini analiz ederek e-ticarette yükselen nişleri keşfedin.")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🔍 Analiz Filtreleri")
target_country = st.sidebar.selectbox("Hedef Ülke", ["US", "GB", "CA", "TR"], index=0)
timeframe = st.sidebar.selectbox("Zaman Aralığı", ["today 3-m", "today 12-m", "now 7-d"], index=0)

# Örnek araştırmak istenen e-ticaret kategorileri/anahtar kelimeleri
seed_keywords = st.sidebar.text_area(
    "Analiz Edilecek Anahtar Kelimeler (Her satıra bir tane)",
    "portable blender\nled lights\nneck massager\npet grooming\nsmart mug"
).split("\n")

# --- Ana Panel ---
if st.sidebar.button("Trendleri Analiz Et"):
    keywords = [kw.strip() for kw in seed_keywords if kw.strip()]
    
    if not keywords:
        st.warning("Lütfen en az bir anahtar kelime girin.")
    else:
        st.info("Google Trends verileri çekiliyor ve analiz ediliyor... Lütfen bekleyin.")
        
        results = []
        
        for kw in keywords:
            try:
                time.sleep(2) # Google engeline takılmamak için bekleme süresi
                
                pytrends.build_payload([kw], cat=0, timeframe=timeframe, geo=target_country, gprop='')
                interest_df = pytrends.interest_over_time()
                
                if not interest_df.empty and kw in interest_df:
                    recent_score = interest_df[kw].iloc[-3:].mean()
                    older_score = interest_df[kw].iloc[:5].mean()
                    
                    growth = ((recent_score - older_score) / (older_score + 1)) * 100
                    current_trend_value = interest_df[kw].iloc[-1]
                    
                    related_queries = pytrends.related_queries()
                    breakout_queries = []
                    
                    if kw in related_queries and related_queries[kw]['rising'] is not None:
                        rising_df = related_queries[kw]['rising']
                        breakout_df = rising_df[rising_df['value'] == 'Breakout']
                        if not breakout_df.empty:
                            breakout_queries = breakout_df['query'].tolist()[:3]
                    
                    results.append({
                        "Ürün / Kelime": kw,
                        "Mevcut Trend Skoru (0-100)": int(current_trend_value),
                        "Tahmini Büyüme Oranı (%)": round(growth, 2),
                        "Breakout Alt Başlıklar": ", ".join(breakout_queries) if breakout_queries else "Yok"
                    })
            except Exception as e:
                st.error(f"'{kw}' analiz edilirken limit aşımı veya hata oluştu. Biraz bekleyip tekrar deneyin.")
        
        if results:
            df_results = pd.DataFrame(results)
            
            df_results['Potansiyel Durumu'] = df_results.apply(
                lambda row: "🔥 ÇOK YÜKSEK (Winning)" if row['Tahmini Büyüme Oranı (%)'] > 50 and row['Mevcut Trend Skoru (0-100)'] > 60
                else ("📈 YÜKSELEN" if row['Tahmini Büyüme Oranı (%)'] > 10 else "📉 DURAĞAN/DÜŞÜŞTE"), axis=1
            )
            
            st.success("Analiz Tamamlandı!")
            st.dataframe(df_results)
            
            st.write("---")
            st.subheader("📊 Zaman İçindeki Değişim Grafiği")
            
            all_trends = []
            for kw in keywords:
                try:
                    pytrends.build_payload([kw], timeframe=timeframe, geo=target_country)
                    indf = pytrends.interest_over_time()
                    if not indf.empty and kw in indf:
                        all_trends.append(indf[kw])
                except:
                    pass
            
            if all_trends:
                chart_df = pd.concat(all_trends, axis=1)
                fig = px.line(chart_df, x=chart_df.index, y=chart_df.columns, title="Ürünlerin Popülerlik Trendi")
                st.plotly_chart(fig, use_container_width=True)
