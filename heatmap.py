import pandas as pd
import ast
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the Excel file
file_path = 'сравнение групп.xls'
df = pd.read_excel(file_path)

# Ensure column names are strings for consistent access
df.columns = df.columns.astype(str)

# Function to parse list-like strings, handling various formats and errors
def parse_list_string(list_data):
    if pd.isna(list_data):
        return []
    if isinstance(list_data, (int, float)): # If it's a single number, treat as a list with that number
        return [str(int(list_data))] # Convert to string for TF-IDF
    if isinstance(list_data, str):
        list_data = list_data.strip()
        # Try ast.literal_eval first for proper list strings (e.g., "['item1', 'item2']")
        try:
            parsed = ast.literal_eval(list_data)
            if isinstance(parsed, list):
                # Return all elements as strings, without any digit check
                return [str(x) for x in parsed if pd.notna(x)]
            else: # If it's a single item like 'item' or 123
                return [str(parsed)]
        except (ValueError, SyntaxError):
            # If ast.literal_eval fails, try to parse as comma-separated strings
            items = []
            for item in list_data.split(','):
                cleaned_item = item.strip().strip("'").strip('"') # Remove leading/trailing quotes
                if cleaned_item: # Only add if not empty after cleaning
                    items.append(cleaned_item)
            return items
    return [] # Default for unhandled types or parsing failures

# Apply the parsing function to the 'Список' column
df['Parsed_Список'] = df['Список'].apply(parse_list_string)

# Convert 'Категория' to numeric, handling missing values by filling with a placeholder like -1
df['Категория'] = pd.to_numeric(df['Категория'], errors='coerce').fillna(-1).astype(int)

# Group by 'Категория' and aggregate all 'Parsed_Список' items into a single list per category
category_documents = df.groupby('Категория')['Parsed_Список'].apply(lambda x: [item for sublist in x for item in sublist]).reset_index()

# Create a 'full_document' string for each category by joining its aggregated Parsed_Список items
category_documents['full_document'] = category_documents['Parsed_Список'].apply(lambda x: ' '.join(x))

# The labels for the matrix will now be unique categories
unique_category_labels = category_documents['Категория'].tolist()
documents_for_tfidf_new = category_documents['full_document'].tolist()

# Initialize TF-IDF Vectorizer
tfidf_vectorizer = TfidfVectorizer(
    tokenizer=lambda x: x.split(), # Split by space to get individual names as tokens
    lowercase=False # Names don't need lowercasing, treat as distinct tokens
)

# Fit and transform the documents to get TF-IDF vectors
tfidf_matrix = tfidf_vectorizer.fit_transform(documents_for_tfidf_new)

# Calculate cosine similarity between the TF-IDF vectors
cosine_sim_matrix = cosine_similarity(tfidf_matrix)

# Create a DataFrame for the similarity matrix with unique category labels
tfidf_similarity_df = pd.DataFrame(cosine_sim_matrix, index=unique_category_labels, columns=unique_category_labels)

print("TF-IDF Cosine Similarity Matrix for unique categories:")
print(tfidf_similarity_df)
output_file_path = 'Сравнение групп результат.xlsx'

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter(output_file_path, engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
tfidf_similarity_df.to_excel(writer, sheet_name='Similarity Matrix', index=True)

# Get the xlsxwriter workbook and worksheet objects.
workbook  = writer.book
worksheet = writer.sheets['Similarity Matrix']

# Add a format for the green fill.
green_format = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})

# Get the dimensions of the dataframe.
(max_row, max_col) = tfidf_similarity_df.shape

# Apply a conditional format to the cell range.
# Add 1 to max_row and max_col as Excel ranges are 1-indexed and exclude the header row/column
# The data starts from the second row (index 1) and second column (index 1).
worksheet.conditional_format(1, 1, max_row, max_col, {'type': 'cell',
                                                   'criteria': '>=',
                                                   'value': 0.9,
                                                   'format': green_format})

# Close the Pandas Excel writer and output the Excel file.
writer.close()

print(f"Матрица сходства с условным форматированием сохранена в файл: {output_file_path}")

import matplotlib.pyplot as plt
import seaborn as sns

# Create the heatmap
plt.figure(figsize=(14, 12)) # Adjusted figure size for better readability
sns.heatmap(tfidf_similarity_df, annot=True, cmap='viridis', fmt=".2f", linewidths=.5)
plt.title('TF-IDF Cosine Similarity Heatmap for Categories', fontsize=16) # Increased title fontsize
plt.xlabel('Category', fontsize=12)
plt.ylabel('Category', fontsize=12)
plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better visibility if they overlap
plt.yticks(rotation=0) # Ensure y-axis labels are horizontal
plt.tight_layout() # Automatically adjust plot parameters for a tight layout

# Save the heatmap figure to an image file first, before displaying it
image_path = 'heatmap.png'
plt.savefig(image_path, bbox_inches='tight', dpi=300)

plt.show()

image_path = 'heatmap.png'

print(f"Тепловая карта успешно сохранена как PNG файл: {image_path}")

