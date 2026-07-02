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
        },
        {
            "title": "Baby White Noise Soother Bear", 
            "niche": "Anne & Bebek", 
            "views": "2.8M", 
            "likes": 195000, 
            "days_running": 12, 
            "cpa": "$7.20", 
            "margin": "%72", 
            "spend": 320, 
            "store_url": "https://cozybaby-us.com", 
            "type": "📈 VIRAL RISING", 
            "hook": "Get your baby to sleep in minutes with this smart white noise heartbeat bear. 🧸 Absolute lifesaver for parents!"
        },
        {
            "title": "MagSafe Transparent Powerbank", 
            "niche": "Teknoloji Aksesuarları", 
            "views": "5.1M", 
            "likes": 410000, 
            "days_running": 19, 
            "cpa": "$11.50", 
            "margin": "%68", 
            "spend": 850, 
            "store_url": "https://cybertech-us.com", 
            "type": "🔥 WINNING PRODUCT", 
            "hook": "See the tech inside! 🔋 Cyberpunk style meets ultra-fast MagSafe charging. Running out of battery is officially over."
        },
        {
            "title": "Adjustable Smart Counting Hula Hoop", 
            "niche": "Fitness & Spor", 
            "views": "8.3M", 
            "likes": 670000, 
            "days_running": 30, 
            "cpa": "$9.00", 
            "margin": "%77", 
            "spend": 1400, 
            "store_url": "https://fitshape-co.com", 
            "type": "🔥 EVERGREEN PRODUCT", 
            "hook": "Burn 500 calories while watching your favorite show! 💃 This hula hoop never drops and counts your reps automatically."
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
        },
        {
            "title": "Orthopedic Chronic Neck Stretcher", 
            "niche": "Sağlık & Kişisel Bakım", 
            "views": "1.9M", 
            "likes": 130000, 
            "days_running": 9, 
            "cpa": "€8.00", 
            "margin": "%82", 
            "spend": 180, 
            "store_url": "https://spinecare-eu.com", 
            "type": "📈 VIRAL RISING", 
            "hook": "Sitting at a desk all day? Relieve neck tension in just 8 minutes. 🧘‍♂️ Fast shipping inside EU!"
        },
        {
            "title": "Automatic Electric Baby Nail Trimmer", 
            "niche": "Anne & Bebek", 
            "views": "1.4M", 
            "likes": 92000, 
            "days_running": 6, 
            "cpa": "€3.90", 
            "margin": "%74", 
            "spend": 110, 
            "store_url": "https://babysafe-eu.com", 
            "type": "📈 VIRAL RISING", 
            "hook": "Stop worrying about scratching your newborn's skin! 👶 Safe, silent, and works even when they sleep."
        },
        {
            "title": "Fast-Absorbing Diatomite Bath Mat", 
            "niche": "Ev & Dekorasyon", 
            "views": "3.8M", 
            "likes": 210000, 
            "days_running": 15, 
            "cpa": "€5.10", 
            "margin": "%80", 
            "spend": 400, 
            "store_url": "https://drystep-mat.com", 
            "type": "🔥 WINNING PRODUCT", 
            "hook": "Dries in literally 3 seconds. 🧼 Say goodbye to soggy, moldy bathroom mats forever!"
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
        },
        {
            "title": "Electric Garlic & Vegetable Chopper", 
            "niche": "Mutfak Pratik", 
            "views": "950K", 
            "likes": 68000, 
            "days_running": 5, 
            "cpa": "$3.10", 
            "margin": "%60", 
            "spend": 90, 
            "store_url": "https://chefkitchentools.com", 
            "type": "📈 VIRAL RISING", 
            "hook": "Prep meals in 3 seconds flat. 🔪 Cordless, powerful, and washes in seconds."
        },
        {
            "title": "Grip Strength Trainer with Counter", 
            "niche": "Fitness & Spor", 
            "views": "2.4M", 
            "likes": 180000, 
            "days_running": 14, 
            "cpa": "$4.10", 
            "margin": "%73", 
            "spend": 280,
    
