

from IPython.display import display as display
import pandas as pd


# Read the Excel file

df_excel = pd.read_excel('операторы_бухгалтеры.xlt')

operlist = []
buhlist = []

# Iterate through each row of the DataFrame to populate operlist and buhlist
for index, row in df_excel.iterrows():
    # Process 'Операторы' column for the current row
    oper_item = row['Операторы']
    if pd.notna(oper_item):
        oper_names = [name.strip() for name in str(oper_item).split(',') if name.strip()]
        operlist.append(oper_names)
    else:
        operlist.append([])  # Append an empty list if the cell is NaN or contains no valid names

    # Process 'Бухгалтеры' column for the current row
    buh_item = row['Бухгалтеры']
    if pd.notna(buh_item):
        buh_names = [name.strip() for name in str(buh_item).split(',') if name.strip()]
        buhlist.append(buh_names)
    else:
        buhlist.append([])  # Append an empty list if the cell is NaN or contains no valid names

print("operlist has been re-created:")
for sublist in operlist:
    print(sublist)

print("\nbuhlist has been re-created:")
for sublist in buhlist:
    print(sublist)

# список обработчиков
oper_unique_set = list(set(person for sublist in operlist for person in sublist))  # Все операторы
buh_unique_set = list(set(person for sublist in buhlist for person in sublist))  # Все бухгалтеры
unique_set = list(set(oper_unique_set + buh_unique_set))  # Весь список обработчиков

categorized_items = []

for item in unique_set:
    in_oper_unique_set = item in oper_unique_set
    in_buh_unique_set = item in buh_unique_set

    category = ""
    if in_oper_unique_set and not in_buh_unique_set:
        category = "O"
    elif not in_oper_unique_set and in_buh_unique_set:
        category = "B"
    elif in_oper_unique_set and in_buh_unique_set:
        category = "OB"
    else:
        category = "None"
    categorized_items.append((item, category))
    print(f"'{item}': In operlist: {in_oper_unique_set}, In buhlist: {in_buh_unique_set}, Category: {category}")

    # Ensure category_map is defined from categorized_items, which is generated in an earlier cell.
    category_map = {item: category for item, category in categorized_items}

from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Extract categories from categorized_items
categories = [item[1] for item in categorized_items]

# Count the occurrences of each category
category_counts = Counter(categories)

# Convert to DataFrame for easier plotting with seaborn
plot_data = pd.DataFrame(category_counts.items(), columns=['Category', 'Count'])

# Ensure all expected categories are present, even if their count is 0
all_categories = ['O', 'B', 'OB']
plot_data = plot_data.set_index('Category').reindex(all_categories, fill_value=0).reset_index()

# Create the bar plot
plt.figure(figsize=(8, 6))
sns.barplot(x='Category', y='Count', data=plot_data, palette='viridis', hue='Category', legend=False)
plt.title('Distribution of Items by Category')
plt.xlabel('Category')
plt.ylabel('Number of Items')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

import pandas as pd

results_data = []

# Determine the maximum length of the two lists
max_len = max(len(operlist), len(buhlist))

# Pad the shorter list(s) with empty lists to match the maximum length
operlist_padded = operlist + [[]] * (max_len - len(operlist))
buhlist_padded = buhlist + [[]] * (max_len - len(buhlist))

# Iterate up to the maximum length
for i in range(max_len):
  # Get current sublists from the padded lists
  current_operlist_sublist = operlist_padded[i]
  current_buhlist_sublist = buhlist_padded[i]

  # Categorization based on row-specific sets
  common_set = set(current_operlist_sublist) & set(current_buhlist_sublist)
  common_list = list(common_set)

  oper_set = set(current_operlist_sublist) - set(current_buhlist_sublist)
  oper_list = list(oper_set)

  buh_set = set(current_buhlist_sublist) - set(current_operlist_sublist)
  buh_list = list(buh_set)

  results_data.append({
      "Строка": i,
      "Только Операторы": sorted(list(oper_list)),
      "Только Бухгалтеры": sorted(list(buh_list)),
      "Операторы и Бухгалтеры": sorted(list(common_list))
  })

df_results = pd.DataFrame(results_data)

# Define the desired column order for the table
desired_column_order = ["Строка", "Только Операторы", "Только Бухгалтеры", "Операторы и Бухгалтеры"]

