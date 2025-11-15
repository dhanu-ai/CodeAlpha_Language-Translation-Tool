# 🌍 Hugging Face Translator

A professional translation web application powered by Hugging Face's state-of-the-art translation models. Supports 25+ languages with specialized models for different language pairs.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🚀 **Multiple Translation Models**: Choose from 6 specialized models including MBART, M2M100, NLLB, and OPUS-MT
- 🎯 **Auto-Language Detection**: Automatically detects source language
- 🌐 **25+ Languages**: Support for major world languages including English, Spanish, French, German, Hindi, Chinese, Japanese, Arabic, and more
- 📊 **Smart Model Recommendations**: Built-in guide for choosing the best model for your language pair
- ⚡ **Real-time Translation**: Fast inference using Hugging Face's API
- 🔧 **Debug Mode**: View detailed translation metrics and language codes
- 📋 **One-Click Copy**: Easy copy-to-clipboard functionality
- 💪 **Fallback System**: Automatic fallback to LLM if translation models fail

## 🎯 Supported Models

| Model | Best For | Languages |
|-------|----------|-----------|
| **MBART Large 50** ⭐ | General purpose, casual text | 50+ languages |
| **M2M100 418M** | Asian languages, multilingual chains | 100+ languages |
| **NLLB 200 Distilled** | Rare/low-resource languages | 200+ languages |
| **OPUS MT EN-HI** | English → Hindi (formal) | EN→HI only |
| **OPUS MT HI-EN** | Hindi → English | HI→EN only |
| **Google T5 Small** | Experimental | Limited |

## 📋 Prerequisites

- Python 3.8 or higher
- Hugging Face account and API token

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/hf-translator.git
cd hf-translator
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Get your Hugging Face API Token**
   - Visit [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Create a new token (read permissions are sufficient)
   - Copy the token

4. **Configure your token** (Choose one method)

   **Method 1: Using Streamlit Secrets (Recommended)**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   HF_TOKEN = "your_huggingface_token_here"
   ```

   **Method 2: Environment Variable**
   ```bash
   export HF_TOKEN="your_huggingface_token_here"
   ```

   **Method 3: Enter in UI**
   
   The app will prompt you to enter the token when you first run it.

## 💻 Usage

1. **Run the application**
```bash
streamlit run app.py
```

2. **Open your browser**
   - The app will automatically open at `http://localhost:8501`

3. **Start translating**
   - Enter your text (max 2000 characters)
   - Select source language (or use Auto-detect)
   - Select target language
   - Choose a translation model
   - Click "🚀 Translate"

## 📚 Model Selection Guide

### Best Practices

**For English ↔ Spanish/French/German:**
- Use **MBART Large 50** (best quality)

**For English ↔ Hindi:**
- Use **OPUS MT EN-HI** for English → Hindi
- Use **OPUS MT HI-EN** for Hindi → English
- Use **MBART** for casual/informal text

**For Asian Languages (Chinese, Japanese, Korean):**
- Use **M2M100 418M** or **MBART**

**For Rare Languages:**
- Use **NLLB 200 Distilled** (supports 200+ languages)

### Quick Reference

```
🇺🇸 ↔ 🇪🇸  English-Spanish    → MBART Large 50
🇺🇸 ↔ 🇫🇷  English-French     → MBART Large 50
🇺🇸 → 🇮🇳  English→Hindi      → OPUS MT EN-HI
🇮🇳 → 🇺🇸  Hindi→English      → OPUS MT HI-EN
🇺🇸 ↔ 🇨🇳  English-Chinese    → M2M100 418M
🇺🇸 ↔ 🇯🇵  English-Japanese   → MBART / M2M100
```

## 🔧 Advanced Features

### Debug Mode
Enable "Show debug info" to see:
- Source and target language codes
- Model used
- Text lengths
- Detected language (if auto-detect)

### Enhanced Accuracy Mode
Adds a small delay to potentially improve translation quality.

### Hallucination Detection
Automatically detects when models generate unrelated text and warns you.

## 📂 Project Structure

```
hf-translator/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .streamlit/
    └── secrets.toml      # API token (not in repo)
```

## 🌐 Supported Languages

English, Hindi, French, Spanish, German, Italian, Chinese, Japanese, Arabic, Russian, Portuguese, Korean, Turkish, Dutch, Greek, Hebrew, Thai, Vietnamese, Indonesian, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Urdu, and more!

## 🐛 Troubleshooting

### "No translation generated" error
- Try a different model (MBART or M2M100 recommended)
- Check if your language pair is supported by the selected model
- Verify your internet connection

### Model hallucination (wrong output)
- Use MBART Large 50 or M2M100 418M
- Avoid T5 Small for short texts
- Check the hallucination warning message

### API Token issues
- Ensure your token has read permissions
- Check token is correctly set in secrets.toml
- Verify token hasn't expired

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for providing the translation models and inference API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- All the open-source model creators: Facebook AI (MBART, M2M100, NLLB), Helsinki-NLP (OPUS-MT), Google (T5)


---

**Made with ❤️ using Streamlit and Hugging Face**
