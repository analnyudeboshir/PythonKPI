file_path = 'netflix_list.csv'

with open(file_path, 'r', encoding='utf-8') as file:
    rows = file.readlines()

headers = [header.strip(' "') for header in rows[0].strip().split(',')]
data = []

for row in rows[1:]:
    values = []
    current_value = ''
    in_quotes = False
    for char in row:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            values.append(current_value.strip(' "'))
            current_value = ''
        else:
            current_value += char
    values.append(current_value.strip(' "'))
    data.append(values)
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
print("Відфільтровані дані (перші 6 рядків, рейтинг > 7.5):")
for row in filtered_top_columns[:6]:
    print(row)
print("\nРезультати генератора (перші 5 рядків):")
for row in generated_rows:
    print(row)
cast_index = headers.index('cast')
def filter_cast(data, cast_index):
    return [row[cast_index] for row in data if len(row) > cast_index and len(row[cast_index]) > 50]

cast_entries = filter_cast(data, cast_index)[:10]

is_adult_index = headers.index('isAdult')
rating_index = headers.index('rating')
num_votes_index = headers.index('numVotes')

adult_count = sum(
    1 for row in data
    if len(row) > is_adult_index and row[is_adult_index].isdigit() and int(row[is_adult_index]) == 1
)

valid_ratings = [
    float(row[rating_index]) for row in data
    if len(row) > max(rating_index, num_votes_index) and
    row[num_votes_index].isdigit() and int(row[num_votes_index]) > 1000 and
    row[rating_index].replace('.', '', 1).isdigit()
]

average_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0


episodes_index = headers.index('episodes')
titles_with_conditions = [
    row[headers.index('title')] for row in data
    if len(row) > max(episodes_index, rating_index) and
    row[episodes_index].isdigit() and int(row[episodes_index]) > 10 and
    row[rating_index].replace('.', '', 1).isdigit() and float(row[rating_index]) > average_rating
]

print("\nПерші 10 записів з ітератора для 'cast':")
for cast in cast_entries:
    print(cast)

print("\nКількість дорослих шоу/фільмів (isAdult == 1):", adult_count)
print("Середній рейтинг шоу/фільмів із більше ніж 1000 голосами:", average_rating)

print("\nЗаголовки шоу з більше ніж 10 епізодами та рейтингом вище середнього:")
for title in titles_with_conditions[:10]:
    print(title)
