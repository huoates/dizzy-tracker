import time

import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(
    page_title="Dizzy Diary",
    page_icon="📔",  # You can use an emoji or a URL to an image
)

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("Dizzy Diary")


with st.form("diary_entry"):
    food_eaten = st.text_input("What food did you eat?")
    st.write(
        "Rate the dizziness and vertigo on a scale of 0 (none) to 5 (worst I've ever experienced)"
    )
    dizzy_severity = st.slider("How much dizziness?", 0, 5)
    vertigo_severity = st.slider("How much vertigo?", 0, 5)
    comments = st.text_area("Any other comments?")
    submit_button = st.form_submit_button("Add Diary Entry")

if submit_button:
    with st.spinner("Saving to your diary..."):
        latest_df = conn.read(ttl=0)
        current_unix_timestamp = int(time.time())
        new_entry = {
            "food_eaten": food_eaten,
            "dizzy_severity": dizzy_severity,
            "vertigo_severity": vertigo_severity,
            "comments": comments,
            "timestamp": current_unix_timestamp,
        }
        new_data = pd.DataFrame([new_entry])
        updated_df = pd.concat([latest_df, new_data], ignore_index=True)
        conn.update(data=updated_df)
        st.cache_data.clear()
        st.success("Diary entry added!")
        st.rerun()

st.divider()
st.subheader("Recent Entries")
df = conn.read()
if df is not None and not df.empty:
    display_df = df.copy()
    display_df["date"] = pd.to_datetime(display_df["timestamp"], unit="s")
    display_df["date"] = (
        display_df["date"]
        .dt.tz_localize("UTC")
        .dt.tz_convert("America/Chicago")
        .dt.strftime("%b %d, %I:%M %p")
    )
    display_df = display_df.drop(columns=["timestamp"])
    # Option 1: A searchable, sortable table
    st.dataframe(display_df.sort_values(by="date", ascending=False), hide_index=True)

    # Option 2: Total count for a quick "health check" of your sheet
    st.info(f"Total entries logged: {len(display_df)}")
else:
    st.warning("No data found yet. Try adding your first entry below!")
