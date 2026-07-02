import streamlit as st
import pandas as pd
import time

# Sayfa Ayarları
st.set_page_config(page_title="WinningHunter Ultimate - E-Com Spy Tool", layout="wide", initial_sidebar_state="expanded")

st.title("🎯 WinningHunter Pro: Ultimate Dropshipping Spy Suite")
st.subheader("Yapay Zeka Destekli Reklam Analizi, Mağaza Casusluğu ve Gelişmiş Metrik Yönetimi")

# --- MANUEL ÜRÜN ARAMA ALANI ---
search_query_input = st.text_input("🔍 Kelime ile Canlı Reklam Ara (Örn: Humidifier, Massager, Brush, Camera, Projector...)", "", help="Arama çubuğuna bir ürün adı yazarak doğrudan filtrelerden bağımsız arama yapabilirsiniz.")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🛡️ Gelişmiş Casusluk Filtreleri")
platform = st.sidebar.selectbox("Reklam Platformu", ["TikTok Ads", "Meta (Facebook/IG) Ads", "Pinterest Ads"])
target_country = st.sidebar.selectbox("Hedef Ülke (Pazar)", ["US (Amerika)", "EU (Avrupa Birliği)", "GB (İngiltere)", "CA (Kanada)", "TR (Türkiye)"])

category_filter = st.sidebar.selectbox(
    "Ürün Kategorisi", 
    ["Tüm Kategoriler", "Ev & Dekorasyon", "Mutfak Pratik", "Evcil Hayvan", "Güzellik & Kozmetik", "Sağlık & Kişisel Bakım", "Anne & Bebek", "Teknoloji Aksesuarları", "Fitness & Spor"]
)

min_spend, max_spend = st.sidebar.slider("Tahmini Günlük Reklam Bütçesi ($)", 10, 5000, (10, 3500))
sort_by = st.sidebar.selectbox("Sıralama Kriteri", ["En Yüksek Etkileşim (Engagement)", "Viral Artış Hızı"])

# --- TÜM METRİKLERİ VE KAZANAN ÜRÜNLERİ İÇEREN DEVASE VERİTABANI ---
spy_database = {
    "US (Amerika)": [
        {
            "title": "Anti-Gravity Levitating Humidifier", "niche": "Ev & Dekorasyon", "views": "4.2M", "likes": 310000, "days_running": 14, "cpa": 8.50, "margin": 75, "spend": 450, "store_url": "https://mysticshophome.com", "type": "🔥 WINNING PRODUCT", 
            "hook": "Tired of boring humidifiers? This one literally defies gravity. 🤯 Get yours 50% OFF today!",
            "audience": "Ev dekorasyonu, İç mimari, Modern teknoloji meraklıları | 22-45 Yaş | Unisex", "trend_base": [10, 25, 45, 80, 150, 240, 310]
        },
        {
            "title": "Smart Cupping Therapy Massager", "niche": "Sağlık & Kişisel Bakım", "views": "6.7M", "likes": 520000, "days_running": 28, "cpa": 12.00, "margin": 80, "spend": 1200, "store_url": "https://recoverysmart.com", "type": "🔥 WINNING PRODUCT", 
            "hook": "Recover like a pro athlete from your own bed. 🕒 5 minutes a day is all it takes to melt the pain away.",
            "audience": "Fitness, Vücut Geliştirme, Kronik sırt/bel ağrısı çekenler, Masaj | 25-55 Yaş", "trend_base": [40, 90, 160, 250, 340, 430, 520]
        },
        {
            "title": "Crystal Hair Eraser Exfoliator", "niche": "Güzellik & Kozmetik", "views": "12.4M", "likes": 980000, "days_running": 45, "cpa": 4.50, "margin": 85, "spend": 1800, "store_url": "https://silky-skin-co.com", "type": "🔥 EVERGREEN PRODUCT", 
            "hook": "No more razor burns, no more painful waxing. 🛑 This crystal eraser changes everything.",
            "audience": "Cilt bakımı, Kişisel bakım, Epilasyon ve Kozmetik | 18-35 Yaş | Ağırlıklı Kadın", "trend_base": [200, 350, 500, 680, 800, 900, 980]
        },
        {
            "title": "Flame Effect Air Humidifier Diffuser", "niche": "Ev & Dekorasyon", "views": "2.1M", "likes": 145000, "days_running": 9, "cpa": 6.20, "margin": 70, "spend": 280, "store_url": "https://flamediffuse.com", "type": "📈 VIRAL RISING", 
            "hook": "Add moisture to your room while giving it an insane fireplace vibe. 🔥 Perfect for cozy nights.",
            "audience": "Oda tasarımı (Room Setup), Oyuncu odası, Estetik ev ürünleri | 18-30 Yaş", "trend_base": [5, 15, 32, 55, 82, 115, 145]
        }
    ],
    "EU (Avrupa Birliği)": [
        {
            "title": "Sunset Lamp Bluetooth App Control", "niche": "Ev & Dekorasyon", "views": "3.5M", "likes": 280000, "days_running": 18, "cpa": 6.20, "margin": 78, "spend": 350, "store_url": "https://solarlamp-eu.com", "type": "🔥 HOT IN EUROPE", 
            "hook": "Transform your room vibe with just one click. 🌅 Control over 16 million colors from your phone.",
            "audience": "TikTok/Instagram içerik üreticileri, Fotoğrafçılık, Genç odası dekoru | 16-28 Yaş", "trend_base": [20, 50, 90, 140, 190, 240, 280]
        },
        {
            "title": "Self-Cleaning Pet Grooming Brush", "niche": "Evcil Hayvan", "views": "2.1M", "likes": 190000, "days_running": 11, "cpa": 4.50, "margin": 70, "spend": 250, "store_url": "https://pawsome-europe.com", "type": "👑 WINNING PRODUCT", 
            "hook": "The easiest way to de-shed your pet without the mess! 🐾 One button cleans it all.",
            "audience": "Kedi sahipleri, Köpek sahipleri, Evcil hayvan bakımı | 20-50 Yaş | Unisex", "trend_base": [15, 35, 65, 95, 130, 165, 190]
        }
    ],
    "CA (Kanada)": [
        {
            "title": "Portable Mini HD Pocket Projector", "niche": "Teknoloji Aksesuarları", "views": "3.1M", "likes": 240000, "days_running": 13, "cpa": 18.50, "margin": 60, "spend": 720, "store_url": "https://cybertech-us.com", "type": "🔥 WINNING PRODUCT", 
            "hook": "Turn any blank wall into a 130-inch cinematic home theater. 🎬 Built-in speaker, connects to phone.",
            "audience": "Ev sineması, Film/Dizi severler, Kamp ve Seyahat, Gadget meraklıları | 20-40 Yaş", "trend_base": [10, 35, 70, 110, 150, 195, 240]
        }
    ],
    "TR (Türkiye)": [
        {
            "title": "Pratik Şarjlı Sebze Doğrayıcı", "niche": "Mutfak Pratik", "views": "620K", "likes": 45000, "days_running": 7, "cpa": 2.50, "margin": 65, "spend": 80, "store_url": "https://chefkitchentools.com", "type": "🔥 POPÜLER", 
            "hook": "Yemek yaparken saatlerce soğan doğramaya son! 🧅 Şarjlı ve aşırı pratik.",
            "audience": "Pratik mutfak araçları, Yemek tarifleri, Ev düzeni | 25-60 Yaş | Kadın & Erkek", "trend_base": [2, 7, 14, 22, 29, 37, 45]
        }
    ]
}