# Reindex the DataFrame to match the desired column order
import pandas as pd

results_data = []

# Determine the maximum length of the two lists
max_len = max(len(operlist), len(buhlist))

# Pad the shorter list(s) with empty lists to match the maximum length
operlist_padded = operlist + [[]] * (max_len - len(operlist))
buhlist_padded = buhlist + [[]] * (max_len - len(buhlist))

# Iterate up to the maximum length
for i in range(max_len):
  # Get current sublists from the padded lists
  current_operlist_sublist = operlist_padded[i]
  current_buhlist_sublist = buhlist_padded[i]

  # Categorization based on row-specific sets
  common_set = set(current_operlist_sublist) & set(current_buhlist_sublist)
  common_list = list(common_set)

  oper_set = set(current_operlist_sublist) - set(current_buhlist_sublist)
  oper_list = list(oper_set)

  buh_set = set(current_buhlist_sublist) - set(current_operlist_sublist)
  buh_list = list(buh_set)

  results_data.append({
      "Строка": i,
      "Только Операторы": sorted(list(oper_list)),
      "Только Бухгалтеры": sorted(list(buh_list)),
      "Операторы и Бухгалтеры": sorted(list(common_list))
  })

df_results = pd.DataFrame(results_data)

# Define the desired column order for the table
desired_column_order = ["Строка", "Только Операторы", "Только Бухгалтеры", "Операторы и Бухгалтеры"]

# Reindex the DataFrame to match the desired column order
df_results = df_results[desired_column_order]
display(df_results)

import pandas as pd

# Ensure category_map is defined from categorized_items, which is generated in an earlier cell.
# category_map = {item: category for item, category in categorized_items} # This line is commented as category_map is already in scope

# Create a deep copy to avoid modifying the original df_results from the previous cell directly
df_results_processed = df_results.copy()

print("Применяю логику перемещения элементов из 'Только Операторы' в 'Только Бухгалтеры' на основе глобальной категории...")

for index, row in df_results_processed.iterrows():
    # Get current lists for the row
    current_row_operators = list(row['Только Операторы'])
    current_row_bookkeepers = list(row['Операторы и Бухгалтеры'])

    # Lists to hold items after potential movement
    newly_retained_operators = []
    newly_moved_to_bookkeepers = []

    for person in current_row_operators:
        global_category = category_map.get(person)

        if global_category == 'O':
            newly_retained_operators.append(person)
        else: # global_category is 'B' or 'OB'
            newly_moved_to_bookkeepers.append(person)
            print(f"Перемещено: '{person}' из 'Только Операторы' строки {index} в 'Операторы и Бухгалтеры' так как его глобальная категория '{global_category}' (не 'O').")

    # Combine original bookkeepers with newly moved items, then convert to set to remove duplicates
    # before converting back to list and sorting
    final_bookkeepers_for_row = sorted(list(set(current_row_bookkeepers + newly_moved_to_bookkeepers)))

    # Update the DataFrame row
    df_results_processed.at[index, 'Только Операторы'] = sorted(newly_retained_operators)
    df_results_processed.at[index, 'Операторы и Бухгалтеры'] = final_bookkeepers_for_row

print("\nОбновленная таблица распределения:")
display(df_results_processed)

import itertools
from collections import Counter
import pandas as pd
import random

# --- Step 1: Helper function to generate all subsets from a list ---
def generate_all_subsets(data_list):
    """
    Generates all possible frozenset subsets (including single elements) from a given list.
    Order of elements does not matter, so frozenset is used for hashability and comparison.
    """
    if not data_list:
        return []
    subsets = []
    # Generate combinations of all possible lengths (from 1 to len(data_list))
    for i in range(1, len(data_list) + 1):
        for combo in itertools.combinations(data_list, i):
            subsets.append(frozenset(combo))
    return subsets

