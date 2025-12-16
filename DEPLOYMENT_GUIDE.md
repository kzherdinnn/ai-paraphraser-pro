# 🚀 Deploy ke Streamlit Cloud - Panduan Lengkap

## 📋 Persiapan Files

File yang diperlukan (✅ sudah ada):
- ✅ `web_app_enhanced.py` (atau rename jadi `app.py`)
- ✅ `requirements.txt` (dependencies)
- ✅ `.streamlit/config.toml` (konfigurasi)

---

## 🎯 Langkah-Langkah Deploy

### **Option 1: Deploy via GitHub (Recommended)**

#### **Step 1: Prepare GitHub Repository**

1. **Buka GitHub** → https://github.com
2. **Create New Repository**
   - Name: `paraphraser-app` (atau nama lain)
   - Public atau Private (terserah)
   - ✅ Initialize with README

#### **Step 2: Upload Files ke GitHub**

Upload file-file ini:
```
paraphraser-app/
├── app.py                    # Rename dari web_app_enhanced.py
├── requirements.txt          # ✅ Sudah ada
├── .streamlit/
│   └── config.toml          # ✅ Sudah ada
└── README.md                # Optional
```

**Cara Upload:**
1. Klik **Add file** → **Upload files**
2. Drag & drop:
   - `web_app_enhanced.py` (rename jadi `app.py`)
   - `requirements.txt`
   - Folder `.streamlit` dengan `config.toml`
3. Commit changes

#### **Step 3: Deploy ke Streamlit Cloud**

1. **Buka** → https://share.streamlit.io/
2. **Sign in** dengan GitHub account
3. **Click "New app"**
4. **Fill form:**
   - Repository: `your-username/paraphraser-app`
   - Branch: `main`
   - Main file path: `app.py`
5. **Click "Deploy"**

#### **Step 4: Wait & Done!**

- Streamlit akan install dependencies (~2-5 menit)
- Setelah selesai, app akan running!
- URL: `https://your-app-name.streamlit.app`

---

### **Option 2: Deploy via Streamlit CLI (Local)**

Jika ingin test lokal dulu:

```bash
# 1. Install streamlit
pip install streamlit

# 2. Run app
streamlit run web_app_enhanced.py

# 3. App akan buka di http://localhost:8501
```

---

## 📝 File Setup Commands

Jika belum ada file, buat dengan command ini:

### **1. Rename web_app_enhanced.py → app.py**
```bash
cd c:\Users\herdinkz\OneDrive\Videos\Paraphraser_app
copy web_app_enhanced.py app.py
```

### **2. Verify requirements.txt**
File sudah ada di folder. Isinya:
```
transformers==4.35.0
torch==2.1.0
nltk==3.8.1
streamlit==1.28.0
rouge-score==0.1.2
sacrebleu==2.3.1
```

### **3. Verify .streamlit/config.toml**
File sudah ada di folder `.streamlit/config.toml`

---

## 🎨 Customization (Optional)

### **Update App Title**
Edit `app.py`, cari:
```python
st.set_page_config(
    page_title="AI Paraphraser Pro",  # Ganti ini
    page_icon="🔄",
    ...
)
```

### **Update Theme**
Edit `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#0072ff"  # Ganti warna
backgroundColor = "#ffffff"
```

---

## ⚠️ Troubleshooting

### **Error: Module not found**
- Cek `requirements.txt` sudah lengkap
- Restart deployment di Streamlit Cloud

### **App too slow**
- Normal untuk first load (download model ~250MB)
- Setelah cache, akan cepat

### **Out of memory**
- Streamlit Cloud free tier: 1GB RAM
- Model T5-base butuh ~500MB
- Sudah cukup, tapi jangan buka banyak tabs

---

## 📊 Streamlit Cloud Limits (Free Tier)

| Resource | Limit |
|----------|-------|
| RAM | 1 GB |
| CPU | Shared |
| Storage | Limited |
| Apps | Unlimited |
| Users | Unlimited |
| Uptime | Always on |

---

## 🎯 Quick Deploy Checklist

- [ ] Rename `web_app_enhanced.py` → `app.py`
- [ ] Upload ke GitHub repository
- [ ] Pastikan `requirements.txt` ada
- [ ] Pastikan `.streamlit/config.toml` ada
- [ ] Deploy di https://share.streamlit.io/
- [ ] Wait for build (~5 mins)
- [ ] ✅ Done! Share URL

---

## 🔗 URLs Penting

- **Streamlit Cloud:** https://share.streamlit.io/
- **Docs:** https://docs.streamlit.io/streamlit-community-cloud
- **GitHub:** https://github.com/

---

## 🎉 After Deployment

Setelah deploy, Anda akan dapat:
- ✅ Public URL (e.g., `https://paraphraser.streamlit.app`)
- ✅ Auto-update ketika push ke GitHub
- ✅ Free hosting selamanya
- ✅ HTTPS & SSL included
- ✅ Analytics & monitoring

---

**Made with ❤️ - Ready to deploy!**
