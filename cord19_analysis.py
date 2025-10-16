import pandas as pd

# Load the dataset
df = pd.read_csv("metadata.csv")

# Show first 5 rows
print(df.head())

# Check number of rows and columns
print("Shape:", df.shape)

# Get basic info about columns and data types
print(df.info())
# Check missing values for each column
missing = df.isnull().sum()
print("Missing values per column:\n", missing)

# Quick stats for numerical columns
print("\nNumerical stats:\n", df.describe())

# Convert publish_time to datetime
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')

# Extract year from publish_time
df['year'] = df['publish_time'].dt.year

# Count papers per year
year_counts = df['year'].value_counts().sort_index()
print("\nPapers per year:\n", year_counts)
# ===== Step 4: Data Cleaning =====

# 1. Drop columns that are mostly empty or not useful
columns_to_drop = ['mag_id', 'arxiv_id', 'pdf_json_files', 'pmc_json_files']
df_clean = df.drop(columns=columns_to_drop)

# 2. Drop rows without title or publish_time (essential for analysis)
df_clean = df_clean.dropna(subset=['title', 'publish_time'])

# 3. Remove papers with invalid years (before 2019 or after 2022)
df_clean = df_clean[(df_clean['year'] >= 2019) & (df_clean['year'] <= 2022)]

# 4. Optional: create a new column counting words in abstract
df_clean['abstract_word_count'] = df_clean['abstract'].apply(lambda x: len(str(x).split()))

# 5. Reset index after cleaning
df_clean = df_clean.reset_index(drop=True)

# 6. Quick check
print("Cleaned dataset shape:", df_clean.shape)
print(df_clean[['title', 'publish_time', 'year', 'abstract_word_count']].head())
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns

# ===== 1. Publications by Year =====
year_counts = df_clean['year'].value_counts().sort_index()

plt.figure(figsize=(8,5))
plt.bar(year_counts.index, year_counts.values, color='skyblue')
plt.title("Number of COVID-19 Papers by Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.xticks(year_counts.index)
plt.show()

# ===== 2. Top Journals =====
top_journals = df_clean['journal'].value_counts().head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis")
plt.title("Top 10 Journals Publishing COVID-19 Research")
plt.xlabel("Number of Papers")
plt.ylabel("Journal")
plt.show()

# ===== 3. Most Frequent Words in Titles =====
# Combine all titles
all_titles = " ".join(df_clean['title'].dropna().astype(str)).lower().split()
# Count words
word_counts = Counter(all_titles)
# Most common 20 words
common_words = word_counts.most_common(20)

words, counts = zip(*common_words)

plt.figure(figsize=(10,6))
sns.barplot(x=counts, y=words, palette="magma")
plt.title("Top 20 Most Frequent Words in Paper Titles")
plt.xlabel("Count")
plt.ylabel("Word")
plt.show()

# ===== 4. Distribution of Papers by Source =====
source_counts = df_clean['source_x'].value_counts()

plt.figure(figsize=(8,6))
plt.pie(source_counts, labels=source_counts.index, autopct='%1.1f%%', startangle=140)
plt.title("Distribution of Papers by Source")
plt.show()

