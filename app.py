import streamlit as st
import pandas as pd
import time

# Sayfa Ayarları
st.set_page_config(page_title="WinningHunter Ultimate - E-Com Spy Tool", layout="wide", initial_sidebar_state="expanded")

st.title("🎯 WinningHunter Pro: Ultimate Dropshipping Spy Suite")
st.subheader("Yapay Zeka Destekli Reklam Analizi, Mağaza Casusluğu ve Manuel Ürün Arama")

# --- MANUEL ÜRÜN ARAMA ALANI ---
search_query_input = st.text_input("🔍 Kelime ile Canlı Reklam Ara (Örn: Humidifier, Massager, Brush...)", "", help="Arama çubuğuna bir ürün adı yazarak doğrudan filtrelerden bağımsız arama yapabilirsiniz. Filtreleri kullanmak için burayı boş bırakın.")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🛡️ Gelişmiş Casusluk Filtreleri")
platform = st.sidebar.selectbox("Reklam Platformu", ["TikTok Ads", "Meta (Facebook/IG) Ads", "Pinterest Ads"])
target_country = st.sidebar.selectbox("Hedef Ülke (Pazar)", ["US (Amerika)", "EU (Avrupa Birliği)", "GB (İngiltere)", "CA (Kanada)", "TR (Türkiye)"])

category_filter = st.sidebar.selectbox(
    "Ürün Kategorisi", 
    ["Tüm Kategoriler", "Ev & Dekorasyon", "Mutfak Pratik", "Evcil Hayvan", "Güzellik & Kozmetik", "Sağlık & Kişisel Bakım", "Anne & Bebek", "Teknoloji Aksesuarları", "Fitness & Spor"]
)

ad_creation_date = st.sidebar.selectbox("Reklam Yayınlanma Tarihi", ["Son 7 Gün", "Son 30 Gün", "Son 90 Gün"])

min_spend, max_spend = st.sidebar.slider("Tahmini Günlük Reklam Bütçesi ($)", 10, 5000, (30, 2500))
sort_by = st.sidebar.selectbox("Sıralama Kriteri", ["En Yüksek Etkileşim (Engagement)", "Viral Artış Hızı"])

# --- TÜM KATEGORİLERİ İÇEREN GÜVENLİ VERİTABANI ---
spy_database = {
    "US (Amerika)": [
        {
            "title": "Anti-Gravity Levitating Humidifier", 
            "niche": "Ev & Dekorasyon", 
            "views": "4.2M", 
            "likes": 310000, 
            "days_running": 14, 
            "cpa": "$8.50", 
            "margin": "%75", 
            "spend": 450, 
            "store_url": "https://mysticshophome.com", 
            "type": "🔥 WINNING PRODUCT", 
            "hook": "Tired of boring humidifiers? This one literally defies gravity. 🤯 Get yours 50% OFF today!"
        },
        {
            "title": "Smart Cupping Therapy Massager", 
            "niche": "Sağlık & Kişisel Bakım", 
            "views": "6.7M", 
            "likes": 520000, 
            "days_running": 28, 
            "cpa": "$12.00", 
            "margin": "%80", 
            "spend": 1200, 
            "store_url": "https://recoverysmart.com", 
            "type": "🔥 WINNING PRODUCT", 
            "hook": "Recover like a pro athlete from your own bed. 🕒 5 minutes a day is all it takes to melt the pain away."
        },
        {
            "title": "Crystal Hair Eraser Exfoliator", 
            "niche": "Güzellik & Kozmetik", 
            "views": "12.4M", 
            "likes": 980000, 
            "days_running": 45, 
            "cpa": "$4.50", 
            "margin": "%85", 
            "spend": 1800, 
            "store_url": "https://silky-skin-co.com", 
            "type": "🔥 EVERGREEN PRODUCT", 
            "hook": "No more razor burns, no more painful waxing. 🛑 This crystal eraser changes everything."
        }
    ],
    "EU (Avrupa Birliği)": [
        {
            "title": "Sunset Lamp Bluetooth App Control", 
            "niche": "Ev & Aydınlatma", 
            "views": "3.5M", 
            "likes": 280000, 
            "days_running": 18, 
            "cpa": "€6.20", 
            "margin": "%78", 
            "spend": 350, 
            "store_url": "https://solarlamp-eu.com", 
            "type": "🔥 HOT IN EUROPE", 
            "hook": "Transform your room vibe with just one click. 🌅 Control over 16 million colors from your phone."
        },
        {
            "title": "Self-Cleaning Pet Grooming Brush", 
            "niche": "Evcil Hayvan", 
            "views": "2.1M", 
            "likes": 190000, 
            "days_running": 11, 
            "cpa": "€4.50", 
            "margin": "%70", 
            "spend": 250, 
            "store_url": "https://pawsome-europe.com", 
            "type": "👑 WINNING PRODUCT", 
            "hook": "The easiest way to de-shed your pet without the mess! 🐾 One button cleans it all."
        }
    ],
    "GB (İngiltere)": [
        {
            "title": "Wireless Cat Water Fountain", 
            "niche": "Evcil Hayvan", 
            "views": "1.8M", 
            "likes": 145000, 
            "days_running": 8, 
            "cpa": "$5.20", 
            "margin": "%68", 
            "spend": 150, 
            "store_url": "https://happy-paws-co.myshopify.com", 
            "type": "📈 VIRAL RISING", 
            "hook": "Cats prefer running water! Keep your best friend hydrated and healthy with zero wires. 🐈"
        }
    ],
    "CA (Kanada)": [
        {
            "title": "Anti-Gravity Levitating Humidifier", 
            "niche": "Ev & Dekorasyon", 
            "views": "1.1M", 
            "likes": 95000, 
            "days_running": 10, 
            "cpa": "$9.00", 
            "margin": "%75", 
            "spend": 210, 
            "store_url": "https://mysticshophome.com", 
            "type": "📈 TEST PHASE",
            "hook": "Winter is coming, protect your skin in style. ❄️ Watch the water droplets flow upwards!"
        }
    ],
    "TR (Türkiye)": [
        {
            "title": "Pratik Şarjlı Sebze Doğrayıcı", 
            "niche": "Mutfak Pratik", 
            "views": "620K", 
            "likes": 45000, 
            "days_running": 7, 
            "cpa": "$2.50", 
            "margin": "%65", 
            "spend": 80, 
            "store_url": "https://chefkitchentools.com", 
            "type": "🔥 POPÜLER", 
            "hook": "Yemek yaparken saatlerce soğan doğramaya son! 🧅 Şarjlı ve aşırı pratik."
        }
    ]
}

