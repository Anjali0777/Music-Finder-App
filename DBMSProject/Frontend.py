import tkinter as tk
from tkinter import ttk, messagebox
import Backend

class MusicApp:
    def __init__(self, root):
        self.root = root
        root.title("Music Finder App")
        root.geometry("900x600")

        # Notebook for tabs
        tab_control = ttk.Notebook(root)

        self.tab_home = ttk.Frame(tab_control)
        self.tab_search = ttk.Frame(tab_control)
        self.tab_create_delete = ttk.Frame(tab_control)

        tab_control.add(self.tab_home, text="Home")
        tab_control.add(self.tab_search, text="Search")
        tab_control.add(self.tab_create_delete, text="Create/Delete")
        tab_control.pack(expand=1, fill="both")

        self.create_home_tab()
        self.create_search_tab()
        self.create_create_delete_tab()

    # ----------------------------
    # Home Tab
    # ----------------------------
    def create_home_tab(self):
        ttk.Label(self.tab_home, text="Recommended Tracks", font=("Arial", 14)).pack(pady=10)
        self.recommendations_text = tk.Text(self.tab_home, width=100, height=25)
        self.recommendations_text.pack(pady=10)
        ttk.Button(self.tab_home, text="Show Recommendations", command=self.show_recommendations).pack(pady=5)

    def show_recommendations(self):
        self.recommendations_text.delete("1.0", tk.END)
        genre_tracks = Backend.get_top_tracks_dynamic(top_genres=3, top_tracks=5)

        for genre, tracks in genre_tracks:
            self.recommendations_text.insert(tk.END, f"--- Top 5 {genre} Tracks ---\n")
            if tracks:
                for name, popularity, album, artists in tracks:
                    self.recommendations_text.insert(tk.END, f"{name} | Album: {album} | Artists: {artists} | Popularity: {popularity}\n")
            else:
                self.recommendations_text.insert(tk.END, "No tracks found for this genre.\n")
            self.recommendations_text.insert(tk.END, "\n")

    # ----------------------------
    # Search Tab
    # ----------------------------
    def create_search_tab(self):
        ttk.Label(self.tab_search, text="Search Tracks, Albums, or Artists", font=("Arial", 14)).pack(pady=10)
        frame = ttk.Frame(self.tab_search)
        frame.pack(pady=5)

        ttk.Label(frame, text="Search: ").grid(row=0, column=0, padx=5)
        self.search_entry = ttk.Entry(frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5)

        ttk.Label(frame, text="Type: ").grid(row=0, column=2, padx=5)
        self.search_type = ttk.Combobox(frame, values=["Track", "Album", "Artist", "Genre"], width=15)
        self.search_type.current(0)
        self.search_type.grid(row=0, column=3, padx=5)

        ttk.Button(frame, text="Search", command=self.perform_search).grid(row=0, column=4, padx=5)
        self.search_results_text = tk.Text(self.tab_search, width=100, height=25)
        self.search_results_text.pack(pady=10)

    def perform_search(self):
        query = self.search_entry.get().strip()
        search_type = self.search_type.get()
        if not query:
            messagebox.showwarning("Input Error", "Please enter a search query.")
            return
        self.search_results_text.delete("1.0", tk.END)

        if search_type == "Track":
            results = Backend.search_track_by_name(query)
            for r in results:
                self.search_results_text.insert(tk.END, f"{r[1]} | Popularity: {r[5]} | Genre: {r[19]}\n")
        elif search_type == "Album":
            results = Backend.search_album_by_name(query)
            for album_id, album_name, track_name in results:
                self.search_results_text.insert(tk.END, f"Album: {album_name} (ID: {album_id}) - Track: {track_name}\n")
        elif search_type == "Artist":
            results = Backend.search_artist_by_name(query)
            for artist_id, artist_name, track_name in results:
                self.search_results_text.insert(tk.END, f"Artist: {artist_name} (ID: {artist_id}) - Track: {track_name}\n")
        elif search_type == "Genre":
            results = Backend.search_by_genre(query)
            for name, genre in results:
                self.search_results_text.insert(tk.END, f"{name} - Genre: {genre}\n")

    # ----------------------------
    # Create/Delete Tab
    # ----------------------------
    def create_create_delete_tab(self):
        frame = ttk.Frame(self.tab_create_delete)
        frame.pack(pady=10)

        ttk.Label(frame, text="Playlist Name: ").grid(row=0, column=0, padx=5, pady=5)
        self.playlist_name_entry = ttk.Entry(frame, width=40)
        self.playlist_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Created Date (YYYY-MM-DD): ").grid(row=1, column=0, padx=5, pady=5)
        self.playlist_date_entry = ttk.Entry(frame, width=40)
        self.playlist_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Create Playlist", command=self.create_playlist).grid(row=2, column=1, pady=10)

        ttk.Label(frame, text="Track ID to Delete: ").grid(row=3, column=0, padx=5, pady=5)
        self.track_id_entry = ttk.Entry(frame, width=40)
        self.track_id_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Delete Track", command=self.delete_track).grid(row=4, column=1, pady=10)

    def create_playlist(self):
        name = self.playlist_name_entry.get().strip()
        created_date = self.playlist_date_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter playlist name.")
            return
        if not created_date:
            import datetime
            created_date = str(datetime.date.today())
        Backend.create_playlist(name, created_date)
        messagebox.showinfo("Success", f"Playlist '{name}' created!")

    def delete_track(self):
        track_id = self.track_id_entry.get().strip()
        if not track_id:
            messagebox.showwarning("Input Error", "Please enter Track ID.")
            return
        Backend.delete_track(track_id)
        messagebox.showinfo("Success", f"Track {track_id} deleted!")

# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicApp(root)
    root.mainloop()
