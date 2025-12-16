from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from nltk.tokenize import sent_tokenize
import streamlit as st
import time
import nltk

# For evaluation metrics
from rouge_score import rouge_scorer
from sacrebleu.metrics import BLEU

# Download NLTK data if not exists
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

# Setup device and load model
@st.cache_resource
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base")
    model = AutoModelForSeq2SeqLM.from_pretrained("humarin/chatgpt_paraphraser_on_T5_base").to(device)
    return tokenizer, model, device

tokenizer, model, device = load_model()

def paraphrase_one_sentence(
    question,
    num_beams=5,
    num_return_sequences=1,
    repetition_penalty=2.0,
    no_repeat_ngram_size=2,
    temperature=1.0,
    max_length=128
):
    input_ids = tokenizer(
        f'paraphrase: {question}',
        return_tensors="pt", 
        padding="longest",
        max_length=max_length,
        truncation=True,
    ).input_ids.to(device)
    
    outputs = model.generate(
        input_ids, 
        temperature=temperature, 
        repetition_penalty=repetition_penalty,
        num_return_sequences=num_return_sequences, 
        no_repeat_ngram_size=no_repeat_ngram_size,
        num_beams=num_beams,
        max_length=max_length,
        early_stopping=True
    )

    res = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return res

def paraphrase(paragraph):
    sentences = sent_tokenize(paragraph)
    paraphrased_sentences = []

    for sentence in sentences:
        paraphrased_result = paraphrase_one_sentence(
            sentence, 
            num_beams=3, 
            num_return_sequences=1, 
            max_length=128
        )
        paraphrased_sentences.append(paraphrased_result[0])

    paraphrased_paragraph = " ".join(paraphrased_sentences)
    return paraphrased_paragraph

def calculate_bleu(reference, hypothesis):
    """Calculate BLEU score"""
    bleu = BLEU()
    score = bleu.sentence_score(hypothesis, [reference])
    return score.score

def calculate_rouge(reference, hypothesis):
    """Calculate ROUGE scores"""
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)
    return {
        'rouge1': scores['rouge1'].fmeasure,
        'rouge2': scores['rouge2'].fmeasure,
        'rougeL': scores['rougeL'].fmeasure
    }

