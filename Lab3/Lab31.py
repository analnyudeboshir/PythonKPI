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
valid_ratings = []
invalid_rows = []
for row in data:
    if len(row) > max(rating_index, num_votes_index):
        try:
            num_votes_valid = row[num_votes_index] and float(row[num_votes_index]) > 1000
            rating_valid = row[rating_index] and float(row[rating_index]) > 0
            if num_votes_valid and rating_valid:
                valid_ratings.append(float(row[rating_index]))
            else:
                invalid_rows.append(row)
        except ValueError:
            invalid_rows.append(row)



average_rating = sum(valid_ratings) / len(valid_ratings) if valid_ratings else 0.0

episodes_index = headers.index('episodes')
titles_with_conditions = [
    row[headers.index('title')] for row in data
    if len(row) > max(episodes_index, rating_index) and
    row[episodes_index] and row[episodes_index].isdigit() and int(row[episodes_index]) > 10 and
    row[rating_index] and float(row[rating_index]) > average_rating
]

print("\nПерші 10 записів з ітератора для 'cast':")
for cast in cast_entries:
    print(cast)

print("\nКількість дорослих шоу/фільмів (isAdult == 1):", adult_count)
print("Середній рейтинг шоу/фільмів із більше ніж 1000 голосами:", average_rating)

print("\nЗаголовки шоу з більше ніж 10 епізодами та рейтингом вище середнього:")
for title in titles_with_conditions[:10]:
    print(title)