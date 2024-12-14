
file_path = 'netflix_list.csv'
with open(file_path, 'r', encoding='utf-8') as file:
    rows = file.readlines()
data_as_lists = [row.strip().split(',') for row in rows]
headers = data_as_lists[0] 
data = data_as_lists[1:] 
rating_index = headers.index('rating')
filtered_by_rating = [
    row for row in data
    if len(row) > rating_index and row[rating_index].replace('.', '', 1).isdigit() and float(row[rating_index]) > 7.5
]
filtered_top_columns = [row[:5] for row in filtered_by_rating]

def netflix_generator(data, headers):

    language_index = headers.index('language')
    type_index = headers.index('type')
    end_year_index = headers.index('endYear')
    
    for row in data:
        if (
            len(row) > max(language_index, type_index, end_year_index) and 
            row[language_index] == 'English' and
            row[type_index] in ['tvSeries', 'movie'] and
            row[end_year_index].isdigit() and int(row[end_year_index]) > 2015
        ):
            yield row

netflix_gen = netflix_generator(data, headers)
generated_rows = [next(netflix_gen) for _ in range(5)]

print("Заголовки:", headers[:5]) 
print("Відфільтровані дані (перші 6 рядків, рейтинг > 7.5):")
for row in filtered_top_columns[:6]:
    print(row)
print("\nРезультати генератора (перші 5 рядків):")
for row in generated_rows:
    print(row)
