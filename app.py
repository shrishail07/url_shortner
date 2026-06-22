import streamlit as st
import requests

# Set up page configuration
st.set_page_config(page_title="URL Shortener", page_icon="🔗", layout="centered")

# Title and description
st.title("🔗 Quick URL Shortener")
st.write("Paste your long, messy links below to turn them into clean, shareable short URLs.")

st.markdown("---")

# Using a Streamlit Form to bundle inputs and prevent the app 
# from refreshing on every single keystroke.
with st.form(key="shortener_form"):
    long_url = st.text_input(
        "Enter Long URL:", 
        placeholder="https://example.com/some/very/long/and/complicated/path"
    )
    submit_button = st.form_submit_button(label="Shorten URL", type="primary")

# Logic triggers only after clicking the form's submit button
if submit_button:
    # Clean up whitespace from the input string
    long_url = long_url.strip()
    
    if not long_url:
        st.warning("Please enter a URL first!")
    elif not long_url.startswith(("http://", "https://")):
        st.error("Invalid URL. Make sure it starts with http:// or https://")
    else:
        with st.spinner("Shortening your link..."):
            try:
                # Making a call to the TinyURL API (API Concept)
                api_url = f"http://tinyurl.com/api-create.php?url={long_url}"
                response = requests.get(api_url, timeout=10)
                
                # Check if the API request was successful
                if response.status_code == 200:
                    short_url = response.text # The API returns the plain text short link
                    
                    st.success("Your short link is ready!")
                    
                    # Display the short URL inside a code component for built-in easy copying
                    st.code(short_url, language="text")
                    st.info("💡 Click the copy icon in the top-right corner of the box above to copy your link.")
                else:
                    st.error("Failed to shorten URL. The service might be temporarily unavailable.")
            
            except requests.exceptions.RequestException as e:
                st.error("A network error occurred. Please check your connection and try again.")