# --- Step 2: Function to find significant common sublists within a column ---
def find_significant_common_sublists(column_series):
    """
    Analyzes a Series of lists (representing a column) to find common sublists.
    Criteria:
    1. Within each row, if sublists overlap, prioritize the longer one.
       (i.e., if A is a subset of B and B is found in the same row, A is not counted for that row).
    2. A sublist must appear in at least two rows to be considered 'common'.
    """
    all_filtered_subsets_per_row = []

    # Process each row (list of names) in the column
    for row_list in column_series.dropna().apply(lambda x: x if isinstance(x, list) else []):
        if not row_list:
            continue

        # Generate all possible subsets for the current row
        subsets_for_this_row = generate_all_subsets(row_list)

        # Sort subsets by length in descending order to prioritize longer ones
        subsets_for_this_row.sort(key=len, reverse=True)

        significant_subsets_in_current_row = []
        elements_covered_by_longer_subsets = set()

        # Apply the rule: prioritize longer overlapping sublists within this row
        for current_subset in subsets_for_this_row:
            if not current_subset: # Skip empty sets if any
                continue

            # Check if any element of the current_subset is already covered by a longer subset
            # If no elements are covered, this is a 'significant' non-overlapping subset for this row
            if not any(elem in elements_covered_by_longer_subsets for elem in current_subset):
                significant_subsets_in_current_row.append(current_subset)
                elements_covered_by_longer_subsets.update(current_subset)

        all_filtered_subsets_per_row.extend(significant_subsets_in_current_row)

    # Count occurrences of these significant sublists across all rows
    subset_counts = Counter(all_filtered_subsets_per_row)

    # Filter for sublists that appear in at least two rows
    final_common_subsets = [s for s, count in subset_counts.items() if count >= 2]

    return final_common_subsets

# --- Step 3: Identify target columns and compute common sublists ---
target_columns = ['Только Операторы', 'Только Бухгалтеры', 'Операторы и Бухгалтеры']

column_common_sublists = {}
all_unique_common_subsets = set()

for col in target_columns:
    # Ensure df_results_processed is available from previous cells
    if col in df_results_processed.columns:
        print(f"Processing column: '{col}'...")
        common_subs = find_significant_common_sublists(df_results_processed[col])
        column_common_sublists[col] = common_subs
        all_unique_common_subsets.update(common_subs)
        print(f"Found {len(common_subs)} significant common sublists in '{col}'.")
    else:
        print(f"Warning: Column '{col}' not found in df_results_processed. Skipping.")

# --- Step 4: Generate a global color map for unique common sublists ---
def generate_distinct_colors(n):
    """
    Generates a list of n visually distinct hex colors.
    """
    colors = [
        '#FFD1DC', '#ADD8E6', '#90EE90', '#FFD700', '#DDA0DD', '#FFA07A', '#B0E0E6',
        '#FFCC99', '#CCCCFF', '#FFB6C1', '#87CEFA', '#98FB98', '#FAFAD2', '#E6E6FA'
    ]
    # Extend with random colors if more than predefined are needed
    if n > len(colors):
        for _ in range(n - len(colors)):
            colors.append('#%06X' % random.randint(0, 0xFFFFFF))
    random.shuffle(colors)
    return colors[:n]

# Generate enough distinct colors for all unique common sublists
num_unique_subsets = len(all_unique_common_subsets)
if num_unique_subsets > 0:
    distinct_colors = generate_distinct_colors(num_unique_subsets)
    global_color_map = {subset: distinct_colors[i] for i, subset in enumerate(all_unique_common_subsets)}
else:
    global_color_map = {}

print(f"Generated color map for {len(global_color_map)} unique common sublists.")

# --- Step 5: Define styling function for DataFrame cells ---
def highlight_cell_style(cell_value, column_name, common_sublists_map, color_map):
    """
    Returns CSS style string for a cell if its content contains a common sublist.
    Prioritizes highlighting based on the longest matching common sublist in the cell.
    """
    if not isinstance(cell_value, list) or not cell_value:
        return ''  # No highlighting for non-list or empty cells

    cell_set = frozenset(cell_value)
    relevant_common_sublists = common_sublists_map.get(column_name, [])

    best_match_subset = None
    # Find the longest matching common sublist for this cell
    for common_subset in relevant_common_sublists:
        if common_subset.issubset(cell_set):
            if best_match_subset is None or len(common_subset) > len(best_match_subset):
                best_match_subset = common_subset

    if best_match_subset:
        color = color_map.get(best_match_subset, '#FFFFFF') # Default to white if no color found
        return f'background-color: {color}; font-weight: bold;'
    return ''