# Streamlit UI Configuration
st.set_page_config(
    page_title="AI Paraphraser Pro",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
        /* Main background */
        .main {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        /* Text areas */
        .stTextArea textarea {
            font-size: 16px;
            border-radius: 10px;
            border: 2px solid #667eea;
        }
        
        /* Buttons */
        .stButton>button {
            background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
            color: white;
            font-size: 18px;
            font-weight: bold;
            border-radius: 10px;
            padding: 15px 30px;
            border: none;
            transition: all 0.3s ease;
            width: 100%;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0,114,255,0.4);
        }
        
        /* Headers */
        h1 {
            color: white;
            text-align: center;
            font-size: 3em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 10px;
        }
        
        h2 {
            color: white;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
        }
        
        h3 {
            color: #333;
        }
        
        /* Metric cards */
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin: 10px 0;
            text-align: center;
        }
        
        .metric-title {
            font-size: 14px;
            color: #666;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 28px;
            font-weight: bold;
            color: #0072ff;
        }
        
        .metric-subtitle {
            font-size: 12px;
            color: #999;
            margin-top: 5px;
        }
        
        /* Performance section */
        .performance-header {
            background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            margin: 20px 0 10px 0;
        }
        
        /* Score badges */
        .score-excellent {
            color: #10b981;
            font-weight: bold;
        }
        
        .score-good {
            color: #3b82f6;
            font-weight: bold;
        }
        
        .score-fair {
            color: #f59e0b;
            font-weight: bold;
        }
        
        .score-poor {
            color: #ef4444;
            font-weight: bold;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: rgba(255, 255, 255, 0.95);
        }
        
        /* Info boxes */
        .stAlert {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("🔄 AI Paraphraser Pro")
st.markdown(
    "<p style='text-align: center; color: white; font-size: 1.2em; margin-top: -20px;'>"
    "Transform your text with AI-powered paraphrasing & real-time performance metrics"
    "</p>", 
    unsafe_allow_html=True
)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.info(
        "This app uses the **T5 transformer model** to paraphrase text with "
        "real-time performance evaluation using BLEU and ROUGE metrics."
    )
    
    st.header("⚙️ Model Info")
    st.write(f"**Device:** {device.upper()}")
    if device == "cuda":
        st.write(f"**GPU:** {torch.cuda.get_device_name(0)}")
    st.write("**Model:** humarin/chatgpt_paraphraser_on_T5_base")
    st.write("**Base Architecture:** T5-base")
    
    st.header("📊 Metrics Explained")
    with st.expander("BLEU Score"):
        st.write("""
        **BLEU (Bilingual Evaluation Understudy)**
        - Originally designed for machine translation
        - Measures exact n-gram matches between texts
        - Range: 0-100
        - **For paraphrasing: 10-35 is EXCELLENT!**
        - Why? Because good paraphrase = lots of synonyms = low exact matches
        - ⚠️ High BLEU (>70) = barely paraphrased
        """)
    
    with st.expander("ROUGE Scores"):
        st.write("""
        **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**
        - **ROUGE-1:** Unigram (single word) overlap
        - **ROUGE-2:** Bigram (2-word phrase) overlap  
        - **ROUGE-L:** Longest common subsequence
        - Range: 0-1
        - **For paraphrasing: 0.4-0.7 is ideal**
        - This ensures meaning is preserved while allowing variation
        """)
    
    with st.expander("How to Interpret"):
        st.write("""
        ✅ **Excellent Paraphrase:**
        - BLEU: 10-35 (high word variation!)
        - ROUGE-1: 0.4-0.7 (meaning preserved)
        - ROUGE-L: 0.35-0.7 (structure maintained)
        
        ✅ **Very Good Paraphrase:**
        - BLEU: 20-50
        - ROUGE-1: 0.5-0.8
        
        ⚠️ **Too Similar (barely paraphrased):**
        - BLEU: >75
        - ROUGE-1: >0.9
        
        ⚠️ **Needs Review (verify meaning):**
        - ROUGE-1: <0.25
        - ROUGE-L: <0.2
        
        **Remember:** Low BLEU + Moderate ROUGE = Perfect! 🎯
        """)

# Main content
st.markdown("<br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.header("📝 Original Text")
    input_text = st.text_area(
        "Enter your text here:", 
        height=350,
        placeholder="Type or paste your text here...",
        help="Enter the text you want to paraphrase"
    )

with col2:
    st.header("✨ Paraphrased Text")
    
    # Paraphrase button
    if st.button("🚀 Paraphrase Now", use_container_width=True):
        if input_text:
            with st.spinner("🔄 Paraphrasing in progress..."):
                # Start timing
                start_time = time.time()
                
                # Paraphrase the text
                paraphrased_text = paraphrase(input_text)
                
                # Calculate elapsed time
                elapsed_time = time.time() - start_time
                
                # Calculate metrics
                bleu_score = calculate_bleu(input_text, paraphrased_text)
                rouge_scores = calculate_rouge(input_text, paraphrased_text)
            
            # Success message
            st.success("✅ Paraphrasing complete!")
            
            # Display paraphrased text
            st.text_area(
                "Result:", 
                value=paraphrased_text, 
                height=350,
                help="Your paraphrased text"
            )
            
            # Store in session state for later use
            st.session_state.last_original = input_text
            st.session_state.last_paraphrased = paraphrased_text
            st.session_state.last_metrics = {
                'time': elapsed_time,
                'bleu': bleu_score,
                'rouge': rouge_scores,
                'original_words': len(input_text.split()),
                'paraphrased_words': len(paraphrased_text.split())
            }
        else:
            st.warning("⚠️ Please enter text in the left column.")

# Display performance metrics if available
if 'last_metrics' in st.session_state:
    metrics = st.session_state.last_metrics
    
    # Performance header
    st.markdown(
        '<div class="performance-header">📊 Performance Metrics & Quality Analysis</div>', 
        unsafe_allow_html=True
    )
    
    # Row 1: Basic metrics
    col_a, col_b, col_c, col_d = st.columns(4)
    
    with col_a:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">⏱️ INFERENCE TIME</div>
            <div class="metric-value">{metrics['time']:.2f}s</div>
            <div class="metric-subtitle">Processing time</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_b:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📝 ORIGINAL WORDS</div>
            <div class="metric-value">{metrics['original_words']}</div>
            <div class="metric-subtitle">Word count</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_c:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">✨ PARAPHRASED WORDS</div>
            <div class="metric-value">{metrics['paraphrased_words']}</div>
            <div class="metric-subtitle">Word count</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_d:
        word_diff = metrics['paraphrased_words'] - metrics['original_words']
        diff_percent = (word_diff / metrics['original_words'] * 100) if metrics['original_words'] > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📊 WORD CHANGE</div>
            <div class="metric-value">{diff_percent:+.1f}%</div>
            <div class="metric-subtitle">Length variation</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Row 2: Quality metrics
    st.subheader("🎯 Quality Metrics")
    
    col_e, col_f, col_g, col_h = st.columns(4)
    
    # Helper function to get score class
    def get_bleu_class(score):
        if score > 70: return "score-poor"  # Too similar
        elif score >= 30: return "score-excellent"  # Perfect
        elif score >= 20: return "score-good"  # Good
        else: return "score-fair"  # Acceptable
    
    def get_rouge_class(score):
        if score > 0.9: return "score-poor"  # Too similar
        elif score >= 0.5: return "score-excellent"  # Perfect
        elif score >= 0.3: return "score-good"  # Good
        else: return "score-fair"  # Acceptable
    
    bleu_class = get_bleu_class(metrics['bleu'])
    rouge1_class = get_rouge_class(metrics['rouge']['rouge1'])
    rouge2_class = get_rouge_class(metrics['rouge']['rouge2'])
    rougeL_class = get_rouge_class(metrics['rouge']['rougeL'])
    
    with col_e:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">🎯 BLEU SCORE</div>
            <div class="metric-value {bleu_class}">{metrics['bleu']:.2f}</div>
            <div class="metric-subtitle">Similarity score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_f:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📈 ROUGE-1</div>
            <div class="metric-value {rouge1_class}">{metrics['rouge']['rouge1']:.4f}</div>
            <div class="metric-subtitle">Unigram overlap</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_g:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📈 ROUGE-2</div>
            <div class="metric-value {rouge2_class}">{metrics['rouge']['rouge2']:.4f}</div>
            <div class="metric-subtitle">Bigram overlap</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">📈 ROUGE-L</div>
            <div class="metric-value {rougeL_class}">{metrics['rouge']['rougeL']:.4f}</div>
            <div class="metric-subtitle">Longest common seq</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quality assessment
    st.subheader("✅ Quality Assessment")
    
    # Determine overall quality with improved logic
    bleu = metrics['bleu']
    rouge1 = metrics['rouge']['rouge1']
    rouge2 = metrics['rouge']['rouge2']
    rougeL = metrics['rouge']['rougeL']
    
    # NEW LOGIC: Low BLEU + Moderate ROUGE = Excellent paraphrase!
    # This means: lots of word variation (low BLEU) but meaning preserved (moderate ROUGE)
    
    if bleu > 75 or rouge1 > 0.9:
        # Too similar - barely paraphrased
        quality = "Too Similar"
        quality_icon = "⚠️"
        quality_color = "#f59e0b"
        quality_msg = "The paraphrased text is very similar to the original. More word variation would improve quality."
    
    elif rouge1 < 0.25 or rougeL < 0.2:
        # Meaning might be lost - too different
        quality = "Needs Review"
        quality_icon = "⚠️"
        quality_color = "#ef4444"
        quality_msg = "Low semantic overlap detected. Please verify the paraphrased text preserves the original meaning."
    
    elif 10 <= bleu <= 35 and 0.4 <= rouge1 <= 0.7 and rougeL >= 0.35:
        # EXCELLENT: Low BLEU (good variation) + Moderate ROUGE (meaning preserved)
        quality = "Excellent"
        quality_icon = "🌟"
        quality_color = "#10b981"
        quality_msg = "Outstanding paraphrase! High word variation while preserving meaning and structure. Professional quality."
    
    elif 20 <= bleu <= 50 and 0.5 <= rouge1 <= 0.8:
        # VERY GOOD: Moderate BLEU + Good ROUGE
        quality = "Very Good"
        quality_icon = "✅"
        quality_color = "#059669"
        quality_msg = "Very good paraphrase! Effective rephrasing with strong meaning preservation."
    
    elif rouge1 >= 0.4 and rougeL >= 0.3:
        # GOOD: Decent overlap, meaning likely preserved
        quality = "Good"
        quality_icon = "👍"
        quality_color = "#3b82f6"
        quality_msg = "Good paraphrase! The text has been rephrased while preserving the original meaning."
    
    else:
        # FAIR: Acceptable but could be better
        quality = "Fair"
        quality_icon = "ℹ️"
        quality_color = "#6366f1"
        quality_msg = "Acceptable paraphrase. Consider reviewing to ensure meaning is preserved."
    
    st.markdown(f"""
    <div style="background: {quality_color}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
        <div style="font-size: 48px; margin-bottom: 10px;">{quality_icon}</div>
        <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">Quality: {quality}</div>
        <div style="font-size: 16px;">{quality_msg}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed breakdown
    with st.expander("📋 Detailed Analysis"):
        st.write("**Interpretation:**")
        st.write("*Note: For paraphrasing, low BLEU with moderate ROUGE is actually IDEAL!*")
        st.write("")
        
        # BLEU interpretation - UPDATED LOGIC
        if bleu > 75:
            st.write(f"- 🔴 **BLEU ({bleu:.2f}):** Too high - paraphrase is almost identical to original (barely rephrased)")
        elif 35 < bleu <= 75:
            st.write(f"- � **BLEU ({bleu:.2f}):** Moderate-high - some variation but could use more rephrasing")
        elif 20 <= bleu <= 35:
            st.write(f"- 🟢 **BLEU ({bleu:.2f}):** Good range - balanced similarity and variation")
        elif 10 <= bleu < 20:
            st.write(f"- � **BLEU ({bleu:.2f}):** Excellent - high word variation (this is GOOD for paraphrasing!)")
        else:
            st.write(f"- � **BLEU ({bleu:.2f}):** Very low - verify meaning is preserved, but variation is great")
        
        # ROUGE-1 interpretation - UPDATED LOGIC
        if rouge1 > 0.9:
            st.write(f"- 🔴 **ROUGE-1 ({rouge1:.4f}):** Too high - very little word variation")
        elif rouge1 >= 0.7:
            st.write(f"- 🟡 **ROUGE-1 ({rouge1:.4f}):** High - meaning preserved but limited variation")
        elif rouge1 >= 0.4:
            st.write(f"- 🟢 **ROUGE-1 ({rouge1:.4f}):** Optimal - excellent balance of preservation and variation")
        elif rouge1 >= 0.25:
            st.write(f"- 🟡 **ROUGE-1 ({rouge1:.4f}):** Moderate - verify meaning is preserved")
        else:
            st.write(f"- 🔴 **ROUGE-1 ({rouge1:.4f}):** Low - meaning might be significantly changed")
        
        # ROUGE-L interpretation
        rougeL = metrics['rouge']['rougeL']
        if rougeL >= 0.5:
            st.write(f"- 🟢 **ROUGE-L ({rougeL:.4f}):** Excellent structural preservation")
        elif rougeL >= 0.35:
            st.write(f"- 🟢 **ROUGE-L ({rougeL:.4f}):** Good structural similarity")
        elif rougeL >= 0.2:
            st.write(f"- 🟡 **ROUGE-L ({rougeL:.4f}):** Moderate structural changes")
        else:
            st.write(f"- � **ROUGE-L ({rougeL:.4f}):** Significant structural changes")
        
        st.write("")
        st.write("**Key Insight:**")
        st.write("🎯 *A good paraphrase should have LOW BLEU (10-35) and MODERATE ROUGE-1 (0.4-0.7)*")
        st.write("   → This means: lots of synonyms and restructuring, but meaning preserved!")
        
        # Performance
        st.write("")
        if metrics['time'] < 1:
            st.write(f"- ⚡ **Speed:** Excellent ({metrics['time']:.2f}s)")
        elif metrics['time'] < 3:
            st.write(f"- 🟢 **Speed:** Good ({metrics['time']:.2f}s)")
        else:
            st.write(f"- 🟡 **Speed:** Slow ({metrics['time']:.2f}s) - consider optimizing")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: white; font-size: 0.9em;'>"
    "Made with ❤️ using Streamlit & Hugging Face Transformers"
    "</p>", 
    unsafe_allow_html=True
)
