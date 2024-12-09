import streamlit as st
import pandas as pd

# Load the scraped data from the CSV
data_file = "behance_jobs.csv"
try:
    df = pd.read_csv(data_file)
except FileNotFoundError:
    st.error(f"File '{data_file}' not found. Please make sure the CSV exists in the same directory.")
    st.stop()

# Set up the Streamlit app
st.set_page_config(page_title="Job Listings", layout="wide")
st.title("Job Listings from Behance")
st.write("Explore job listings with images and search functionality.")

# Get unique company names for the dropdown
company_names = df["Company"].dropna().unique().tolist()
company_names.insert(0, "All Companies")  # Add an "All Companies" option at the top

# Combined search bar and dropdown
with st.container():
    col1, col2 = st.columns([2, 1])
    with col1:
        search_query = st.text_input("Search by Job Title or Location:", placeholder="Enter search term...")
    with col2:
        selected_company = st.selectbox("Select a Company:", company_names)

# Filter the DataFrame based on search query and selected company
filtered_df = df

if search_query:
    filtered_df = filtered_df[
        filtered_df["Job Title"].str.lower().str.contains(search_query.lower(), na=False) |
        filtered_df["Location"].str.lower().str.contains(search_query.lower(), na=False)
    ]

if selected_company != "All Companies":
    filtered_df = filtered_df[filtered_df["Company"] == selected_company]

# Display job cards in a grid
if filtered_df.empty:
    st.warning("No results found for your search.")
else:
    # Create a 3-column layout for displaying job cards
    cols = st.columns(3)
    for i, row in filtered_df.iterrows():
        col = cols[i % 3]  # Rotate through the columns
        with col:
            st.image(row["Image URL"], use_container_width=True, caption=row["Job Title"])
            st.write(f"**{row['Job Title']}**")
            st.write(f"Company: {row['Company']}")
            st.write(f"Location: {row['Location']}")
            st.write(f"Posted: {row['Time Posted']}")
            st.write("---")
