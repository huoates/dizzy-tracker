import streamlit as st

st.set_page_config(
    page_title="Dizzy Diary Home",
    page_icon="📔",
)


st.title("Welcome to Your Diary!")
st.write(
    """
    Use this application to log your daily experiences with dizziness, vertigo,
    and related symptoms. Track potential triggers like food and stress levels,
    and monitor your progress over time.
    """
)

st.info("Navigate using the sidebar to 'Add New Entry' or 'View Entries'.")

# You can add more content here for your home page, like charts or summaries.
# For example:
# st.subheader("Your Dizzy Diary at a Glance")
# # Placeholder for future charts or insights
# st.write("Coming soon: personalized insights and trend analysis!")
