import streamlit as st
import requests
import validators
import pandas as pd  # For handling data as DataFrame

# Set the Heroku URL for the Flask app
FLASK_URL = "https://vignesh-flask2-d8b64f2c64ed.herokuapp.com"

# Function to calculate and display combinations
def display_hex_combinations():
    st.markdown("## Hexadecimal Combinations")
    st.markdown("""
    In this URL shortener, we generate short codes using hexadecimal characters (0-9, a-f). Each character can be one of 16 values, which gives us a large number of possible combinations.""")
    
    st.write(f"**16^7**: {16**7:,} unique combinations (handles up to 268 million URLs)")
    st.write(f"**16^6**: {16**6:,} unique combinations (handles up to 16 million URLs)")
    st.write(f"**16^5**: {16**5:,} unique combinations (handles up to 1 million URLs)")
    st.write(f"**16^4**: {16**4:,} unique combinations (handles up to 65,536 URLs :) ")

def main():
    st.markdown("<h1 style='text-align: center;'>🔗 URL Shortener</h1>", unsafe_allow_html=True)

    

    menu = st.radio(
        "",
        ["Home", "Retrieve"],
        horizontal=True,
        index=0,
        key="main_menu"
    )

    # Home page: URL Shortener
    if menu == "Home":
        st.title("🔗 URL Shortener")
        with st.form("shorten_form"):
            original_url = st.text_input("Enter the URL to shorten:")
            submitted = st.form_submit_button("Shorten URL")

        if submitted:
            if not original_url:
                st.error("Please enter a URL.")
            elif not validators.url(original_url):
                st.error("Invalid URL. Please enter a valid URL (e.g., https://example.com).")
            else:
                # Send request to Flask app to shorten the URL
                try:
                    response = requests.post(
                        f"{FLASK_URL}/shorten",
                        json={"original_url": original_url}
                    )

                    if response.status_code == 201:
                        data = response.json()
                        short_code = data.get("short_code")
                        short_url = f"{FLASK_URL}/short/{short_code}"

                        # If the URL already exists, display a message saying so
                        if data.get("already_exists"):
                            st.info(f"This URL has already been shortened: {short_url}")
                        else:
                            st.success(f"Short URL created: {short_url}")
                    else:
                        st.error(f"Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Failed to connect to Flask app: {e}")

    # Retrieve page: Display existing URL mappings in a table
    elif menu == "Retrieve":
        st.title("🔍 Retrieve URL Mappings")
        try:
            response = requests.get(f"{FLASK_URL}/list_urls")
            if response.status_code == 200:
                urls = response.json()
                if urls:
                    # Convert the list of URLs to a pandas DataFrame for a nice table view
                    df = pd.DataFrame(urls)
                    df['short_url'] = FLASK_URL + '/short/' + df['short_code']
                    df = df[['short_url', 'original_url', 'click_count']]  # Rearrange columns
                    df.columns = ['Short URL', 'Original URL', 'Click Count']  # Rename columns

                    # Display the DataFrame as a table
                    st.dataframe(df)
                else:
                    st.info("No URL mappings found.")
            else:
                st.error(f"Error fetching URLs: {response.status_code}")
        except Exception as e:
            st.error(f"Failed to connect to Flask app: {e}")
# Display hexadecimal combinations
    display_hex_combinations()
if __name__ == "__main__":
    main()