# --- Veri Havuzunu Düzleştirme Mantığı ---
all_ads_list = []
for country, ads in spy_database.items():
    for ad in ads:
        ad_copy = ad.copy()
        ad_copy["country"] = country
        all_ads_list.append(ad_copy)

# --- Tetikleyici ve Arama Algoritması ---
if st.sidebar.button("🕵️‍♂️ Canlı Reklam Ağını Taramaya Başla") or (search_query_input != ""):
    filtered_ads = []
    
    if search_query_input != "":
        st.info(f"🔍 Küresel veri havuzunda '{search_query_input}' kelimesi manuel olarak aranıyor...")
        for ad in all_ads_list:
            if search_query_input.lower() in ad["title"].lower() or search_query_input.lower() in ad["niche"].lower():
                filtered_ads.append(ad)
    else:
        st.info(f"🤖 Yapay zeka botları {target_country} bölgesini süzüyor...")
        for ad in all_ads_list:
            if ad["country"] == target_country:
                if category_filter == "Tüm Kategoriler" or ad["niche"] == category_filter:
                    if min_spend <= ad["spend"] <= max_spend:
                        filtered_ads.append(ad)

    # Sıralama Kriterleri
    if sort_by == "En Yüksek Etkileşim (Engagement)":
        filtered_ads = sorted(filtered_ads, key=lambda x: x["likes"], reverse=True)
    else:
        filtered_ads = sorted(filtered_ads, key=lambda x: x["days_running"])

    # Yükleme Barı Animasyonu
    progress_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.002)
        progress_bar.progress(percent_complete + 1)

    if not filtered_ads:
        st.warning("⚠️ Aradığınız kriterlere uygun ürün bulunamadı. Lütfen filtreleri esnetin.")
    else:
        st.success(f"⚡ Toplam {len(filtered_ads)} adet canlı reklam listelendi!")
        
        # --- ÖZELLİK 1: KÜRESEL PAZAR TABLO GÖRÜNÜMÜ ---
        with st.expander("📊 Tüm Sonuçları Büyük Veri Tablosu Olarak İncele / Excel Olarak İndir"):
            df = pd.DataFrame(filtered_ads)[["title", "niche", "country", "views", "likes", "spend"]]
            df.columns = ["Ürün Adı", "Kategori", "Pazar Ülkesi", "Toplam İzlenme", "Toplam Beğeni", "Günlük Reklam Harcaması ($)"]
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Tabloyu CSV Olarak Bilgisayara İndir", csv, "winning_products_report.csv", "text/csv")

        st.write("---")
        
        # --- ÜRÜN KARTLARI DÖNGÜSÜ ---
        for item in filtered_ads:
            with st.container(border=True):
                col_title, col_badge = st.columns([3, 1])
                with col_title:
                    st.subheader(item['title'])
                    st.caption(f"Kategori: **{item['niche']}** | Pazar: **{item['country']}** | Reklam Süresi: {item['days_running']} Gün")
                with col_badge:
                    st.warning(item['type'])
                
                # Metrik Göstergeleri
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Toplam İzlenme", item['views'])
                m2.metric("Toplam Beğeni", f"{item['likes']:,}")
                m3.metric("Tahmini CPA", f"${item['cpa']:.2f}")
                m4.metric("Ortalama Brüt Marj", f"%{item['margin']}")
                
                # --- ÖZELLİK 2: TREND GRAFİK SİMÜLASYONU ---
                with st.expander("📈 Son 7 Günlük Viral Etkileşim Artış İvmesini Görselleştir"):
                    chart_data = pd.DataFrame({
                        "Günler": ["1. Gün", "2. Gün", "3. Gün", "4. Gün", "5. Gün", "6. Gün", "Son Gün"],
                        "Beğeni Artış Hızı (K)": item["trend_base"]
                    }).set_index("Günler")
                    st.line_chart(chart_data)
                
                # Buton Satırları Kontrolü
                btn_col1, btn_col2, btn_col3 = st.columns(3)
                search_query = item['title'].replace(" ", "+")
                aliexpress_url = f"https://www.aliexpress.com/w/wholesale-{search_query}.html"
                
                with btn_col1:
                    st.link_button("🏪 Rakip Mağazayı İncele", item['store_url'], use_container_width=True)
                with btn_col2:
                    st.link_button("🇨🇳 AliExpress Tedarikçisini Bul", aliexpress_url, use_container_width=True)
                with btn_col3:
                    # --- ÖZELLİK 3: AI HEDEF KİTLE & POPOVER ---
                    with st.popover("🤖 AI Reklam Metni & Hedef Kitle Önerisi", use_container_width=True):
                        st.markdown("### 📝 AI Reklam Metni (Hook)")
                        st.code(item['hook'], language="text")
                        st.markdown("### 🎯 Reklam Seti Hedef Kitle Önerisi")
                        st.info(item['audience'])

                # --- ÖZELLİK 4: DROPSHIPPING KÂR HESAPLAYICI ---
                with st.expander("🧮 Gelişmiş E-Ticaret Kâr / ROI Hesaplayıcı Simülatörü"):
                    calc_col1, calc_col2, calc_col3 = st.columns(3)
                    with calc_col1:
                        c_cost = st.number_input(f"Tedarik Maliyeti ($) - [{item['title'][:12]}]", value=5.00, step=0.50)
                    with calc_col2:
                        c_price = st.number_input(f"Mağaza Satış Fiyatın ($) - [{item['title'][:12]}]", value=29.90, step=1.00)
                    with calc_col3:
                        c_cpa = st.number_input(f"Tahmini Reklam CPA ($) - [{item['title'][:12]}]", value=item['cpa'], step=0.50)
                    
                    gross_profit = c_price - c_cost
                    net_profit = c_price - c_cost - c_cpa
                    roi = (net_profit / (c_cost + c_cpa)) * 100 if (c_cost + c_cpa) > 0 else 0
                    
                    r_col1, r_col2, r_col3 = st.columns(3)
                    r_col1.metric("Brüt Kâr (Ürün Başı)", f"${gross_profit:.2f}")
                    r_col2.metric("Net Kâr (Reklam Dahil)", f"${net_profit:.2f}", delta=f"${net_profit:.2f}")
                    if roi > 0:
                        r_col3.metric("Yatırım Getirisi (ROI)", f"%{roi:.1f}", delta="🔥 YÜKSEK POTANSİYEL")
                    else:
                        r_col3.metric("Yatırım Getirisi (ROI)", f"%{roi:.1f}", delta="⚠️ RİSKLİ MARJ", delta_color="inverse")

                st.write("") 
else:
    st.write("### 👈 Arama çubuğunu kullanın veya filtreleri ayarlayıp sol panelden casus yazılımı çalıştırın.")
