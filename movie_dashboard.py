import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, END, BOTH, Label

# Load Dataset
try:
    # Replace this path with the correct path to your CSV file
    file_path = r'C:/Users/AYUSHMAAN/Desktop/imdb_top_1000.csv'
    imdb_data = pd.read_csv(file_path)
    # Clean and process data
    imdb_data['Released_Year'] = pd.to_numeric(imdb_data['Released_Year'], errors='coerce')
    imdb_data = imdb_data.dropna(subset=['Released_Year']).reset_index(drop=True)
except Exception as e:
    print(f"Error loading dataset: {e}")
    imdb_data = pd.DataFrame()

# Functions for Visualizations
def show_genre_distribution():
    print("Displaying genre distribution...")
    genres = imdb_data['Genre'].str.split(', ').dropna()
    all_genres = [genre for sublist in genres for genre in sublist]
    genre_counts = pd.Series(all_genres).value_counts()

    if genre_counts.empty:
        display_message("No genre data available.")
        return

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=genre_counts.values[:10], y=genre_counts.index[:10], palette='viridis', ax=ax)
    ax.set_title('Top 10 Movie Genres')
    ax.set_xlabel('Number of Movies')
    ax.set_ylabel('Genre')
    display_plot(fig)

def show_release_year_trend():
    print("Displaying release year trend...")
    movies_by_year = imdb_data['Released_Year'].value_counts().sort_index()

    if movies_by_year.empty:
        display_message("No release year data available.")
        return

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(movies_by_year.index, movies_by_year.values, marker='o', linestyle='-', color='blue')
    ax.set_title('Movies Released Over Time')
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Movies')
    ax.grid(True)
    display_plot(fig)

def show_top_directors():
    print("Displaying top directors...")
    top_directors = imdb_data['Director'].value_counts().head(10)

    if top_directors.empty:
        display_message("No director data available.")
        return

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=top_directors.values, y=top_directors.index, palette='mako', ax=ax)
    ax.set_title('Top 10 Directors')
    ax.set_xlabel('Number of Movies')
    ax.set_ylabel('Director')
    display_plot(fig)

def show_ratings_distribution():
    print("Displaying ratings distribution...")
    if imdb_data['IMDB_Rating'].isnull().all():
        display_message("No ratings data available.")
        return

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.histplot(imdb_data['IMDB_Rating'], bins=10, kde=True, color='orange', ax=ax)
    ax.set_title('Distribution of IMDb Ratings')
    ax.set_xlabel('IMDb Rating')
    ax.set_ylabel('Frequency')
    display_plot(fig)

def filter_movies_by_genre():
    print("Filtering movies by genre...")
    selected_genre = genre_var.get()
    filtered_movies = imdb_data[imdb_data['Genre'].str.contains(selected_genre, na=False, case=False)]

    for widget in table_frame.winfo_children():
        widget.destroy()

    if not filtered_movies.empty:
        table = ttk.Treeview(table_frame, columns=("Title", "Rating", "Year"), show='headings', height=10)
        table.heading("Title", text="Series Title")
        table.heading("Rating", text="IMDB Rating")
        table.heading("Year", text="Released Year")
        
        # Adding rows to the table
        for _, row in filtered_movies[['Series_Title', "IMDB_Rating", 'Released_Year']].iterrows():
            table.insert("", END, values=(row['Series_Title'], row['IMDB_Rating'], int(row['Released_Year'])))
        table.pack(fill=BOTH, expand=True)
    else:
        Label(table_frame, text="No Movies Found in Selected Genre!", fg="red", font=("Arial", 12)).pack()

def display_plot(fig):
    # Clear previous plots
    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

def display_message(message):
    for widget in plot_frame.winfo_children():
        widget.destroy()
    Label(plot_frame, text=message, fg="red", font=("Arial", 14)).pack()

# Main Window
root = tk.Tk()
root.title("Movie Analytics Dashboard")
root.geometry("1200x800")
root.configure(bg="#d6eaf3")  # Light blue background

# Title
title_label = tk.Label(root, text="🎬 Movie Analytics Dashboard", font=("Arial", 20, "bold"), bg="#d6eaf3", fg="black")
title_label.pack(pady=20)

# Button Frame
button_frame = tk.Frame(root, bg="#d6eaf3")
button_frame.pack(pady=10)

ttk.Button(button_frame, text="Genre Distribution", command=show_genre_distribution).grid(row=0, column=0, padx=15, pady=10)
ttk.Button(button_frame, text="Release Year Trend", command=show_release_year_trend).grid(row=0, column=1, padx=15, pady=10)
ttk.Button(button_frame, text="Top Directors", command=show_top_directors).grid(row=0, column=2, padx=15, pady=10)
ttk.Button(button_frame, text="Ratings Distribution", command=show_ratings_distribution).grid(row=0, column=3, padx=15, pady=10)

# Filter Movies by Genre
filter_frame = tk.Frame(root, bg="#d6eaf3")
filter_frame.pack(pady=20)

genre_label = tk.Label(filter_frame, text="Select Genre:", font=("Arial", 14), bg="#d6eaf3")
genre_label.pack(side=tk.LEFT, padx=10)

genre_var = tk.StringVar()
genres = imdb_data['Genre'].str.split(', ').dropna()
unique_genres = sorted(set([genre for sublist in genres for genre in sublist]))
genre_dropdown = ttk.Combobox(filter_frame, textvariable=genre_var, values=unique_genres, state="readonly", width=20, font=("Arial", 12))
genre_dropdown.pack(side=tk.LEFT, padx=10)

ttk.Button(filter_frame, text="Filter Movies", command=filter_movies_by_genre).pack(side=tk.LEFT, padx=10)

# Plot and Table Frames
plot_frame = tk.Frame(root, bg="#d6eaf3", width=1000, height=500)
plot_frame.pack(pady=20, fill=BOTH, expand=True)

table_frame = tk.Frame(root, bg="#d6eaf3", width=1000, height=300)
table_frame.pack(pady=20, fill=BOTH, expand=True)

root.mainloop()
