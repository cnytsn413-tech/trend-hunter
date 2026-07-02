import streamlit as st
import pandas as pd
import time
import random

# Sayfa Ayarları
st.set_page_config(page_title="WinningHunter Clone - E-Com Spy Tool", layout="wide", initial_sidebar_state="expanded")

# --- Stil ve Tema Ayarları (Koyu Şık Arayüz) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #ff3333; color: white; }
    .card { background-color: #1e222b; padding: 20px; border-radius: 10px; border: 1px solid #2d3139; margin-bottom: 15px; }
    .winning-badge { background-color: #28a745; color: white; padding: 3px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; }
    .viral-badge { background-color: #fd7e14; color: white; padding: 3px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; }
    </style>
""", unsafe_allow_unsafe_html=True)

st.title("🎯 WinningHunter Pro: Viral Dropshipping Spy Tool")
st.subheader("Sosyal Medyada Gizlice Büyüyen ve Satış Rekorları Kıran Reklamları Yakalayın")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🛡️ Casusluk Filtreleri")
platform = st.sidebar.selectbox("Reklam Platformu", ["TikTok Ads", "Meta (Facebook/IG) Ads", "Pinterest Ads"])
ad_creation_date = st.sidebar.selectbox("Reklam Yayınlanma Tarihi", ["Son 7 Gün", "Son 30 Gün", "Son 90 Gün"])
daily_spend = st.sidebar.slider("Tahmini Günlük Reklam Bütçesi ($)", 50, 5000, (100, 1500))
sort_by = st.sidebar.selectbox("Sıralama Kriteri", ["En Yüksek Etkileşim (Engagement)", "En Yeni Reklamlar", "Viral Artış Hızı"])

# --- Arka Plan Casusluk Veritabanı (WinningHunter Mantığı) ---
spy_database = [
    {
        "title": "Anti-Gravity Levitating Humidifier",
        "niche": "Ev & Dekorasyon",
        "views": "4.2M",
        "likes": "310K",
        "days_running": 14,
        "cpa": "$8.50",
        "margin": "%75",
        "store_url": "https://mysticshophome.com",
        "ad_link": "https://tiktok.com/ads/library",
        "type": "🔥 WINNING PRODUCT"
    },
    {
        "title": "Wireless Cat Water Fountain",
        "niche": "Evcil Hayvan",
        "views": "1.8M",
        "likes": "145K",
        "days_running": 8,
        "cpa": "$5.20",
        "margin": "%68",
        "store_url": "https://happy-paws-co.myshopify.com",
        "ad_link": "https://facebook.com/ads/library",
        "type": "📈 VIRAL RISING"
    },
    {
        "title": "Smart Cupping Therapy Massager",
        "niche": "Sağlık & Kişisel Bakım",
        "views": "6.7M",
        "likes": "520K",
        "days_running": 28,
        "cpa": "$12.00",
        "margin": "%80",
        "store_url": "https://recoverysmart.com",
        "ad_link": "https://tiktok.com/ads/library",
        "type": "🔥 WINNING PRODUCT"
    },
    {
        "title": "Electric Garlic & Vegetable Chopper",
        "niche": "Mutfak Pratik",
        "views": "950K",
        "likes": "68K",
        "days_running": 5,
        "cpa": "$3.10",
        "margin": "%60",
        "store_url": "https://chefkitchentools.com",
        "ad_link": "https://facebook.com/ads/library",
        "type": "📈 VIRAL RISING"
    },
    {
        "title": "Crystal Hair Eraser Exfoliator",
        "niche": "Güzellik & Kozmetik",
        "views": "12.4M",
        "likes": "980K",
        "days_running": 45,
        "cpa": "$4.50",
        "margin": "%85",
        "store_url": "https://silky-skin-co.com",
        "ad_link": "https://tiktok.com/ads/library",
        "type": "🔥 SÜREKLİ SATAN (Evergreen)"
    }
]

# --- Ana Ekran Aksiyonu ---
if st.sidebar.button("🕵️‍♂️ Canlı Reklam Ağını Taramaya Başla"):
    st.info("🤖 Yapay zeka botları sosyal medya reklam kütüphanelerine sızıyor... Filtrelere uygun 'Winning' ürünler ayıklanıyor.")
    
    # Gerçekçi bir yükleme efekti
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.01)
        progress_bar.progress(percent_complete + 1)
        
    st.success(f"⚡ Tarama Tamamlandı! {platform} üzerinde patlayan {len(spy_database)} adet potansiyel ürün listelendi.")
    st.write("---")
    
    # Kart Tasarımlarının Ekrana Basılması
    for item in spy_database:
        # Rozet rengini belirleme
        badge = f"<span class='winning-badge'>{item['type']}</span>" if "WINNING" in item['type'] else f"<span class='viral-badge'>{item['type']}</span>"
        
        st.markdown(f"""
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: #ff4b4b;">{item['title']}</h3>
                {badge}
            </div>
            <p style="color: #888888; font-size: 14px; margin-top: 5px;">Kategori: <b>{item['niche']}</b> | Reklam Süresi: <b>{item['days_running']} Gün</b></p>
            <hr style="border: 0.5px solid #2d3139; margin: 10px 0;">
            <div style="display: flex; justify-content: space-between; text-align: center;">
                <div>
                    <h5 style="margin:0; color:#4caf50;">{item['views']}</h5>
                    <small style="color:#888;">İzlenme</small>
                </div>
                <div>
                    <h5 style="margin:0; color:#2196f3;">{item['likes']}</h5>
                    <small style="color:#888;">Beğeni</small>
                </div>
                <div>
                    <h5 style="margin:0; color:#ff9800;">{item['cpa']}</h5>
                    <small style="color:#888;">Tahmini Müşteri Edinme (CPA)</small>
                </div>
                <div>
                    <h5 style="margin:0; color:#e91e63;">{item['margin']}</h5>
                    <small style="color:#888;">Brüt Kâr Marjı</small>
                </div>
            </div>
            <hr style="border: 0.5px solid #2d3139; margin: 10px 0;">
            <div style="display: flex; gap: 15px;">
                <a href="{item['store_url']}" target="_blank" style="text-decoration: none; background-color: #2196f3; color: white; padding: 8px 15px; border-radius: 5px; font-size: 14px; font-weight: bold;">🏪 Rakip Mağazayı İncele</a>
                <a href="{item['ad_link']}" target="_blank" style="text-decoration: none; background-color: #555; color: white; padding: 8px 15px; border-radius: 5px; font-size: 14px; font-weight: bold;">🎥 Reklam Videosunu Gör</a>
            </div>
        </div>
        """, unsafe_allow_unsafe_html=True)

else:
    # Kullanıcı henüz butona basmadıysa hoş geldiniz ekranı göster
    st.write("### 👈 Casusluk yapmaya başlamak için sol paneldeki filtreleri ayarlayın ve butona basın.")
    st.markdown("""
    **Bu Araç ile Neler Yapabilirsiniz?**
    * TikTok ve Facebook'ta gizlice yüksek bütçelerle dönen dropshipping reklamlarını yakalayabilirsiniz.
    * Rakiplerinizin ürünü kaça sattığını ve hangi reklam videolarını kullandığını görebilirsiniz.
    * Boşuna reklam bütçesi harcamadan, Amerika pazarında halihazırda tutmuş ürünleri kopyalayarak satmaya başlayabilirsiniz.
    """)
