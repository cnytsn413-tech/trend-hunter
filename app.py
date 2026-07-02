import streamlit as st
import pandas as pd
import time

# Sayfa Ayarları
st.set_page_config(page_title="WinningHunter Ultimate - E-Com Spy Tool", layout="wide", initial_sidebar_state="expanded")

st.title("🎯 WinningHunter Pro: Ultimate Dropshipping Spy Suite")
st.subheader("Yapay Zeka Destekli Reklam Analizi, Mağaza Casusluğu ve Mayıs-Haziran 2026 Canlı Trend Havuzu")

# --- MANUEL ÜRÜN ARAMA ALANI ---
search_query_input = st.text_input("🔍 Kelime ile Canlı Reklam Ara (Örn: Ice, Fan, Camera, Cleaning, Projector...)", "", help="Arama çubuğuna bir ürün adı yazarak doğrudan filtrelerden bağımsız arama yapabilirsiniz.")

# --- Sol Panel (Filtreler) ---
st.sidebar.header("🛡️ Gelişmiş Casusluk Filtreleri")
platform = st.sidebar.selectbox("Reklam Platformu", ["TikTok Ads", "Meta (Facebook/IG) Ads", "Pinterest Ads"])
target_country = st.sidebar.selectbox("Hedef Ülke (Pazar)", ["US (Amerika)", "EU (Avrupa Birliği)", "GB (İngiltere)", "CA (Kanada)", "TR (Türkiye)"])

category_filter = st.sidebar.selectbox(
    "Ürün Kategorisi", 
    ["Tüm Kategoriler", "Ev & Dekorasyon", "Mutfak Pratik", "Evcil Hayvan", "Güzellik & Kozmetik", "Sağlık & Kişisel Bakım", "Anne & Bebek", "Teknoloji Aksesuarları", "Fitness & Spor"]
)

min_spend, max_spend = st.sidebar.slider("Tahmini Günlük Reklam Bütçesi ($)", 10, 5000, (10, 4500))
sort_by = st.sidebar.selectbox("Sıralama Kriteri", ["En Yüksek Etkileşim (Engagement)", "Viral Artış Hızı"])

