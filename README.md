# 🔄 AI Paraphraser Pro

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

Transform your text with AI-powered paraphrasing and real-time performance metrics.

## ✨ Features

- 🤖 **T5 Transformer Model** - State-of-the-art paraphrasing
- 📊 **Real-time Metrics** - BLEU & ROUGE scores with quality assessment
- 🎨 **Beautiful UI** - Modern gradient design with animations
- 🚀 **Fast Inference** - Optimized for performance
- 📈 **Quality Analysis** - Color-coded indicators and detailed breakdown
- 💾 **Session Memory** - Metrics persist across paraphrases

## 🎯 Quality Assessment

The app uses intelligent quality assessment that understands paraphrasing:

- **🌟 Excellent** - BLEU 10-35, ROUGE-1 0.4-0.7 (high variation, meaning preserved)
- **✅ Very Good** - BLEU 20-50, ROUGE-1 0.5-0.8
- **👍 Good** - ROUGE-1 ≥0.4, ROUGE-L ≥0.3
- **⚠️ Too Similar** - BLEU >75 (barely paraphrased)
- **⚠️ Needs Review** - ROUGE-1 <0.25 (meaning might be lost)

## 🚀 Quick Start

### Online (Recommended)
Visit: [https://your-app-url.streamlit.app](https://your-app-url.streamlit.app)

### Local Installation

```bash
# Clone repository
git clone https://github.com/your-username/paraphraser-app.git
cd paraphraser-app

# Install dependencies
pip install -r requirements.txt

# Run app
streamlit run app.py
```

## 📊 Metrics Explained

### BLEU Score
- Measures exact n-gram matches
- **For paraphrasing: 10-35 is excellent!**
- Low BLEU = lots of synonyms = good paraphrase

### ROUGE Scores
- **ROUGE-1:** Unigram overlap (ideal: 0.4-0.7)
- **ROUGE-2:** Bigram overlap
- **ROUGE-L:** Longest common subsequence

**Key Insight:** Low BLEU + Moderate ROUGE = Perfect paraphrase! 🎯

## 🛠️ Tech Stack

- **Framework:** Streamlit
- **Model:** [humarin/chatgpt_paraphraser_on_T5_base](https://huggingface.co/humarin/chatgpt_paraphraser_on_T5_base)
- **Evaluation:** BLEU (sacrebleu), ROUGE (rouge-score)
- **NLP:** Transformers, PyTorch, NLTK

## 📸 Screenshots

### Main Interface
![Main UI](https://via.placeholder.com/800x400?text=Upload+your+screenshot+here)

### Performance Metrics
![Metrics](https://via.placeholder.com/800x400?text=Upload+your+screenshot+here)

## 🎨 Customization

Edit `.streamlit/config.toml` to change theme:

```toml
[theme]
primaryColor = "#0072ff"
backgroundColor = "#ffffff"
```

## 📝 Example Usage

**Input:**
```
Regular physical activity is essential for maintaining good health.
```

**Output:**
```
Maintaining a healthy lifestyle requires regular physical activity.
```

**Metrics:**
- BLEU: 17.36 → 🟢 Excellent variation
- ROUGE-1: 0.5079 → 🟢 Meaning preserved
- Quality: 🌟 Excellent

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for the T5 model
- [Streamlit](https://streamlit.io/) for the amazing framework

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/your-username/paraphraser-app](https://github.com/your-username/paraphraser-app)

---

**Made with ❤️ using Streamlit & Hugging Face Transformers**
