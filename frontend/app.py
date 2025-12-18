import streamlit as st
import requests

# ========================
# CONFIG
# ========================

API_URL = "http://127.0.0.1:8000/recommend"

st.set_page_config(
    page_title="SHL Assessment Recommendation Engine",
    layout="centered"
)

# ========================
# UI
# ========================

st.title("🔍 SHL Assessment Recommendation Engine")
st.write(
    "Enter a job requirement or hiring need, and get relevant SHL assessments."
)

query = st.text_input(
    "Enter your requirement:",
    placeholder="e.g. Looking for a cognitive assessment for graduates"
)

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Fetching recommendations..."):
            response = requests.post(
                API_URL,
                json={"query": query}
            )

        if response.status_code == 200:
            results = response.json()

            if not results:
                st.info("No recommendations found.")
            else:
                st.success(f"Top {len(results)} recommendations:")

                for idx, item in enumerate(results, start=1):
                    st.markdown(f"### {idx}. {item['name']}")
                    st.markdown(f"**URL:** {item['url']}")
                    st.markdown(f"**Description:** {item['description']}")
                    st.markdown(
                        f"- Duration: {item['duration']}\n"
                        f"- Remote Support: {item['remote_support']}\n"
                        f"- Adaptive Support: {item['adaptive_support']}\n"
                        f"- Test Type: {item['test_type']}"
                    )
                    st.markdown("---")
        else:
            st.error("Error connecting to recommendation service.")