# --- Step 6: Apply styling to the DataFrame ---
def column_style_applier(s, common_sublists_map, color_map, target_columns):
    """
    Applies the highlight_cell_style function to elements of target columns.
    """
    if s.name in target_columns:
        return s.apply(lambda cell_value: highlight_cell_style(cell_value, s.name, common_sublists_map, color_map))
    return [''] * len(s) # No styling for other columns

print("Applying styling to the DataFrame...")
styled_df = df_results_processed.style.apply(column_style_applier,
                                            common_sublists_map=column_common_sublists,
                                            color_map=global_color_map,
                                            target_columns=target_columns,
                                            axis=0)

display(styled_df)
print("Styling applied. Common sublists highlighted.")

output_excel_path = 'Результаты обработки.xlsx'
styled_df.to_excel(output_excel_path, index=False)
print(f"DataFrame успешно сохранен в '{output_excel_path}'")

import itertools
from collections import Counter
import pandas as pd

# Переопределение вспомогательной функции (если ее нет в контексте из предыдущих шагов)
def generate_all_subsets(data_list):
    """
    Генерирует все возможные frozenset подмножества (включая отдельные элементы) из данного списка.
    Порядок элементов не имеет значения, поэтому frozenset используется для хешируемости и сравнения.
    """
    if not data_list:
        return []
    subsets = []
    # Генерируем комбинации всех возможных длин (от 1 до len(data_list))
    for i in range(1, len(data_list) + 1):
        for combo in itertools.combinations(data_list, i):
            subsets.append(frozenset(combo))
    return subsets

# Переопределение функции для поиска значимых общих подсписков (если ее нет в контексте)
def find_significant_common_sublists(column_series):
    """
    Анализирует Series списков (представляющих столбец) для поиска общих подсписков.
    Критерии:
    1. В каждой строке, если подсписки перекрываются, приоритет отдается более длинному.
       (т.е. если A является подмножеством B, и B найдено в той же строке, A не учитывается для этой строки).
    2. Подсписок должен встречаться как минимум в двух строках, чтобы считаться 'общим'.
    """
    all_filtered_subsets_per_row = []

    # Обрабатываем каждую строку (список имен) в столбце
    for row_list in column_series.dropna().apply(lambda x: x if isinstance(x, list) else []):
        if not row_list:
            continue

        # Генерируем все возможные подмножества для текущей строки
        subsets_for_this_row = generate_all_subsets(row_list)

        # Сортируем подмножества по длине в убывающем порядке, чтобы отдать приоритет более длинным
        subsets_for_this_row.sort(key=len, reverse=True)

        significant_subsets_in_current_row = []
        elements_covered_by_longer_subsets = set()

        # Применяем правило: приоритет более длинных перекрывающихся подсписков в этой строке
        for current_subset in subsets_for_this_row:
            if not current_subset: # Пропускаем пустые множества, если они есть
                continue

            # Проверяем, покрыт ли какой-либо элемент current_subset более длинным подмножеством
            # Если ни один элемент не покрыт, это 'значимое' неперекрывающееся подмножество для этой строки
            if not any(elem in elements_covered_by_longer_subsets for elem in current_subset):
                significant_subsets_in_current_row.append(current_subset)
                elements_covered_by_longer_subsets.update(current_subset)

        all_filtered_subsets_per_row.extend(significant_subsets_in_current_row)

    # Подсчитываем вхождения этих значимых подсписков по всем строкам
    subset_counts = Counter(all_filtered_subsets_per_row)

    # Фильтруем подсписки, которые встречаются как минимум в двух строках
    final_common_subsets = [s for s, count in subset_counts.items() if count >= 2]

    return final_common_subsets

# Убедитесь, что df_results_processed доступен и актуален из предыдущих ячеек
# (предполагается, что предыдущая ячейка '5e251c28' была выполнена и создала df_results_processed)

# Определяем целевые столбцы для анализа сходства
target_columns = ['Только Операторы', 'Только Бухгалтеры', 'Операторы и Бухгалтеры']

column_common_sublists = {}
all_unique_common_subsets = set()

