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

# AVRUPA BİRLİĞİ EKLENMİŞ ÜLKE/BÖLGE FİLTRESİ
target_country = st.sidebar.selectbox("Hedef Ülke (Pazar)", ["US (Amerika)", "EU (Avrupa Birliği)", "GB (İngiltere)", "CA (Kanada)", "TR (Türkiye)"])

ad_creation_date = st.sidebar.selectbox("Reklam Yayınlanma Tarihi", ["Son 7 Gün", "Son 30 Gün", "Son 90 Gün"])
daily_spend = st.sidebar.slider("Tahmini Günlük Reklam Bütçesi ($)", 50, 5000, (100, 1500))
sort_by = st.sidebar.selectbox("Sıralama Kriteri", ["En Yüksek Etkileşim (Engagement)", "En Yeni Reklamlar", "Viral Artış Hızı"])

# --- Ülke ve Bölgelere Göre Dinamik Değişen Reklam Veritabanı ---
spy_database = {
    "US (Amerika)": [
        {"title": "Anti-Gravity Levitating Humidifier", "niche": "Ev & Dekorasyon", "views": "4.2M", "likes": "310K", "days_running": 14, "cpa": "$8.50", "margin": "%75", "store_url": "https://mysticshophome.com", "ad_link": "https://tiktok.com/ads/library", "type": "🔥 WINNING PRODUCT (US)"},
        {"title": "Smart Cupping Therapy Massager", "niche": "Sağlık & Kişisel Bakım", "views": "6.7M", "likes": "520K", "days_running": 28, "cpa": "$12.00", "margin": "%80", "store_url": "https://recoverysmart.com", "ad_link": "https://tiktok.com/ads/library", "type": "🔥 WINNING PRODUCT (US)"},
        {"title": "Crystal Hair Eraser Exfoliator", "niche": "Güzellik & Kozmetik", "views": "12.4M", "likes": "980K", "days_running": 45, "cpa": "$4.50", "margin": "%85", "store_url": "https://silky-skin-co.com", "ad_link": "https://tiktok.com/ads/library", "type": "🔥 EVERGREEN PRODUCT"}
    ],
    "EU (Avrupa Birliği)": [
        {"title": "Sunset Lamp Bluetooth App Control", "niche": "Ev & Aydınlatma", "views": "3.5M", "likes": "280K", "days_running": 18, "cpa": "€6.20", "margin": "%78", "store_url": "https://solarlamp-eu.com", "ad_link": "https://tiktok.com/ads/library", "type": "🔥 HOT IN EUROPE (EU)"},
        {"title": "Self-Cleaning Pet Grooming Brush", "niche": "Evcil Hayvan", "views": "2.1M", "likes": "190K", "days_running": 11, "cpa": "€4.50", "margin": "%70", "store_url": "https://pawsome-europe.com", "ad_link": "https://facebook.com/ads/library", "type": "👑 WINNING PRODUCT (EU)"},
        {"title": "Orthopedic Chronic Neck Stretcher", "niche": "Medikal & Sağlık", "views": "1.9M", "likes": "130K", "days_running": 9, "cpa": "€8.00", "margin": "%82", "store_url": "https://spinecare-eu.com", "ad_link": "https://facebook.com/ads/library", "type": "📈 VIRAL RISING (EU)"}
    ],
    "GB (İngiltere)": [
        {"title": "Wireless Cat Water Fountain", "niche": "Evcil Hayvan", "views": "1.8M", "likes": "145K", "days_running": 8, "cpa": "$5.20", "margin": "%68", "store_url": "https://happy-paws-co.myshopify.com", "ad_link": "https://facebook.com/ads/library", "type": "📈 VIRAL RISING (UK)"},
        {"title": "Electric Garlic & Vegetable Chopper", "niche": "Mutfak Pratik", "views": "950K", "likes": "68K", "days_running": 5, "cpa": "$3.10", "margin": "%60", "store_url": "https://chefkitchentools.com", "ad_link": "https://facebook.com/ads/library", "type": "📈 VIRAL RISING (UK)"}
    ],
    "CA (Kanada)": [
        {"title": "Anti-Gravity Levitating Humidifier", "niche": "Ev & Dekorasyon", "views": "1.1M", "likes": "95K", "days_running": 10, "cpa": "$9.00", "margin": "%75", "store_url": "https://mysticshophome.com", "ad_link": "