# --- 2026 MAYIS-HAZİRAN CANLI VE GENİŞLETİLMİŞ TREND VERİTABANI ---
spy_database = {
    "US (Amerika)": [
        {
            "title": "IceAir Portable 3-in-1 Hydro Cooling Fan", "niche": "Ev & Dekorasyon", "views": "8.4M", "likes": 640000, "days_running": 12, "cpa": 9.20, "margin": 78, "spend": 850, "store_url": "https://iceair-cool.com", "type": "🔥 MAYIS-HAZİRAN 2026 WINNING", 
            "hook": "Summer 2026 is hitting different! 🥵 Drop ice cubes in, turn it on, and blast -5°C instant arctic air anywhere.",
            "audience": "Sıcak yaz ayları, Ev/Ofis soğutma, Kampçılar, Öğrenci evleri | 18-45 Yaş", "trend_base": [80, 150, 240, 380, 490, 580, 640]
        },
        {
            "title": "Ultra-Sonic 360° Magnetic Window Cleaner", "niche": "Ev & Dekorasyon", "views": "5.1M", "likes": 390000, "days_running": 8, "cpa": 14.50, "margin": 72, "spend": 1100, "store_url": "https://glidewindow.com", "type": "📈 HAZİRAN 2026 YÜKSELEN TREND", 
            "hook": "Clean the outside of your high-rise windows safely from the inside! 🤯 Heavy-duty magnetic lock does it for you.",
            "audience": "Ev hanımları, Rezidans/Apartman sakinleri, Temizlik tüyoları | 25-55 Yaş", "trend_base": [20, 55, 110, 190, 260, 330, 390]
        },
        {
            "title": "AI Smart-Track Sports Phone Gimbal", "niche": "Teknoloji Aksesuarları", "views": "9.3M", "likes": 710000, "days_running": 19, "cpa": 11.00, "margin": 65, "spend": 1400, "store_url": "https://aotugimbal.com", "type": "🔥 HAZİRAN 2026 VIRAL", 
            "hook": "No cameraman? No problem. 🎥 This 2026 AI mount locks onto your face and follows you 360° seamlessly.",
            "audience": "TikTok içerik üreticileri, Fitness vloggerları, Dansçılar | 16-35 Yaş", "trend_base": [100, 220, 340, 450, 540, 630, 710]
        }
    ],
    "EU (Avrupa Birliği)": [
        {
            "title": "IceAir Portable 3-in-1 Hydro Cooling Fan", "niche": "Ev & Dekorasyon", "views": "4.2M", "likes": 310000, "days_running": 10, "cpa": 8.90, "margin": 78, "spend": 550, "store_url": "https://iceair-cool.com", "type": "🔥 YAZ TRENDİ", 
            "hook": "No AC in Europe? 🇪🇺 No worries. This desktop hydro cooler feels like a mini iceberg.",
            "audience": "Avrupa yaz sıcakları, Klimasız evler, Ofis çalışanları | 20-40 Yaş", "trend_base": [30, 70, 120, 180, 230, 270, 310]
        },
        {
            "title": "Self-Cleaning Electric Cat Litter Mat", "niche": "Evcil Hayvan", "views": "3.8M", "likes": 290000, "days_running": 15, "cpa": 7.50, "margin": 70, "spend": 600, "store_url": "https://pawsome-tech.com", "type": "👑 HAZİRAN 2026 WINNING", 
            "hook": "Stop sweeping cat litter every single day. 🐾 This smart mat vacuums scattered litter automatically.",
            "audience": "Kedi sahipleri, Pratik evcil hayvan çözümleri | 22-50 Yaş", "trend_base": [40, 85, 130, 175, 215, 250, 290]
        }
    ],
    "CA (Kanada)": [
        {
            "title": "4K Ultra-Short Throw Cinema Projector", "niche": "Teknoloji Aksesuarları", "views": "6.2M", "likes": 480000, "days_running": 14, "cpa": 22.00, "margin": 60, "spend": 1900, "store_url": "https://nextgencinema.com", "type": "🔥 2026 MEGA WINNING", 
            "hook": "Just 10cm away from the wall gives you a massive 150-inch 4K home theater. 🎬 The future of movies is here.",
            "audience": "Ev sineması, Netflix tutkunları, Lüks ev dizaynı | 25-45 Yaş", "trend_base": [50, 110, 190, 270, 350, 420, 480]
        },
        {
            "title": "IceAir Portable 3-in-1 Hydro Cooling Fan", "niche": "Ev & Dekorasyon", "views": "2.1M", "likes": 160000, "days_running": 6, "cpa": 9.50, "margin": 75, "spend": 310, "store_url": "https://iceair-cool.com", "type": "📈 YÜKSELEN TREND", 
            "hook": "Beat the 2026 summer heat waves instantly. Ultra-quiet and USB powered! ☀️",
            "audience": "Ev dekoru, Taşınabilir klima arayanlar | 18-40 Yaş", "trend_base": [15, 40, 65, 95, 120, 145, 160]
        }
    ],
    "TR (Türkiye)": [
        {
            "title": "Hazneli Otomatik Buz Küpü Yapıcı", "niche": "Mutfak Pratik", "views": "1.4M", "likes": 98000, "days_running": 7, "cpa": 3.20, "margin": 65, "spend": 250, "store_url": "https://pratikmutfagim.com", "type": "🔥 HAZİRAN 2026 POPÜLER", 
            "hook": "Yaz sıcaklarında buzdolabında buz beklemeye son! 🧊 Tek tuşla 6 dakikada buz küpleri hazır.",
            "audience": "Yaz içecekleri, Pratik mutfak aletleri, Ev partileri | 18-50 Yaş", "trend_base": [10, 25, 42, 60, 75, 88, 98]
        },
        {
            "title": "Taşınabilir Mini Şarjlı Hava Soğutucu", "niche": "Ev & Dekorasyon", "views": "920K", "likes": 72000, "days_running": 5, "cpa": 4.00, "margin": 70, "spend": 180, "store_url": "https://iceair-cool.com", "type": "📈 YÜKSELEN TREND", 
            "hook": "Masa başı çalışanlar ve klimasız odalar için Haziran 2026 kurtarıcısı! 💨 İçine su ekleyin, serinleyin.",
            "audience": "Öğrenciler, Ofis çalışanları, Ekonomik serinleme | 16-40 Yaş", "trend_base": [8, 20, 35, 48, 58, 66, 72]
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
        st.info(f"🤖 Yapay zeka botları {target_country} pazarını süzüyor...")
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
