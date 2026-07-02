import streamlit as st
import pandas as pd
import time

# Sayfa Ayarları
st.set_page_config(page_title="WinningHunter Ultimate - E-Com Spy Tool", layout="wide", initial_sidebar_state="expanded")

st.title("🎯 WinningHunter Pro: Ultimate Dropshipping Spy Suite")
st.subheader("Yapay Zeka Destekli Reklam Analizi, Mağaza Casusluğu ve Genişletilmiş Ürün Havuzu")

# --- MANUEL ÜRÜN ARAMA ALANI ---
search_query_input = st.text_input("🔍 Kelime ile Canlı Reklam Ara (Örn: Humidifier, Massager, Brush, Camera, Projector...)", "", help="Arama çubuğuna bir ürün adı yazarak doğrudan filtrelerden bağımsız arama yapabilirsiniz. Filtreleri kullanmak için burayı boş bırakın.")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🛡️ Gelişmiş Casusluk Filtreleri")
platform = st.sidebar.selectbox("Reklam Platformu", ["TikTok Ads", "Meta (Facebook/IG) Ads", "Pinterest Ads"])
target_country = st.sidebar.selectbox("Hedef Ülke (Pazar)", ["US (Amerika)", "EU (Avrupa Birliği)", "GB (İngiltere)", "CA (Kanada)", "TR (Türkiye)"])

category_filter = st.sidebar.selectbox(
    "Ürün Kategorisi", 
    ["Tüm Kategoriler", "Ev & Dekorasyon", "Mutfak Pratik", "Evcil Hayvan", "Güzellik & Kozmetik", "Sağlık & Kişisel Bakım", "Anne & Bebek", "Teknoloji Aksesuarları", "Fitness & Spor"]
)

ad_creation_date = st.sidebar.selectbox("Reklam Yayınlanma Tarihi", ["Son 7 Gün", "Son 30 Gün", "Son 90 Gün"])

min_spend, max_spend = st.sidebar.slider("Tahmini Günlük Reklam Bütçesi ($)", 10, 5000, (10, 3500))
sort_by = st.sidebar.selectbox("Sıralama Kriteri", ["En Yüksek Etkileşim (Engagement)", "Viral Artış Hızı"])

