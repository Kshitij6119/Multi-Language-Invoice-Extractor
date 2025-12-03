
from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
from PIL import Image
import google.generativeai as genai

# Load and configure Gemini API client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_text, image_object, user_prompt):
    """
    Sends input text + invoice image (PIL Image object) + user query to Gemini model
    and returns response.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=[input_text, image_object, user_prompt],
        )
        return response.text
    except Exception as e:
        return f"Error: {e}"


# --- Streamlit interface setup (Applying Dark Mode Theme) ---

# 1. Custom Page Configuration and Dark Theme
st.set_page_config(
    page_title="Invoice Genius",
    layout="wide",
    initial_sidebar_state="auto",
)


# Using a vibrant Teal (#00E676) for primary accents against a dark background
st.markdown("""
    <style>
        /* General Background and Text */
        .stApp {
            background-color: #121212; /* Very dark background */
        }
        
        /* Main Title Styling */
        h1 {
            color: #00E676; /* Vibrant Teal */
            text-align: center;
            font-size: 3rem;
            text-shadow: 0 0 10px rgba(0, 230, 118, 0.5); /* Subtle glow effect */
            margin-bottom: 0.5rem;
        }

        /* Subheader Styling */
        h3 {
            color: #00BCD4; /* Cyan/Aqua accent */
            border-bottom: 2px solid #00E676;
            padding-bottom: 5px;
            margin-top: 1.5rem;
        }

        /* Submit Button Styling */
        .stButton>button {
            background-color: #00E676; /* Teal */
            color: black;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            padding: 10px 20px;
            box-shadow: 0 4px 15px rgba(0, 230, 118, 0.4); /* Stronger shadow/glow */
            transition: all 0.3s ease-in-out;
            width: 100%; /* Make button fill the column */
        }
        .stButton>button:hover {
            background-color: #69F0AE; /* Lighter teal on hover */
            color: #121212;
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(0, 230, 118, 0.6);
        }

        /* Custom Box for Response Area */
        .response-box {
            padding: 20px;
            border-radius: 12px;
            background-color: #1E1E1E; /* Slightly lighter background for the box */
            border: 1px solid #00E676; /* Teal border */
            box-shadow: 0 0 15px rgba(0, 230, 118, 0.2);
            color: white; /* Ensure text is white/light */
        }
        
        /* Style for the Uploaded Image */
        .stImage > img {
            border: 4px solid #00BCD4;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 188, 212, 0.5);
        }
    </style>
""", unsafe_allow_html=True)


# 3. Main Title and Subheader
st.title("🤖 ⚡ Invoice Genius ⚡")
st.markdown(
    """<p style='text-align: center; color: #BBBBBB;'>
    Extract structured data from multi-language invoices instantly.
    </p>""", 
    unsafe_allow_html=True
)
st.markdown("---") # Separator

# --- Layout using Columns ---

# Create two columns: one for input/upload and one for the image preview
col1, col2 = st.columns([1, 1])

# --- Column 1: Input and Upload ---
with col1:
    st.subheader("1. 📸 Invoice Upload")
    
    # File upload widget contained in a stylized container
    with st.container(border=True):
        uploaded_file = st.file_uploader(
            "Upload an invoice image (JPG, JPEG, PNG):", 
            type=["jpg", "jpeg", "png"],
            help="Supported formats: JPG, JPEG, PNG. Max size: 20MB."
        )
    
    st.subheader("2. ❓ Define Query")
    
    # Input for prompt
    user_input = st.text_input(
        "Enter your question for the AI:", 
        key="input",
        placeholder="e.g., What is the invoice number and total amount?"
    )

    st.markdown("---")
    
    # Submit button
    submit_button = st.button("🚀 ANALYZE INVOICE & GET DATA")

# --- Column 2: Image Preview ---
with col2:
    st.subheader("3. 🖼️ Preview & AI Output")
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Invoice", use_column_width=True)
    else:
        st.info("Upload an invoice in Step 1 to see the preview here.")


# --- Processing and Output in an Expander ---

if submit_button:
    if uploaded_file is not None:
        st.markdown("<br>", unsafe_allow_html=True) # Add some space
        
        # Use st.expander to cleanly contain the results, which is a good UI pattern
        with st.expander("⚡ AI Extracted Results", expanded=True):
            with st.spinner("Analyzing invoice with Gemini Vision..."):
                try:
                    prompt = """
                        You are an expert in understanding invoices.
                        Analyze the uploaded invoice image and answer the user's question precisely.
                        Always provide a clear, formatted answer using Markdown for readability (e.g., bullet points or a table).
                    """
                    
                    response = get_gemini_response(prompt, image, user_input) 
                    
                    st.success("Analysis Complete! Find the answer below:")
                    st.markdown(f"**Your Question:** *{user_input}*")
                    st.markdown("---")
                    
                    # Apply the custom response box styling
                    st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        st.error("❌ Please upload an invoice image in Step 1 before analyzing.")