for col in target_columns:
    if col in df_results_processed.columns:
        print(f"Обработка столбца для общих подсписков: '{col}'...")
        common_subs = find_significant_common_sublists(df_results_processed[col])
        column_common_sublists[col] = common_subs
        all_unique_common_subsets.update(common_subs)
        print(f"Найдено {len(common_subs)} значимых общих подсписков в '{col}'.")
    else:
        print(f"Предупреждение: Столбец '{col}' не найден в df_results_processed. Пропускаем.")

# Присваиваем последовательные номера категорий всем уникальным общим подспискам
# Сортировка по строковому представлению для детерминированного присвоения ID
category_id_map = {subset: i + 1 for i, subset in enumerate(sorted(list(all_unique_common_subsets), key=lambda x: str(x)))}
print(f"Присвоено {len(category_id_map)} уникальных ID категорий общим подспискам.")

# Функция для получения ID категории для содержимого ячейки на основе схожести Жаккара
def get_subset_category_id(cell_value, common_sublists_for_column, global_category_id_map):
    if not isinstance(cell_value, list) or not cell_value:
        return None # Нет категории для не-списков или пустых ячеек

    cell_set = frozenset(cell_value)
    best_match_subset = None
    max_similarity = -1.0 # Инициализируем значением ниже любого возможного индекса Жаккара

    # Находим подсписок с наибольшей схожестью Жаккара, превышающей пороговое значение
    for common_subset in common_sublists_for_column:
        if not common_subset: # Пропускаем пустые common_subset, чтобы избежать деления на ноль
            continue

        intersection_size = len(cell_set.intersection(common_subset))
        union_size = len(cell_set.union(common_subset))

        if union_size == 0:
            similarity = 0.0 # Если оба набора пусты, это не имеет смысла для непустого common_subset
        else:
            similarity = intersection_size / union_size

        if similarity > 0.8: # Применяем пороговое значение
            # Если несколько подсписков соответствуют порогу, приоритет отдается тому, у кого выше схожесть
            if similarity > max_similarity:
                max_similarity = similarity
                best_match_subset = common_subset
            # Если схожесть равна, предпочтение отдается более длинному common_subset (для разрешения коллизий)
            elif similarity == max_similarity and best_match_subset is not None and len(common_subset) > len(best_match_subset):
                best_match_subset = common_subset

    if best_match_subset:
        return global_category_id_map.get(best_match_subset)
    return None

# Создаем новые столбцы для категорий в копии обработанного DataFrame
df_results_categorized = df_results_processed.copy()

for col in target_columns:
    new_col_name = f'Категория {col}'
    # Вставляем новый столбец категории сразу после соответствующего анализируемого столбца
    col_index = df_results_categorized.columns.get_loc(col)

    if col in df_results_categorized.columns:
        # Получаем общие подсписки, специфичные для этого столбца
        common_sublists_for_current_col = column_common_sublists.get(col, [])
        df_results_categorized.insert(
            loc=col_index + 1,
            column=new_col_name,
            value=df_results_categorized[col].apply(
                lambda x: get_subset_category_id(x, common_sublists_for_current_col, category_id_map)
            )
        )
    else:
        # Если целевой столбец не был найден, вставляем пустой столбец категории
        df_results_categorized.insert(
            loc=col_index + 1,
            column=new_col_name,
            value=None
        )

print("\nОбновленный DataFrame с категориями сходства:")
display(df_results_categorized)

print("\nАнализ категоризации по столбцам (с учетом схожести Жаккара):")
summary_percentages_similarity = [] # Инициализируем список, чтобы избежать дублирования записей при повторном запуске

for col in target_columns:
    category_col_name = f'Категория {col}'
    if category_col_name in df_results_categorized.columns:
        total_rows = len(df_results_categorized)
        # Считаем непустые значения для категоризованных строк
        categorized_rows = df_results_categorized[category_col_name].count()
        uncategorized_rows = total_rows - categorized_rows

        percent_categorized = (categorized_rows / total_rows) * 100 if total_rows > 0 else 0
        percent_uncategorized = (uncategorized_rows / total_rows) * 100 if total_rows > 0 else 0

        summary_percentages_similarity.append({
            'Столбец': col,
            'Процент категоризованных строк': f'{percent_categorized:.2f}%',
            'Процент некатегоризованных строк': f'{percent_uncategorized:.2f}%'
        })

        print(f"\nСтолбец: '{col}'")
        print(f"  Процент строк, получивших категорию: {percent_categorized:.2f}%")
        print(f"  Процент строк, НЕ получивших категорию: {percent_uncategorized:.2f}%")
    else:
        print(f"\nСтолбец категории '{category_col_name}' не найден. Пропуск анализа для '{col}'.")