# --- Ana Ekran Aksiyonu ---
if st.sidebar.button("🕵️‍♂️ Canlı Reklam Ağını Taramaya Başla") or (search_query_input != ""):
    filtered_ads = []
    
    if search_query_input != "":
        st.info(f"🔍 Bütün ülkelerin veri havuzunda '{search_query_input}' kelimesi manuel olarak aranıyor...")
        for country, ads in spy_database.items():
            for ad in ads:
                if search_query_input.lower() in ad["title"].lower() or search_query_input.lower() in ad["niche"].lower():
                    if ad not in filtered_ads:
                        filtered_ads.append(ad)
    else:
        st.info(f"🤖 Yapay zeka botları {target_country} bölgesinde aktif {platform} reklam harcamalarını süzüyor...")
        raw_ads = spy_database.get(target_country, [])
        if category_filter != "Tüm Kategoriler":
            raw_ads = [ad for ad in raw_ads if ad["niche"] == category_filter]
        filtered_ads = [ad for ad in raw_ads if min_spend <= ad["spend"] <= max_spend]

    # Sıralama Mantığı
    if sort_by == "En Yüksek Etkileşim (Engagement)":
        filtered_ads = sorted(filtered_ads, key=lambda x: x["likes"], reverse=True)
    else:
        filtered_ads = sorted(filtered_ads, key=lambda x: x["days_running"])

    # Yükleme Barı
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.003)
        progress_bar.progress(percent_complete + 1)

    if not filtered_ads:
        st.warning("⚠️ Aradığınız kriterlere veya kelimeye uygun aktif reklam bulunamadı. Lütfen kelimeyi kontrol edin veya filtreleri esnetin.")
    else:
        st.success(f"⚡ Toplam {len(filtered_ads)} adet canlı reklam listelendi!")
        st.write("---")
        
        for item in filtered_ads:
            with st.container(border=True):
                col_title, col_badge = st.columns([3, 1])
                with col_title:
                    st.subheader(item['title'])
                    st.caption(f"Kategori: **{item['niche']}** | Günlük Reklam Harcaması: **${item['spend']}** | Reklam Süresi: {item['days_running']} Gün")
                with col_badge:
                    st.warning(item['type'])
                
                # Metrikler
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("İzlenme", item['views'])
                m2.metric("Beğeni", f"{item['likes']:,}")
                m3.metric("Tahmini CPA", item['cpa'])
                m4.metric("Brüt Kâr Marjı", item['margin'])
                
                # Dinamik AliExpress Arama Linki
                search_query = item['title'].replace(" ", "+")
                aliexpress_url = f"https://www.aliexpress.com/w/wholesale-{search_query}.html"
                
                # Butonlar Bölümü
                btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
                with btn_col1:
                    st.link_button("🏪 Rakip Mağazayı İncele", item['store_url'], use_container_width=True)
                with btn_col2:
                    st.link_button("🇨🇳 AliExpress Tedarikçisini Bul", aliexpress_url, use_container_width=True)
                with btn_col3:
                    with st.popover("🤖 AI Viral Reklam Metnini Üret", use_container_width=True):
                        st.write("**Kopyala ve Reklamında Kullan:**")
                        st.code(item['hook'], language="text")
                
                st.write("") 
else:
    st.write("### 👈 Arama çubuğunu kullanın veya filtreleri ayarlayıp sol panelden casus yazılımı çalıştırın.")
