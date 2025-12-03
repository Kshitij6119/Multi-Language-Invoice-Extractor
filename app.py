import streamlit as st
import os
from PIL import Image
import google.generativeai as genai  # <--- FIXED IMPORT
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API (Standard Method)
# Ensure GOOGLE_API_KEY is in your .env file or Streamlit secrets
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, image_object, user_prompt):
    """
    Sends input text + invoice image (PIL Image object) + user query to Gemini model
    """
    try:
        # FIXED: Use the GenerativeModel class from the standard SDK
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # The standard SDK handles the list of contents automatically
        response = model.generate_content([input_text, image_object, user_prompt])
        return response.text
    except Exception as e:
        return f"Error: {e}"


# --- Streamlit interface setup (Applying Dark Mode Theme) ---

# 1. Custom Page Configuration
st.set_page_config(
    page_title="Invoice Genius",
    layout="wide",
    initial_sidebar_state="auto",
)

# 2. Custom CSS
st.markdown("""
    <style>
        .stApp { background-color: #121212; }
        h1 {
            color: #00E676; 
            text-align: center;
            font-size: 3rem;
            text-shadow: 0 0 10px rgba(0, 230, 118, 0.5); 
            margin-bottom: 0.5rem;
        }
        h3 {
            color: #00BCD4; 
            border-bottom: 2px solid #00E676;
            padding-bottom: 5px;
            margin-top: 1.5rem;
        }
        .stButton>button {
            background-color: #00E676; 
            color: black;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            box-shadow: 0 4px 15px rgba(0, 230, 118, 0.4); 
            width: 100%; 
        }
        .stButton>button:hover {
            background-color: #69F0AE; 
            color: #121212;
            transform: scale(1.02);
        }
        .response-box {
            padding: 20px;
            border-radius: 12px;
            background-color: #1E1E1E; 
            border: 1px solid #00E676; 
            color: white; 
        }
        .stImage > img {
            border: 4px solid #00BCD4;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)


# 3. Main UI
st.title("🤖 ⚡ Invoice Genius ⚡")
st.markdown(
    """<p style='text-align: center; color: #BBBBBB;'>
    Extract structured data from multi-language invoices instantly.
    </p>""", 
    unsafe_allow_html=True
)
st.markdown("---") 

col1, col2 = st.columns([1, 1])

# Column 1: Inputs
with col1:
    st.subheader("1. 📸 Invoice Upload")
    with st.container(border=True):
        uploaded_file = st.file_uploader(
            "Upload an invoice image (JPG, JPEG, PNG):", 
            type=["jpg", "jpeg", "png"]
        )
    
    st.subheader("2. ❓ Define Query")
    user_input = st.text_input(
        "Enter your question for the AI:", 
        key="input",
        placeholder="e.g., What is the invoice number and total amount?"
    )
    st.markdown("---")
    submit_button = st.button("🚀 ANALYZE INVOICE & GET DATA")

# Column 2: Preview
with col2:
    st.subheader("3. 🖼️ Preview & AI Output")
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice", use_column_width=True)
    else:
        st.info("Upload an invoice to see preview.")


# Processing
if submit_button:
    if uploaded_file is not None:
        st.markdown("<br>", unsafe_allow_html=True) 
        
        with st.expander("⚡ AI Extracted Results", expanded=True):
            with st.spinner("Analyzing invoice with Gemini Vision..."):
                try:
                    prompt = """
                        You are an expert in understanding invoices.
                        Analyze the uploaded invoice image and answer the user's question precisely.
                        Format the output in Markdown.
                    """
                    
                    response = get_gemini_response(prompt, image, user_input) 
                    
                    st.success("Analysis Complete!")
                    st.markdown(f"**Question:** *{user_input}*")
                    st.markdown("---")
                    st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.error("❌ Please upload an invoice image first.")
