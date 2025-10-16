import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

# Load cleaned dataset (or use the same CSV if you prefer)
df = pd.read_csv("metadata.csv")
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df = df.dropna(subset=['title', 'publish_time'])
df = df[(df['year'] >= 2019) & (df['year'] <= 2022)]
df['abstract_word_count'] = df['abstract'].apply(lambda x: len(str(x).split()))

st.title("CORD-19 Data Explorer")
st.write("Interactive exploration of COVID-19 research papers")

# Sidebar filters
year_range = st.slider("Select Year Range", 2019, 2022, (2019, 2022))

filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Show filtered data sample
st.subheader("Sample Papers")
st.dataframe(filtered_df[['title', 'authors', 'journal', 'year']].head(10))

# Plot publications by year
year_counts = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values, color='skyblue')
ax.set_title("Number of Papers by Year")
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

# Top 10 Journals
top_journals = filtered_df['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis", ax=ax2)
ax2.set_title("Top 10 Journals")
ax2.set_xlabel("Number of Papers")
ax2.set_ylabel("Journal")
st.pyplot(fig2)
