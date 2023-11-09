import tkinter as tk
from tkinter import messagebox
import requests

# Define the functions for fetching data from the API
def get_actor_id(api_key, actor_name):
    search_url = "<API_KEY>"

    params = {
        "api_key": api_key,
        "query": actor_name
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    if data['results']:
        return data['results'][0]['id']
    else:
        return None

def get_genre_id(api_key, genre_name):
    genres_url = "https://api.themoviedb.org/3/genre/movie/list"

    params = {
        "api_key": api_key,
        "language": "en-US"
    }

    response = requests.get(genres_url, params=params)
    data = response.json()

    for genre in data['genres']:
        if genre['name'].lower() == genre_name.lower():
            return genre['id']

    return None

def get_movie_suggestions(api_key, num_suggestions, genre=None, actor=None, rating=None, year=None):
    base_url = "https://api.themoviedb.org/3/discover/movie"

    params = {
        "api_key": api_key,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "vote_average.gte": rating,
        "primary_release_year": year,
        "with_genres": genre,
        "with_cast": actor,
        "page": 1
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    suggestions = []

    for movie in data['results']:
        suggestions.append({
            "title": movie['original_title'],
            "release_date": movie['release_date'],
            "overview": movie['overview']
        })

        if len(suggestions) == num_suggestions:
            break

    return suggestions

# Define the show_movie_suggestions function
def show_movie_suggestions():
    num_suggestions = int(num_suggestions_entry.get())
    genre = genre_entry.get()
    actor = actor_entry.get()
    rating_str = rating_entry.get()
    year = year_entry.get()

    actor_id = get_actor_id(api_key, actor)
    genre_id = get_genre_id(api_key, genre)

    if actor and not actor_id:
        messagebox.showerror("Error", "Actor not found")
        return

    if genre and not genre_id:
        messagebox.showerror("Error", "Genre not found")
        return

    # Check if rating_str is empty
    if rating_str:
        try:
            rating = float(rating_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid rating format")
            return
    else:
        rating = None

    movie_suggestions = get_movie_suggestions(api_key, num_suggestions, genre_id, actor_id, rating, year)

    suggestions_text.delete("1.0", tk.END)  # Clear previous suggestions

    for idx, suggestion in enumerate(movie_suggestions, start=1):
        suggestions_text.insert(tk.END, f"{idx}. {suggestion['title']} ({suggestion['release_date']}) - {suggestion['overview']}\n\n")

# Your API key
api_key = "<API_KEY>"

# Create the main window
root = tk.Tk()
root.title("Movie Suggestion System")

# Create and place GUI elements (labels, entries, button, text widget)
num_suggestions_label = tk.Label(root, text="Number of Suggestions:")
num_suggestions_entry = tk.Entry(root)

genre_label = tk.Label(root, text="Preferred Genre:")
genre_entry = tk.Entry(root)

actor_label = tk.Label(root, text="Actor:")
actor_entry = tk.Entry(root)

rating_label = tk.Label(root, text="Minimum IMDb Rating:")
rating_entry = tk.Entry(root)

year_label = tk.Label(root, text="Release Year:")
year_entry = tk.Entry(root)

get_suggestions_button = tk.Button(root, text="Get Suggestions", command=show_movie_suggestions)

suggestions_text = tk.Text(root, wrap=tk.WORD, height=15, width=60)

# Place elements on the grid
num_suggestions_label.grid(row=0, column=0, padx=10, pady=10)
num_suggestions_entry.grid(row=0, column=1, padx=10, pady=10)

genre_label.grid(row=1, column=0, padx=10, pady=10)
genre_entry.grid(row=1, column=1, padx=10, pady=10)

actor_label.grid(row=2, column=0, padx=10, pady=10)
actor_entry.grid(row=2, column=1, padx=10, pady=10)

rating_label.grid(row=3, column=0, padx=10, pady=10)
rating_entry.grid(row=3, column=1, padx=10, pady=10)

year_label.grid(row=4, column=0, padx=10, pady=10)
year_entry.grid(row=4, column=1, padx=10, pady=10)

get_suggestions_button.grid(row=5, columnspan=2, padx=10, pady=10)

suggestions_text.grid(row=6, columnspan=2, padx=10, pady=10)

# Start the GUI event loop
root.mainloop()
