import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt

# Fetch website content
url = "https://www.imdb.com/chart/top"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find list of movie links
movies_list = soup.find('tbody', class_='lister-list')
movies = []
for row in movies_list.find_all('tr'):
    title_col = row.find('td', class_='titleColumn')
    rating_col = row.find('td', class_='ratingColumn')
    title = title_col.a.text
    year = title_col.span.text.strip('()')
    rating = rating_col.strong.text
    movies.append({
        'title': title,
        'year': year,
        'rating': rating
    })

    if len(movies) == 20:
        break

# Sort movies by rating
movies_sorted = sorted(movies, key=lambda x: float(x['rating']), reverse=True)

# Create visualization
top_titles = [movie['title'] for movie in movies_sorted]
top_ratings = [float(movie['rating']) for movie in movies_sorted]

fig, ax = plt.subplots(figsize=(8, 10))
ax.barh(top_titles, top_ratings, height=0.5)
ax.invert_yaxis()
ax.set_xlabel('Rating')
ax.set_xlim(0, 10)
ax.set_xticks(range(0, 11))
ax.set_title('Top Rated Movies on IMDB')
plt.tight_layout()

# Save chart as PNG
fig.savefig('top_rated_movies.png')

# Save as CSV
with open('movies_scraped.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['title', 'year', 'rating']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for movie in movies_sorted:
        writer.writerow(movie)

print("Done")
