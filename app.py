import streamlit as st
from PIL import Image
from openai import OpenAI

# 🔐 Charge ta clé API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 🔁 Limites d'utilisation
MAX_FREE_TRIALS = 5

if "usage_count" not in st.session_state:
    st.session_state.usage_count = 0

# ⚙️ Fonction principale d'IA
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

    chat = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an expert fashion product describer."},
            {"role": "user", "content": prompt}
        ]
    )
    return chat.choices[0].message.content

# 🖼️ Interface Streamlit
st.set_page_config(page_title="Fashion Tagging AI")
st.title("👗 Fashion Tagging AI")
st.markdown("Upload a fashion product image and enter a product name to generate structured tags and a modern description.")

uploaded_image = st.file_uploader("📸 Upload your product image", type=["jpg", "jpeg", "png"])
product_name = st.text_input("📝 Product name or reference", placeholder="Ex: Beige satin dress with V-neck")

# 💰 Message quota
remaining_uses = MAX_FREE_TRIALS - st.session_state.usage_count
if remaining_uses > 0:
    st.info(f"🧮 {remaining_uses} free generation{'s' if remaining_uses > 1 else ''} left.")
else:
    st.warning("🚫 You have reached your 5 free tries. Please create an account or purchase more credits.")

# 🧠 Bouton IA
if st.button("✨ Generate Tags"):
    if uploaded_image and product_name:
        if st.session_state.usage_count < MAX_FREE_TRIALS:
            image = Image.open(uploaded_image)
            with st.spinner("Generating..."):
                result = fashion_ai(image, product_name)
            st.session_state.usage_count += 1
            st.text_area("📦 AI Output: Structured JSON", value=result, height=400)
        else:
            st.error("🚫 Limit reached. Please upgrade or wait for more credits.")
    else:
        st.warning("Please upload an image and enter a product name.")
