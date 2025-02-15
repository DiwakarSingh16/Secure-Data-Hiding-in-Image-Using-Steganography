import streamlit as st
from stegano.lsb import hide, reveal
from PIL import Image
import io

def set_background():
    page_bg = """
    <style>
    body {
        background-color: #f4f4f4;
    }
    .stApp {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f4f4f4;
        color: grey;
        text-align: center;
        padding: 10px;
    }
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

def encode_message(image, secret_message, password):
    encrypted_message = f"{password}:{secret_message}"
    encoded_image = hide(image, encrypted_message)
    img_bytes = io.BytesIO()
    encoded_image.save(img_bytes, format="PNG")
    return img_bytes.getvalue()

def decode_message(encoded_image, password_attempt):
    hidden_data = reveal(encoded_image)
    if hidden_data:
        stored_password, secret_message = hidden_data.split(":", 1)
        if password_attempt == stored_password:
            return secret_message
        else:
            return "Incorrect password!"
    else:
        return "No hidden message found!"

def main():
    set_background()
    st.title("🖼️ Secure Image Steganography App")
    st.markdown("""<p style='text-align: center; font-size:18px; color: grey;'>
                Hide and reveal messages inside images securely with password protection!
                </p>""", unsafe_allow_html=True)
    
   
    
    option = st.sidebar.radio("Choose an action:", ["Encode", "Decode"])
    
    if option == "Encode":
        st.header("🔐 Hide a Message in an Image")
        uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Image", use_column_width=True)
            secret_message = st.text_area("Enter your secret message:")
            password = st.text_input("Set a password:", type="password")
            
            if st.button("Encode Message"):
                if secret_message and password:
                    encoded_image_bytes = encode_message(image, secret_message, password)
                    st.success("Message encoded successfully!")
                    st.download_button("Download Encoded Image", encoded_image_bytes, "encoded_image.png", "image/png")
                else:
                    st.warning("Please enter both a message and a password.")
    
    elif option == "Decode":
        st.header("🔓 Reveal a Message from an Image")
        encoded_file = st.file_uploader("Upload an encoded image", type=["png"])
        
        if encoded_file is not None:
            encoded_image = Image.open(encoded_file)
            st.image(encoded_image, caption="Encoded Image", use_column_width=True)
            password_attempt = st.text_input("Enter the password to decode:", type="password")
            
            if st.button("Decode Message"):
                try:
                    result = decode_message(encoded_image, password_attempt)
                    if result == "Incorrect password!":
                        st.error(result)
                    elif result == "No hidden message found!":
                        st.warning(result)
                    else:
                        st.success("Hidden Message:")
                        st.code(result)
                except Exception as e:
                    st.error("Error decoding message: " + str(e))
    
    # Footer with developer information
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>Developed by <b>Diwakar Singh</b> | <a href="https://www.linkedin.com/in/diwakar-singh-328981293/">   LinkedIn</a></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()