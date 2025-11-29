# 🚀 Deployment Guide - GitHub & Hosting

This guide will help you deploy your project to GitHub and host it online.

---

## 📦 Part 1: Deploy to GitHub

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **+** icon (top right) → **New repository**
3. Repository name: `prices-predictor-system` (or your choice)
4. Description: `🏠 Production-grade ML pipeline for predicting housing prices using ZenML, MLflow, and Scikit-learn`
5. Choose **Public** (or Private)
6. **DO NOT** check "Initialize with README" (we already have one)
7. Click **Create repository**

### Step 2: Connect Local Repository to GitHub

After creating the repo, GitHub will show you commands. Run these in your terminal:

```bash
cd "c:\Users\suchi\OneDrive\Desktop\python\prices-predictor-system\prices-predictor-system"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/prices-predictor-system.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**Note:** You'll need to authenticate. Use:
- Personal Access Token (recommended)
- Or GitHub CLI

### Step 3: Get Personal Access Token (if needed)

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token
3. Select scopes: `repo` (full control)
4. Copy the token (you'll need it when pushing)

---

## 🌐 Part 2: Hosting Options

### Option 1: GitHub Pages (For Documentation) ✅ Easiest

**Best for:** Hosting project documentation, README, and static content

**Steps:**
1. Go to your GitHub repository
2. Settings → Pages
3. Source: Deploy from a branch
4. Branch: `main` / `docs` folder
5. Save
6. Your site will be at: `https://YOUR_USERNAME.github.io/prices-predictor-system`

**Limitations:** Only static content (HTML, Markdown, etc.)

---

### Option 2: Render (Recommended for ML Services) ⭐

**Best for:** Hosting the ML prediction API

**Steps:**

1. **Sign up at [Render.com](https://render.com)** (free tier available)

2. **Create a Web Service:**
   - New → Web Service
   - Connect your GitHub repository
   - Build command: `pip install -r requirements.txt`
   - Start command: `mlflow models serve -m runs:/<run_id>/model -p $PORT --host 0.0.0.0`

3. **Environment Variables:**
   ```
   PORT=8000
   PYTHON_VERSION=3.8
   ```

4. **Deploy!** Render will automatically deploy on every push.

**Free Tier:**
- 750 hours/month
- Automatic SSL
- Custom domains

---

### Option 3: Railway 🚂

**Best for:** Simple deployment with minimal config

**Steps:**

1. Sign up at [Railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select your repository
4. Railway auto-detects Python
5. Add start command:
   ```bash
   mlflow models serve -m runs:/<run_id>/model -p $PORT
   ```
6. Deploy!

**Free Tier:**
- $5 credit/month
- Pay-as-you-go

---

### Option 4: Heroku ☁️

**Best for:** Traditional hosting (requires credit card for free tier)

**Steps:**

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create prices-predictor-api`
4. Add Procfile:
   ```
   web: mlflow models serve -m runs:/<run_id>/model -p $PORT
   ```
5. Deploy: `git push heroku main`

---

### Option 5: Streamlit Cloud (For Interactive UI) 🎨

**Best for:** Creating an interactive web interface

**Steps:**

1. Create `app.py`:
   ```python
   import streamlit as st
   import mlflow
   import pandas as pd
   
   st.title("🏠 House Price Predictor")
   
   # Load model
   model = mlflow.sklearn.load_model("runs:/<run_id>/model")
   
   # Input form
   # ... create input fields ...
   
   # Predict
   if st.button("Predict"):
       prediction = model.predict(input_data)
       st.success(f"Predicted Price: ${prediction[0]:,.2f}")
   ```

2. Add to requirements.txt: `streamlit`
3. Push to GitHub
4. Go to [share.streamlit.io](https://share.streamlit.io)
5. Deploy from GitHub

---

## 🎯 Recommended Setup

### For Documentation:
- **GitHub Pages** (free, easy)

### For ML API:
- **Render** (free tier, easy setup)
- **Railway** (simple, pay-as-you-go)

### For Interactive Demo:
- **Streamlit Cloud** (free, great for demos)

---

## 📝 Quick Deployment Checklist

- [ ] Repository created on GitHub
- [ ] Code pushed to GitHub
- [ ] README.md updated with your info
- [ ] .gitignore configured
- [ ] Repository description added
- [ ] Topics/tags added (machine-learning, mlops, python)
- [ ] Hosting platform chosen
- [ ] Environment variables set (if needed)
- [ ] Service deployed and tested

---

## 🔧 Post-Deployment

### Update README with Live Links

Add to your README.md:

```markdown
## 🌐 Live Demo

- **API Endpoint:** https://your-app.onrender.com/invocations
- **Documentation:** https://your-username.github.io/prices-predictor-system
- **Interactive Demo:** https://your-app.streamlit.app
```

### Monitor Your Deployment

- Check logs regularly
- Monitor API usage
- Set up alerts (if available)
- Update model periodically

---

## 🆘 Troubleshooting

### GitHub Push Issues

**Authentication Error:**
```bash
# Use Personal Access Token instead of password
git remote set-url origin https://YOUR_TOKEN@github.com/USERNAME/REPO.git
```

**Large Files:**
```bash
# Use Git LFS for large model files
git lfs install
git lfs track "*.pkl"
```

### Hosting Issues

**Port Issues:**
- Use `$PORT` environment variable (Render/Railway)
- Don't hardcode port numbers

**Model Loading:**
- Ensure model files are in repository
- Or use MLflow model registry
- Check model path is correct

**Dependencies:**
- Verify all packages in requirements.txt
- Check Python version compatibility

---

## 📚 Additional Resources

- [GitHub Docs](https://docs.github.com)
- [Render Docs](https://render.com/docs)
- [Railway Docs](https://docs.railway.app)
- [Streamlit Docs](https://docs.streamlit.io)

---

**Good luck with your deployment! 🚀**

