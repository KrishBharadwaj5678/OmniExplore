import wikipedia
import streamlit as st

# Function to get language code from selection
def get_language_code(language):
    return language.split(":")[0].strip()

# Set page configuration
st.set_page_config(
    page_title="Omni Explore",
    page_icon="./assets/icons/omni.png",
    menu_items={
        "About": "OmniExplore offers limitless discovery! Input any topic and specify your language to access comprehensive summaries. Uncover knowledge effortlessly."
    }
)

# Main content
st.markdown("## :orange[Explore the World of Information]")

# Get all Wikipedia languages
getAllLang = wikipedia.languages()
lang = [f"{code}: {getAllLang[code]}" for code in getAllLang]

# User input: language and topic
language = st.selectbox("Please select your language", lang,index=lang.index("en: English"))
topic = st.text_input("Type your topic here", placeholder="e.g. who is elon musk", help="Abbreviations are prohibited! eg. NASA")

# Search button
btn = st.button("Search")

if btn:
    try:
        with st.spinner("Loading..."):
            # Set Wikipedia language
            wikipedia.set_lang(get_language_code(language))

            # Fetch Wikipedia page for the topic
            page = wikipedia.page(topic)

            # Display up to 5 relevant images related to the topic
            images_displayed = 0
            for img in page.images:
                # Check if the image URL contains any part of the topic's title
                if any(word.lower() in img.lower() for word in topic.split()):
                    st.image(img, caption=f"Image {images_displayed + 1}", width=300)
                    images_displayed += 1
                    if images_displayed >= 5:
                        break

            # Display Wikipedia summary
            st.write(wikipedia.summary(topic))
    except wikipedia.exceptions.PageError:
        st.error("Oops! No information available.")
    except wikipedia.exceptions.HTTPTimeoutError:
        st.error("Timeout error. Please try again later.")
    except Exception as e:
        st.code(f"{e}")