df_percentages_similarity = pd.DataFrame(summary_percentages_similarity)

output_excel_path = 'Результаты обработки2.xlsx'

with pd.ExcelWriter(output_excel_path, engine='xlsxwriter') as writer:
    df_results_categorized.to_excel(writer, sheet_name='Категории схожести', index=False)
    df_percentages_similarity.to_excel(writer, sheet_name='Анализ категоризации', index=False)

print(f"DataFrame с категориями схожести и анализ категоризации сохранены в файл '{output_excel_path}' на разных листах.")

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# The df_plot_operators DataFrame contains the required data:
# 'Оператор' (individual operators) and 'Категория ID' (category numbers) for 'Только Операторы' column.
# Prepare data for plotting for 'Только Операторы' column
plot_data_operators = []
for index, row in df_results_categorized.iterrows():
    operators_list = row['Только Операторы']
    category_id = row['Категория Только Операторы']

    if isinstance(operators_list, list) and operators_list:
        for operator in operators_list:
            plot_data_operators.append({
                'Оператор': operator,
                'Категория ID': category_id
            })

df_plot_operators = pd.DataFrame(plot_data_operators)



# Create a copy to avoid modifying the original DataFrame
plot_data_with_zero_category = df_plot_operators.copy()

# Fill NaN values in 'Категория ID' with 0 as requested, then convert to integer type
plot_data_with_zero_category['Категория ID'] = plot_data_with_zero_category['Категория ID'].fillna(0).astype(int)

# Sort the DataFrame by 'Оператор' column alphabetically
plot_data_with_zero_category = plot_data_with_zero_category.sort_values(by='Оператор').reset_index(drop=True)

plt.figure(figsize=(14, 8)) # Adjust figure size for better readability, making it wider for operator names
sns.scatterplot(
    x='Оператор',
    y='Категория ID',
    data=plot_data_with_zero_category,
    marker='o', # Use circular markers
    color='yellow', # As requested: yellow dots
    s=100, # Adjust size of the dots for visibility
    alpha=0.8 # Transparency
)

plt.title('Распределение индивидуальных операторов по их Категориям (Только Операторы)')
plt.xlabel('Индивидуальный Оператор')
plt.ylabel('Категория ID')
plt.xticks(rotation=90, ha='right', fontsize=8) # Rotate labels for better readability on X-axis
# Ensure all unique categories present in the data (including 0) are shown on Y-axis
plt.yticks(plot_data_with_zero_category['Категория ID'].unique().tolist())
plt.grid(axis='both', linestyle='--', alpha=0.7) # Add grid for better readability
plt.tight_layout() # Adjust layout to prevent labels from being cut off
plt.show()

import pandas as pd

# 'plot_data_with_zero_category' DataFrame уже содержит данные об операторах и их категориях,
# где NaN значения в категориях заменены на 0 и тип данных приведен к int.

# Группируем по 'Оператор' и собираем все уникальные 'Категория ID' в список.
# Сортируем список категорий для каждой группы для детерминированного вывода.
df_operator_table_from_plot = plot_data_with_zero_category.groupby('Оператор')['Категория ID'].apply(
    lambda x: sorted(list(x.unique()))
).reset_index()

# Переименовываем столбцы в соответствии с запросом пользователя
df_operator_table_from_plot.columns = ['Индивидуальный Оператор', 'Категории']

# Отображаем полученную таблицу
print("Таблица распределения индивидуальных операторов по их категориям (на основе данных графика):")
display(df_operator_table_from_plot)

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Prepare data for plotting for 'Только Бухгалтеры' column
plot_data_bookkeepers = []
for index, row in df_results_categorized.iterrows():
    bookkeepers_list = row['Только Бухгалтеры']
    category_id = row['Категория Только Бухгалтеры']

    if isinstance(bookkeepers_list, list) and bookkeepers_list:
        for bookkeeper in bookkeepers_list:
            plot_data_bookkeepers.append({
                'Бухгалтер': bookkeeper,
                'Категория ID': category_id
            })

