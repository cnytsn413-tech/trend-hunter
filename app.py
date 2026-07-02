import streamlit as st
import pandas as pd
import time

# Sayfa Ayarları
st.set_page_config(page_title="WinningHunter Clone - E-Com Spy Tool", layout="wide", initial_sidebar_state="expanded")

st.title("🎯 WinningHunter Pro: Viral Dropshipping Spy Tool")
st.subheader("Sosyal Medyada Gizlice Büyüyen ve Satış Rekorları Kıran Reklamları Yakalayın")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🛡️ Casusluk Filtreleri")
platform = st.sidebar.selectbox("Reklam Platformu", ["TikTok Ads", "Meta (Facebook/IG) Ads", "Pinterest Ads"])

# YENİ EKLEYECEĞİMİZ ÜLKE FİLTRESİ
target_country = st.sidebar.selectbox("Hedef Ülke (Pazar)", ["US (Amerika)", "GB (İngiltere)", "CA (Kanada)", "TR (Türkiye)"])

ad_creation_date = st.sidebar.selectbox("Reklam Yayınlanma Tarihi", ["Son 7 Gün", "Son 30 Gün", "Son 90 Gün"])
daily_spend = st.sidebar.slider("Tahmini Günlük Reklam Bütçesi ($)", 50, 5000, (100, 1500))
sort_by = st.sidebar.selectbox("Sıralama Kriteri", ["En Yüksek Etkileşim (Engagement)", "En Yeni Reklamlar", "Viral Artış Hızı"])

# --- Ülkeye Göre Dinamik Değişen Reklam Veritabanı ---
spy_database = {
    "US (Amerika)": [
        {"title": "Anti-Gravity Levitating Humidifier", "niche": "Ev & Dekorasyon", "views": "4.2M", "likes": "310K", "days_running": 14, "cpa": "$8.50", "margin": "%75", "store_url": "https://mysticshophome.com", "ad_link": "https://tiktok.com/ads/library", "type": "🔥 WINNING PRODUCT (US)"},
        {"title": "Smart Cupping Therapy Massager", "niche": "Sağlık & Kişisel Bakım", "views": "6.7M", "likes": "520K", "days_running": 28, "cpa": "$12.00", "margin": "%80", "store_url": "https://recoverysmart.com", "ad_link": "https://tiktok.com/ads/library", "type": "🔥 WINNING PRODUCT (US)"},
        {"title": "Crystal Hair Eraser Exfoliator", "niche": "Güzellik & Kozmetik", "views": "12.4M", "likes": "980K", "days_running": 45, "cpa": "$4.50", "margin": "%85", "store_url": "https://silky-skin-co.com", "ad_link": "https://tiktok.com/ads/library", "type": "🔥 EVERGREEN PRODUCT"}
    ],
    "GB (İngiltere)": [
        {"title": "Wireless Cat Water Fountain", "niche": "Evcil Hayvan", "views": "1.8M", "likes": "145K", "days_running": 8, "cpa": "$5.20", "margin": "%68", "store_url": "https://happy-paws-co.myshopify.com", "ad_link": "https://facebook.com/ads/library", "type": "📈 VIRAL RISING (UK)"},
        {"title": "Electric Garlic & Vegetable Chopper", "niche": "Mutfak Pratik", "views": "950K", "likes": "68K", "days_running": 5, "cpa": "$3.10", "margin": "%60", "store_url": "https://chefkitchentools.com", "ad_link": "https://facebook.com/ads/library", "type": "📈 VIRAL RISING (UK)"}
    ],
    "CA (Kanada)": [
        {"title": "Anti-Gravity Levitating Humidifier", "niche": "Ev & Dekorasyon", "views": "1.1M", "likes": "95K", "days_running": 10, "cpa": "$9.00", "margin": "%75", "store_url": "https://mysticshophome.com", "ad_link": "https://tiktok.com/ads/library", "type": "📈 TEST PHASE (CA)"},
        {"title": "Crystal Hair Eraser Exfoliator", "niche": "Güzellik & Kozmetik", "views": "3.2M", "likes": "240K", "days_running": 20, "cpa": "$4.80", "margin": "%85", "store_url": "https://silky-skin-co.com", "ad_link": "https://tiktok.com/ads/library", "type": "🔥 WINNING PRODUCT (CA)"}
    ],
    "TR (Türkiye)": [
        {"title": "Pratik Şarjlı Sebze Doğrayıcı", "niche": "Mutfak Pratik", "views": "620K", "likes": "45K", "days_running": 7, "cpa": "$2.50", "margin": "%65", "store_url": "https://chefkitchentools.com", "ad_link": "https://facebook.com/ads/library", "type": "🔥 POPÜLER (TR)"},
        {"title": "Kablosuz Kedi Su Pınarı", "niche": "Evcil Hayvan", "views": "410K", "likes": "32K", "days_running": 4, "cpa": "$4.00", "margin": "%60", "store_url": "https://happy-paws-co.myshopify.com", "ad_link": "https://facebook.com/ads/library", "type": "📈 YÜKSELEN TREND (TR)"}
    ]
}

# --- Ana Ekran Aksiyonu ---
if st.sidebar.button("🕵️‍♂️ Canlı Reklam Ağını Taramaya Başla"):
    st.info(f"🤖 Yapay zeka botları {target_country} pazarındaki reklam kütüphanelerine sızıyor...")
    
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.005)
        progress_bar.progress(percent_complete + 1)
        
    # Seçilen ülkenin verisini çekiyoruz
    selected_ads = spy_database.get(target_country, [])
    
    st.success(f"⚡ Tarama Tamamlandı! {target_country} pazarında {platform} üzerinde dönen {len(selected_ads)} ürün listelendi.")
    st.write("---")
    
    # Seçilen ülkenin kartlarını ekrana basıyoruz
    for item in selected_ads:
        with st.container(border=True):
            col_title, col_badge = st.columns([3, 1])
            with col_title:
                st.subheader(item['title'])
                st.caption(f"Kategori: {item['niche']} | Reklam Süresi: {item['days_running']} Gün")
            with col_badge:
                st.warning(item['type'])
            
            # Metrikleri Göster
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("İzlenme", item['views'])
            m2.metric("Beğeni", item['likes'])
            m3.metric("Tahmini CPA", item['cpa'])
            m4.metric("Brüt Kâr Marjı", item['margin'])
            
            # Butonlar
            btn_col1, btn_col2, _ = st.columns([1, 1, 2])
            with btn_col1:
                st.link_button("🏪 Rakip Mağazayı İncele", item['store_url'], use_container_width=True)
            with btn_col2:
                st.link_button("🎥 Reklam Videosunu Gör", item['ad_link'], use_container_width=True)
            
            st.write("") 

else:
    st.write("### 👈 Casusluk yapmaya başlamak için pazar ülkesini seçin ve butona basın.")
    st.markdown("""
    **Pazar Seçim Tüyosu:**
    * **US (Amerika):** Dropshipping trendlerinin doğduğu yerdir. Rekabet yüksek ama hacim devasadır.
    * **TR (Türkiye):** Genellikle Amerika pazarında 3-4 ay önce popüler olmuş ürünlerin yerel pazara uyarlanarak viral yapılabileceği harika bir fırsat alanıdır.
    """)
