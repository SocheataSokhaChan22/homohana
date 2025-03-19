import streamlit as st
from streamlit.components.v1 import html

def copy_to_clipboard(text):
    js_code = f"""
    <script>
        function copyToClipboard() {{
            navigator.clipboard.writeText("{text}");
            alert("Text copied to clipboard!");
        }}
        copyToClipboard();
    </script>
    """
    html(js_code)

# Streamlit UI
st.title("Khmer Homophone Detection and Correction")

# User input
user_input = st.text_area("Enter a sentence in Khmer:")

if st.button("Process"):
    if user_input.strip():
        # Fixed correction for demonstration
        corrected_text = "សាលារៀននិងមន្ទីរពេទ្យ"
        errors = {"នឹង": "និង"}  # Example correction
        
        st.subheader("Corrected Text:")
        st.code(corrected_text)
        
        if st.button("Copy Corrected Text"):
            copy_to_clipboard(corrected_text)
        
        st.subheader("Identified Homophone Errors:")
        for error, correction in errors.items():
            st.write(f"❌ '{error}' should be replaced with ✅ '{correction}'")
    else:
        st.warning("Please enter a sentence.")