df_plot_bookkeepers = pd.DataFrame(plot_data_bookkeepers)

# Create a copy to avoid modifying the original DataFrame
plot_data_bookkeepers_with_zero_category = df_plot_bookkeepers.copy()

# Fill NaN values in 'Категория ID' with 0 as requested, then convert to integer type
plot_data_bookkeepers_with_zero_category['Категория ID'] = plot_data_bookkeepers_with_zero_category['Категория ID'].fillna(0).astype(int)

# Sort the DataFrame by 'Бухгалтер' column alphabetically
plot_data_bookkeepers_with_zero_category = plot_data_bookkeepers_with_zero_category.sort_values(by='Бухгалтер').reset_index(drop=True)

plt.figure(figsize=(14, 8)) # Adjust figure size for better readability, making it wider for bookkeeper names
sns.scatterplot(
    x='Бухгалтер',
    y='Категория ID',
    data=plot_data_bookkeepers_with_zero_category,
    marker='o', # Use circular markers
    color='red', # As requested: yellow dots
    s=100, # Adjust size of the dots for visibility
    alpha=0.8 # Transparency
)

plt.title('Распределение индивидуальных бухгалтеров по их Категориям (Только Бухгалтеры)')
plt.xlabel('Индивидуальный Бухгалтер')
plt.ylabel('Категория ID')
plt.xticks(rotation=90, ha='right', fontsize=8) # Rotate labels for better readability on X-axis
# Ensure all unique categories present in the data (including 0) are shown on Y-axis
plt.yticks(plot_data_bookkeepers_with_zero_category['Категория ID'].unique().tolist())
plt.grid(axis='both', linestyle='--', alpha=0.7) # Add grid for better readability
plt.tight_layout() # Adjust layout to prevent labels from being cut off
plt.show()

import pandas as pd

# 'plot_data_bookkeepers_with_zero_category' DataFrame уже содержит данные о бухгалтерах и их категориях,
# где NaN значения в категориях заменены на 0 и тип данных приведен к int.

# Группируем по 'Бухгалтер' и собираем все уникальные 'Категория ID' в список.
# Сортируем список категорий для каждой группы для детерминированного вывода.
df_bookkeeper_table_from_plot = plot_data_bookkeepers_with_zero_category.groupby('Бухгалтер')['Категория ID'].apply(
    lambda x: sorted(list(x.unique()))
).reset_index()

# Переименовываем столбцы в соответствии с запросом пользователя
df_bookkeeper_table_from_plot.columns = ['Индивидуальный Бухгалтер', 'Категории']

# Отображаем полученную таблицу
print("Таблица распределения индивидуальных бухгалтеров по их категориям (на основе данных графика):")
display(df_bookkeeper_table_from_plot)

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Prepare data for plotting for 'Операторы и Бухгалтеры' column
plot_data_operators_bookkeepers = []
for index, row in df_results_categorized.iterrows():
    op_buh_list = row['Операторы и Бухгалтеры']
    category_id = row['Категория Операторы и Бухгалтеры']

    if isinstance(op_buh_list, list) and op_buh_list:
        for person in op_buh_list:
            plot_data_operators_bookkeepers.append({
                'Оператор/Бухгалтер': person,
                'Категория ID': category_id
            })

df_plot_operators_bookkeepers = pd.DataFrame(plot_data_operators_bookkeepers)

# Create a copy to avoid modifying the original DataFrame
plot_data_op_buh_with_zero_category = df_plot_operators_bookkeepers.copy()

# Fill NaN values in 'Категория ID' with 0 as requested, then convert to integer type
plot_data_op_buh_with_zero_category['Категория ID'] = plot_data_op_buh_with_zero_category['Категория ID'].fillna(0).astype(int)

# Sort the DataFrame by 'Оператор/Бухгалтер' column alphabetically
plot_data_op_buh_with_zero_category = plot_data_op_buh_with_zero_category.sort_values(by='Оператор/Бухгалтер').reset_index(drop=True)

