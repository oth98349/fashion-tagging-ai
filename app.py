import streamlit as st
import openai
from PIL import Image
import os

# Load OpenAI API key from environment variable
import streamlit as st
openai.api_key = st.secrets["OPENAI_API_KEY"]


def fashion_ai(image, reference_text):
    prompt = f"""
You are a professional fashion product describer. Based on this product image and its reference name: "{reference_text}", generate the following in structured JSON format:
1. Main category
2. Subcategory/style
3. Primary color(s)
4. Material (if guessable visually)
5. Notable visual details
6. Fit/silhouette
7. Occasion/style
8. Suggested product title (max 10 words)
9. Suggested product description (2-3 lines, modern retail tone)
10. Tags (list of keywords)

Describe only what can be seen clearly in the image. Avoid vague words like “trendy” and do not invent unobservable attributes.
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert fashion product describer."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content']

# Streamlit UI
st.set_page_config(page_title="Fashion Tagging AI")

st.title("👗 Fashion Tagging AI")
st.markdown("Upload a fashion product image and enter a product name to generate structured tags and a modern description.")

uploaded_image = st.file_uploader("📸 Upload your product image", type=["jpg", "jpeg", "png"])
product_name = st.text_input("📝 Product name or reference", placeholder="Ex: Beige satin dress with V-neck")

if st.button("✨ Generate Tags"):
    if uploaded_image and product_name:
        image = Image.open(uploaded_image)
        with st.spinner("Generating..."):
            result = fashion_ai(image, product_name)
        st.text_area("📦 AI Output: Structured JSON", value=result, height=400)
    else:
        st.warning("Please upload an image and enter a product name.")