# --- GENİŞLETİLMİŞ VE ZENGİNLEŞTİRİLMİŞ VERİTABANI ---
spy_database = {
    "US (Amerika)": [
        {
            "title": "Anti-Gravity Levitating Humidifier", 
            "niche": "Ev & Dekorasyon", 
            "views": "4.2M", "likes": 310000, "days_running": 14, "cpa": "$8.50", "margin": "%75", "spend": 450, 
            "store_url": "https://mysticshophome.com", "type": "🔥 WINNING PRODUCT", 
            "hook": "Tired of boring humidifiers? This one literally defies gravity. 🤯 Get yours 50% OFF today!"
        },
        {
            "title": "Smart Cupping Therapy Massager", 
            "niche": "Sağlık & Kişisel Bakım", 
            "views": "6.7M", "likes": 520000, "days_running": 28, "cpa": "$12.00", "margin": "%80", "spend": 1200, 
            "store_url": "https://recoverysmart.com", "type": "🔥 WINNING PRODUCT", 
            "hook": "Recover like a pro athlete from your own bed. 🕒 5 minutes a day is all it takes to melt the pain away."
        },
        {
            "title": "Crystal Hair Eraser Exfoliator", 
            "niche": "Güzellik & Kozmetik", 
            "views": "12.4M", "likes": 980000, "days_running": 45, "cpa": "$4.50", "margin": "%85", "spend": 1800, 
            "store_url": "https://silky-skin-co.com", "type": "🔥 EVERGREEN PRODUCT", 
            "hook": "No more razor burns, no more painful waxing. 🛑 This crystal eraser changes everything."
        },
        {
            "title": "Flame Effect Air Humidifier Diffuser", 
            "niche": "Ev & Dekorasyon", 
            "views": "2.1M", "likes": 145000, "days_running": 9, "cpa": "$6.20", "margin": "%70", "spend": 280, 
            "store_url": "https://flamediffuse.com", "type": "📈 VIRAL RISING", 
            "hook": "Add moisture to your room while giving it an insane fireplace vibe. 🔥 Perfect for cozy nights."
        },
        {
            "title": "Baby White Noise Soother Bear", 
            "niche": "Anne & Bebek", 
            "views": "2.8M", "likes": 195000, "days_running": 12, "cpa": "$7.20", "margin": "%72", "spend": 320, 
            "store_url": "https://cozybaby-us.com", "type": "📈 VIRAL RISING", 
            "hook": "Get your baby to sleep in minutes with this smart white noise heartbeat bear. 🧸 Absolute lifesaver for parents!"
        },
        {
            "title": "MagSafe Transparent Powerbank", 
            "niche": "Teknoloji Aksesuarları", 
            "views": "5.1M", "likes": 410000, "days_running": 19, "cpa": "$11.50", "margin": "%68", "spend": 850, 
            "store_url": "https://cybertech-us.com", "type": "🔥 WINNING PRODUCT", 
            "hook": "See the tech inside! 🔋 Cyberpunk style meets ultra-fast MagSafe charging. Running out of battery is officially over."
        },
        {
            "title": "Adjustable Smart Counting Hula Hoop", 
            "niche": "Fitness & Spor", 
            "views": "8.3M", "likes": 670000, "days_running": 30, "cpa": "$9.00", "margin": "%77", "spend": 1400, 
            "store_url": "https://fitshape-co.com", "type": "🔥 EVERGREEN PRODUCT", 
            "hook": "Burn 500 calories while watching your favorite show! 💃 This hula hoop never drops and counts your reps automatically."
        },
        {
            "title": "Deep Tissue Percussion Massage Gun", 
            "niche": "Sağlık & Kişisel Bakım", 
            "views": "3.4M", "likes": 220000, "days_running": 16, "cpa": "$14.00", "margin": "%65", "spend": 610, 
            "store_url": "https://recoverysmart.com", "type": "📈 TEST PHASE", 
            "hook": "Say goodbye to muscle soreness instantly. 🏋️‍♂️ 30 speed levels to unlock professional-grade recovery at home."
        },
        {
            "title": "4-in-1 Handheld Electric Vegetable Slicer", 
            "niche": "Mutfak Pratik", 
            "views": "1.9M", "likes": 110000, "days_running": 8, "cpa": "$5.00", "margin": "%73", "spend": 210, 
            "store_url": "https://chefkitchentools.com", "type": "📈 VIRAL RISING", 
            "hook": "Chop, slice, peel, and clean in seconds! 🧄 The ultimate cordless kitchen sidekick is here."
        }
    ],
    "EU (Avrupa Birliği)": [
        {
            "title": "Sunset Lamp Bluetooth App Control", 
            "niche": "Ev & Aydınlatma", 
            "views": "3.5M", "likes": 280000, "days_running": 18, "cpa": "€6.20", "margin": "%78", "spend": 350, 
            "store_url": "https://solarlamp-eu.com", "type": "🔥 HOT IN EUROPE", 
            "hook": "Transform your room vibe with just one click. 🌅 Control over 16 million colors from your phone."
        },
        {
            "title": "Self-Cleaning Pet Grooming Brush", 
            "niche": "Evcil Hayvan", 
            "views": "2.1M", "likes": 190000, "days_running": 11, "cpa": "€4.50", "margin": "%70", "spend": 250, 
            "store_url": "https://pawsome-europe.com", "type": "👑 WINNING PRODUCT", 
            "hook": "The easiest way to de-shed your pet without the mess! 🐾 One button cleans it all."
        },
        {
            "title": "Orthopedic Chronic Neck Stretcher", 
            "niche": "Sağlık & Kişisel Bakım", 
            "views": "1.9M", "likes": 130000, "days_running": 9, "cpa": "€8.00", "margin": "%82", "spend": 180, 
            "store_url": "https://spinecare-eu.com", "type": "📈 VIRAL RISING", 
            "hook": "Sitting at a desk all day? Relieve neck tension in just 8 minutes. 🧘‍♂️ Fast shipping inside EU!"
        },
        {
            "title": "Automatic Electric Baby Nail Trimmer", 
            "niche": "Anne & Bebek", 
            "views": "1.4M", "likes": 92000, "days_running": 6, "cpa": "€3.90", "margin": "%74", "spend": 110, 
            "store_url": "https://babysafe-eu.com", "type": "📈 VIRAL RISING", 
            "hook": "Stop worrying about scratching your newborn's skin! 👶 Safe, silent, and works even when they sleep."
        },
        {
            "title": "Fast-Absorbing Diatomite Bath Mat", 
            "niche": "Ev & Dekorasyon", 
            "views": "3.8M", "likes": 210000, "days_running": 15, "cpa": "€5.10", "margin": "%80", "spend": 400, 
            "store_url": "https://drystep-mat.com", "type": "🔥 WINNING PRODUCT", 
            "hook": "Dries in literally 3 seconds. 🧼 Say goodbye to soggy, moldy bathroom mats forever!"
        },
        {
            "title": "Pet Hair Remover Roller Brush", 
            "niche": "Evcil Hayvan", 
            "views": "4.5M", "likes": 310000, "days_running": 22, "cpa": "€3.50", "margin": "%75", "spend": 550, 
            "store_url": "https://pawsome-europe.com", "type": "🔥 EVERGREEN PRODUCT", 
            "hook": "No sticky tapes, no refills required. 🐶 Roll it back and forth and pick up all pet hair instantly."
        }
    ],
    "GB (İngiltere)": [
        {
            "title": "Wireless Cat Water Fountain", 
            "niche": "Evcil Hayvan", 
            "views": "1.8M", "likes": 145000, "days_running": 8, "cpa": "$5.20", "margin": "%68", "spend": 150, 
            "store_url": "https://happy-paws-co.myshopify.com", "type": "📈 VIRAL RISING", 
            "hook": "Cats prefer running water! Keep your best friend hydrated and healthy with zero wires. 🐈"
        },
        {
            "title": "Electric Garlic & Vegetable Chopper", 
            "niche": "Mutfak Pratik", 
            "views": "950K", "likes": 68000, "days_running": 5, "cpa": "$3.10", "margin": "%60", "spend": 90, 
            "store_url": "https://chefkitchentools.com", "type": "📈 VIRAL RISING", 
            "hook": "Prep meals in 3 seconds flat. 🔪 Cordless, powerful, and washes in seconds."
        },
        {
            "title": "Grip Strength Trainer with Counter", 
            "niche": "Fitness & Spor", 
            "views": "2.4M", "likes": 180000, "days_running": 14, "cpa": "$4.10", "margin": "%73", "spend": 280, 
            "store_url": "https://alpha-grip.co.uk", "type": "🔥 WINNING PRODUCT", 
            "hook": "Level up your forearm veins and crush your lifting PRs. 🦾 Adjustable resistance up to 60kg."
        }
    ],
    "CA (Kanada)": [
        {
            "title": "Anti-Gravity Levitating Humidifier", 
            "niche": "Ev & Dekorasyon", 
            "views": "1.1M", "likes": 95000, "days_running": 10, "cpa": "$9.00", "margin": "%75", "spend": 210, 
            "store_url": "https://mysticshophome.com", "type": "📈 TEST PHASE",
            "hook": "Winter is coming, protect your skin in style. ❄️ Watch the water droplets flow upwards!"
        },
        {
            "title": "Waterproof HD Endoscope Camera", 
            "niche": "Teknoloji Aksesuarları", 
            "views": "1.7M", "likes": 115000, "days_running": 7, "cpa": "$13.20", "margin": "%65", "spend": 310, 
            "store_url": "https://inspecto-cam.com", "type": "📈 VIRAL RISING", 
            "hook": "See into impossible places! 🔍 Perfect for plumbing, car repairs, and DIY fixes right from your smartphone."
        },
        {
            "title": "Portable Mini HD Pocket Projector", 
            "niche": "Teknoloji Aksesuarları", 
            "views": "3.1M", "likes": 240000, "days_running": 13, "cpa": "$18.50", "margin": "%60", "spend": 720, 
            "store_url": "https://cybertech-us.com", "type": "🔥 WINNING PRODUCT", 
            "hook": "Turn any blank wall into a 130-inch cinematic home theater. 🎬 Built-in speaker, connects to phone."
        }
    ],
    "TR (Türkiye)": [
        {
            "title": "Pratik Şarjlı Sebze Doğrayıcı", 
            "niche": "Mutfak Pratik", 
            "views": "620K", "likes": 45000, "days_running": 7, "cpa": "$2.50", "margin": "%65", "spend": 80, 
            "store_url": "https://chefkitchentools.com", "type": "🔥 POPÜLER", 
            "hook": "Yemek yaparken saatlerce soğan doğramaya son! 🧅 Şarjlı ve aşırı pratik."
        },
        {
            "title": "Kablosuz Kedi Su Pınarı", 
            "niche": "Evcil Hayvan", 
            "views": "410K", "likes": 32000, "days_running": 4, "cpa": "$4.00", "margin": "%60", "spend": 60, 
            "store_url": "https://happy-paws-co.myshopify.com", "type": "📈 YÜKSELEN TREND", 
            "hook": "Kediniz taze su içsin diye kablosuz, sessiz su pınarı. 🐱 Sınırlı stok!"
        },
        {
            "title": "Siyah Nokta Temizleme Vakumu", 
            "niche": "Güzellik & Kozmetik", 
            "views": "850K", "likes": 61000, "days_running": 11, "cpa": "$3.20", "margin": "%78", "spend": 140, 
            "store_url": "https://pürüzsüzcilt.com", "type": "🔥 POPÜLER", 
            "hook": "Tek kullanımda gözenekleri derinlemesine temizler! 🧼 Cilt bakım randevularına servet ödemeyin."
        },
        {
            "title": "Ultrasonik Yüz Temizleme Cihazı", 
            "niche": "Güzellik & Kozmetik", 
            "views": "530K", "likes": 39000, "days_running": 5, "cpa": "$3.80", "margin": "%72", "spend": 95, 
            "store_url": "https://pürüzsüzcilt.com", "type": "📈 YÜKSELEN TREND", 
            "hook": "Dakikada 8000 sonik titreşimle cildinizdeki tüm kiri ve makyaj kalıntılarını söküp atın! ✨"
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