plt.figure(figsize=(14, 8)) # Adjust figure size for better readability
sns.scatterplot(
    x='Оператор/Бухгалтер',
    y='Категория ID',
    data=plot_data_op_buh_with_zero_category,
    marker='o', # Use circular markers
    color='green', # As requested: yellow dots
    s=100, # Adjust size of the dots for visibility
    alpha=0.8 # Transparency
)

plt.title('Распределение индивидуальных операторов/бухгалтеров по их Категориям (Операторы и Бухгалтеры)')
plt.xlabel('Индивидуальный Оператор/Бухгалтер')
plt.ylabel('Категория ID')
plt.xticks(rotation=90, ha='right', fontsize=8) # Rotate labels for better readability on X-axis
# Ensure all unique categories present in the data (including 0) are shown on Y-axis
plt.yticks(plot_data_op_buh_with_zero_category['Категория ID'].unique().tolist())
plt.grid(axis='both', linestyle='--', alpha=0.7) # Add grid for better readability
plt.tight_layout() # Adjust layout to prevent labels from being cut off
plt.show()

import pandas as pd

# 'plot_data_op_buh_with_zero_category' DataFrame уже содержит данные об операторах/бухгалтерах и их категориях,
# где NaN значения в категориях заменены на 0 и тип данных приведен к int.

# Группируем по 'Оператор/Бухгалтер' и собираем все уникальные 'Категория ID' в список.
# Сортируем список категорий для каждой группы для детерминированного вывода.
df_op_buh_table_from_plot = plot_data_op_buh_with_zero_category.groupby('Оператор/Бухгалтер')['Категория ID'].apply(
    lambda x: sorted(list(x.unique()))
).reset_index()

# Переименовываем столбцы в соответствии с запросом пользователя
df_op_buh_table_from_plot.columns = ['Индивидуальный Оператор/Бухгалтер', 'Категории']

# Отображаем полученную таблицу
print("Таблица распределения индивидуальных операторов/бухгалтеров по их категориям (на основе данных графика):")
display(df_op_buh_table_from_plot)

import pandas as pd

# Подготовка df_operator_table_from_plot
df_operators_pivot = df_operator_table_from_plot.rename(
    columns={
        'Индивидуальный Оператор': 'Индивидуальный',
        'Категории': 'Категории Операторов (из графика)'
    }
)

# Подготовка df_bookkeeper_table_from_plot
df_bookkeepers_pivot = df_bookkeeper_table_from_plot.rename(
    columns={
        'Индивидуальный Бухгалтер': 'Индивидуальный',
        'Категории': 'Категории Бухгалтеров (из графика)'
    }
)

# Подготовка df_op_buh_table_from_plot
df_combined_pivot = df_op_buh_table_from_plot.rename(
    columns={
        'Индивидуальный Оператор/Бухгалтер': 'Индивидуальный',
        'Категории': 'Категории Операторов/Бухгалтеров (из графика)'
    }
)

# Объединяем таблицы
# Начинаем с операторов
merged_pivot_df = pd.merge(
    df_operators_pivot,
    df_bookkeepers_pivot,
    on='Индивидуальный',
    how='outer'
)

# Объединяем с объединенными операторами/бухгалтерами
merged_pivot_df = pd.merge(
    merged_pivot_df,
    df_combined_pivot,
    on='Индивидуальный',
    how='outer'
)

# Заменяем значения NaN (где человек не относится к категории) на пустые списки
for col in ['Категории Операторов (из графика)', 'Категории Бухгалтеров (из графика)', 'Категории Операторов/Бухгалтеров (из графика)']:
    if col in merged_pivot_df.columns:
        merged_pivot_df[col] = merged_pivot_df[col].apply(lambda x: x if isinstance(x, list) else [])
        # Преобразуем списки категорий в строки через запятую, явно преобразуя каждый элемент в int
        merged_pivot_df[col] = merged_pivot_df[col].apply(lambda x: ', '.join(map(lambda item: str(int(item)), x)) if x else '')

# Выводим финальную сводную таблицу
print("Сводная таблица распределения индивидуальных операторов и бухгалтеров по категориям (из графиков):")
display(merged_pivot_df)

output_summary_path = 'Распределение по категориям.xlsx'
merged_pivot_df.to_excel(output_summary_path, index=False)
print(f"Сводная таблица распределения сохранена в файл '{output_summary_path}'.")
