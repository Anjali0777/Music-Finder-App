import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_PATH = "music.db"  # path to your SQLite database


# ----------------------------
# Database Helper Functions
# ----------------------------
def execute_query(query, params=(), fetch=False):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, params)
    if fetch:
        result = cursor.fetchall()
    else:
        result = None
    conn.commit()
    conn.close()
    return result


# ----------------------------
# Tkinter GUI
# ----------------------------
class MusicDBApp:
    def __init__(self, root):
        self.root = root
        root.title("Music Database Interface")
        root.geometry("900x600")

        tab_control = ttk.Notebook(root)

        # Tabs
        self.tab_insert_artist = ttk.Frame(tab_control)
        self.tab_search_album = ttk.Frame(tab_control)
        self.tab_playlist_view = ttk.Frame(tab_control)
        self.tab_artist_from_track = ttk.Frame(tab_control)
        self.tab_track_stats = ttk.Frame(tab_control)
        self.tab_artist_album_track = ttk.Frame(tab_control)
        self.tab_playlist_by_date = ttk.Frame(tab_control)
        self.tab_top_artist = ttk.Frame(tab_control)
        self.tab_duplicate_tracks = ttk.Frame(tab_control)
        self.tab_nested_query = ttk.Frame(tab_control)
        self.tab_avg_duration = ttk.Frame(tab_control)
        self.tab_delete_track = ttk.Frame(tab_control)

        tabs = [
            ("Insert Artist", self.tab_insert_artist),
            ("Search Album", self.tab_search_album),
            ("Playlist View", self.tab_playlist_view),
            ("Artist from Track", self.tab_artist_from_track),
            ("Tracks per Genre", self.tab_track_stats),
            ("Artists w/ Album & Track", self.tab_artist_album_track),
            ("Playlists by Date", self.tab_playlist_by_date),
            ("Top Artist", self.tab_top_artist),
            ("Duplicate Tracks", self.tab_duplicate_tracks),
            ("Nested Query Artist", self.tab_nested_query),
            ("Avg Track Duration", self.tab_avg_duration),
            ("Delete Track", self.tab_delete_track)
        ]

        for title, frame in tabs:
            tab_control.add(frame, text=title)

        tab_control.pack(expand=1, fill="both")
        self.create_insert_artist_tab()
        self.create_search_album_tab()
        self.create_playlist_view_tab()
        self.create_artist_from_track_tab()
        self.create_track_stats_tab()
        self.create_artist_album_track_tab()
        self.create_playlist_by_date_tab()
        self.create_top_artist_tab()
        self.create_duplicate_tracks_tab()
        self.create_nested_query_tab()
        self.create_avg_duration_tab()
        self.create_delete_track_tab()

    # ----------------------------
    # Tab Implementations
    # ----------------------------

    # Tab 1: Insert Artist
    def create_insert_artist_tab(self):
        ttk.Label(self.tab_insert_artist, text="Artist Name:").grid(row=0, column=0, padx=5, pady=5)
        self.artist_name_entry = ttk.Entry(self.tab_insert_artist, width=50)
        self.artist_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.tab_insert_artist, text="Album Name:").grid(row=1, column=0, padx=5, pady=5)
        self.album_name_entry = ttk.Entry(self.tab_insert_artist, width=50)
        self.album_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.tab_insert_artist, text="Insert", command=self.insert_artist_album).grid(row=2, column=1,
                                                                                                 pady=10)

    def insert_artist_album(self):
        artist_name = self.artist_name_entry.get().strip()
        album_name = self.album_name_entry.get().strip()
        if not artist_name or not album_name:
            messagebox.showwarning("Input Error", "Please enter both artist and album name.")
            return

        # Insert artist
        execute_query("INSERT OR IGNORE INTO Artist (Name) VALUES (?)", (artist_name,))
        artist_id = execute_query("SELECT ArtistID FROM Artist WHERE Name=?", (artist_name,), fetch=True)[0][0]

        # Insert album
        execute_query("INSERT OR IGNORE INTO Album (Name) VALUES (?)", (album_name,))
        album_id = execute_query("SELECT AlbumID FROM Album WHERE Name=?", (album_name,), fetch=True)[0][0]

        # Link artist and album
        execute_query("INSERT OR IGNORE INTO ArtistAlbum (ArtistID, AlbumID) VALUES (?, ?)", (artist_id, album_id))

        messagebox.showinfo("Success", f"Inserted artist '{artist_name}' with album '{album_name}'.")

    # Tab 2: Search Album by AlbumID
    def create_search_album_tab(self):
        ttk.Label(self.tab_search_album, text="Album ID:").grid(row=0, column=0, padx=5, pady=5)
        self.album_id_entry = ttk.Entry(self.tab_search_album, width=30)
        self.album_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.tab_search_album, text="Search", command=self.search_album).grid(row=1, column=1, pady=10)
        self.album_result = ttk.Label(self.tab_search_album, text="")
        self.album_result.grid(row=2, column=0, columnspan=2, pady=10)

    def search_album(self):
        album_id = self.album_id_entry.get().strip()
        if not album_id:
            messagebox.showwarning("Input Error", "Please enter Album ID.")
            return
        result = execute_query("SELECT Name FROM Album WHERE AlbumID=?", (album_id,), fetch=True)
        if result:
            self.album_result.config(text=f"Album Name: {result[0][0]}")
        else:
            self.album_result.config(text="Album not found.")

    # Tab 3: Playlist View (List all Tracks in Playlist)
    def create_playlist_view_tab(self):
        ttk.Label(self.tab_playlist_view, text="Playlist ID:").grid(row=0, column=0, padx=5, pady=5)
        self.playlist_id_entry = ttk.Entry(self.tab_playlist_view, width=30)
        self.playlist_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.tab_playlist_view, text="Show Tracks", command=self.show_playlist_tracks).grid(row=1, column=1,
                                                                                                       pady=10)
        self.playlist_tracks_text = tk.Text(self.tab_playlist_view, width=80, height=20)
        self.playlist_tracks_text.grid(row=2, column=0, columnspan=2, pady=10)

    def show_playlist_tracks(self):
        pid = self.playlist_id_entry.get().strip()
        if not pid:
            messagebox.showwarning("Input Error", "Please enter Playlist ID.")
            return
        query = """
        SELECT Track.Name 
        FROM Track
        JOIN TrackPlaylist ON Track.TrackID = TrackPlaylist.TrackID
        WHERE TrackPlaylist.PlaylistID = ?
        """
        results = execute_query(query, (pid,), fetch=True)
        self.playlist_tracks_text.delete("1.0", tk.END)
        if results:
            for t in results:
                self.playlist_tracks_text.insert(tk.END, f"{t[0]}\n")
        else:
            self.playlist_tracks_text.insert(tk.END, "No tracks found in this playlist.")

    # Tab 4: Artist from TrackID
    def create_artist_from_track_tab(self):
        ttk.Label(self.tab_artist_from_track, text="Track ID:").grid(row=0, column=0, padx=5, pady=5)
        self.track_id_entry = ttk.Entry(self.tab_artist_from_track, width=30)
        self.track_id_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.tab_artist_from_track, text="Find Artist", command=self.find_artist_from_track).grid(row=1,
                                                                                                             column=1,
                                                                                                             pady=10)
        self.artist_result_label = ttk.Label(self.tab_artist_from_track, text="")
        self.artist_result_label.grid(row=2, column=0, columnspan=2, pady=10)

    def find_artist_from_track(self):
        tid = self.track_id_entry.get().strip()
        if not tid:
            messagebox.showwarning("Input Error", "Please enter Track ID.")
            return
        query = """
        SELECT Artist.Name 
        FROM Artist
        JOIN ArtistTrack ON Artist.ArtistID = ArtistTrack.ArtistID
        WHERE ArtistTrack.TrackID = ?
        """
        result = execute_query(query, (tid,), fetch=True)
        if result:
            self.artist_result_label.config(text=f"Artist: {result[0][0]}")
        else:
            self.artist_result_label.config(text="Artist not found.")

    # Tab 5: Tracks per Genre (Stats)
    def create_track_stats_tab(self):
        ttk.Button(self.tab_track_stats, text="Show Tracks per Genre", command=self.show_tracks_per_genre).pack(pady=10)
        self.genre_text = tk.Text(self.tab_track_stats, width=80, height=25)
        self.genre_text.pack(pady=10)

    def show_tracks_per_genre(self):
        query = "SELECT Genre, COUNT(*) FROM Track GROUP BY Genre"
        results = execute_query(query, fetch=True)
        self.genre_text.delete("1.0", tk.END)
        for genre, count in results:
            self.genre_text.insert(tk.END, f"{genre}: {count}\n")

    # Tab 6: Artists with Album & Track
    def create_artist_album_track_tab(self):
        ttk.Button(self.tab_artist_album_track, text="Show Artists w/ Album & Track",
                   command=self.show_artists_album_track).pack(pady=10)
        self.artist_album_track_text = tk.Text(self.tab_artist_album_track, width=80, height=25)
        self.artist_album_track_text.pack(pady=10)

    def show_artists_album_track(self):
        query = """
        SELECT DISTINCT Artist.Name 
        FROM Artist
        JOIN ArtistAlbum ON Artist.ArtistID = ArtistAlbum.ArtistID
        JOIN ArtistTrack ON Artist.ArtistID = ArtistTrack.ArtistID
        """
        results = execute_query(query, fetch=True)
        self.artist_album_track_text.delete("1.0", tk.END)
        for r in results:
            self.artist_album_track_text.insert(tk.END, f"{r[0]}\n")

    # Tab 7: Playlists by CreatedDate
    def create_playlist_by_date_tab(self):
        ttk.Label(self.tab_playlist_by_date, text="Created After (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.created_date_entry = ttk.Entry(self.tab_playlist_by_date, width=30)
        self.created_date_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.tab_playlist_by_date, text="Show Playlists", command=self.show_playlists_by_date).grid(row=1,
                                                                                                               column=1,
                                                                                                               pady=10)
        self.playlist_date_text = tk.Text(self.tab_playlist_by_date, width=80, height=25)
        self.playlist_date_text.grid(row=2, column=0, columnspan=2, pady=10)

    def show_playlists_by_date(self):
        date = self.created_date_entry.get().strip()
        query = "SELECT Name, CreatedDate FROM Playlist WHERE CreatedDate > ?"
        results = execute_query(query, (date,), fetch=True)
        self.playlist_date_text.delete("1.0", tk.END)
        for name, created in results:
            self.playlist_date_text.insert(tk.END, f"{name} ({created})\n")

    # Tab 8: Artist with Most Tracks
    def create_top_artist_tab(self):
        ttk.Button(self.tab_top_artist, text="Show Artist with Most Tracks", command=self.show_top_artist).pack(pady=10)
        self.top_artist_text = tk.Text(self.tab_top_artist, width=80, height=25)
        self.top_artist_text.pack(pady=10)

    def show_top_artist(self):
        query = """
        SELECT Name FROM Artist
        WHERE ArtistID = (
            SELECT ArtistID FROM ArtistTrack
            GROUP BY ArtistID
            ORDER BY COUNT(TrackID) DESC
            LIMIT 1
        )
        """
        result = execute_query(query, fetch=True)
        self.top_artist_text.delete("1.0", tk.END)
        if result:
            self.top_artist_text.insert(tk.END, f"Top Artist: {result[0][0]}")
        else:
            self.top_artist_text.insert(tk.END, "No data found.")

    # Tab 9: Duplicate Tracks
    def create_duplicate_tracks_tab(self):
        ttk.Button(self.tab_duplicate_tracks, text="Find Duplicate Tracks", command=self.show_duplicate_tracks).pack(
            pady=10)
        self.duplicate_text = tk.Text(self.tab_duplicate_tracks, width=80, height=25)
        self.duplicate_text.pack(pady=10)

    def show_duplicate_tracks(self):
        query = """
        SELECT t1.Name, t1.DurationMs
        FROM Track t1
        JOIN Track t2 ON t1.Name = t2.Name AND t1.DurationMs = t2.DurationMs AND t1.TrackID != t2.TrackID
        GROUP BY t1.Name, t1.DurationMs
        """
        results = execute_query(query, fetch=True)
        self.duplicate_text.delete("1.0", tk.END)
        for name, duration in results:
            self.duplicate_text.insert(tk.END, f"{name} ({duration} ms)\n")

    # Tab 10: Nested Query Artist (Tracks not in playlist)
    def create_nested_query_tab(self):
        ttk.Button(self.tab_nested_query, text="Find Artists w/ Tracks Not in Playlist",
                   command=self.show_nested_artists).pack(pady=10)
        self.nested_text = tk.Text(self.tab_nested_query, width=80, height=25)
        self.nested_text.pack(pady=10)

    def show_nested_artists(self):
        query = """
        SELECT DISTINCT a.Name
        FROM Artist a
        JOIN ArtistTrack at ON a.ArtistID = at.ArtistID
        JOIN Track t ON at.TrackID = t.TrackID
        WHERE t.Genre != 'something' AND t.TrackID NOT IN (SELECT TrackID FROM TrackPlaylist)
        """
        results = execute_query(query, fetch=True)
        self.nested_text.delete("1.0", tk.END)
        for r in results:
            self.nested_text.insert(tk.END, f"{r[0]}\n")

    # Tab 11: Average Track Duration
    def create_avg_duration_tab(self):
        ttk.Button(self.tab_avg_duration, text="Show Artists Above Avg Duration", command=self.show_avg_duration).pack(
            pady=10)
        self.avg_text = tk.Text(self.tab_avg_duration, width=80, height=25)
        self.avg_text.pack(pady=10)

    def show_avg_duration(self):
        query = """
        SELECT Artist.Name
        FROM Artist
        JOIN ArtistTrack ON Artist.ArtistID = ArtistTrack.ArtistID
        JOIN Track ON ArtistTrack.TrackID = Track.TrackID
        GROUP BY Artist.ArtistID
        HAVING AVG(Track.DurationMs) > (SELECT AVG(DurationMs) FROM Track)
        """
        results = execute_query(query, fetch=True)
        self.avg_text.delete("1.0", tk.END)
        for r in results:
            self.avg_text.insert(tk.END, f"{r[0]}\n")

    # Tab 12: Delete Track
    def create_delete_track_tab(self):
        ttk.Label(self.tab_delete_track, text="Track ID:").grid(row=0, column=0, padx=5, pady=5)
        self.del_track_entry = ttk.Entry(self.tab_delete_track, width=30)
        self.del_track_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.tab_delete_track, text="Delete Track", command=self.delete_track).grid(row=1, column=1, pady=10)

    def delete_track(self):
        tid = self.del_track_entry.get().strip()
        if not tid:
            messagebox.showwarning("Input Error", "Please enter Track ID.")
            return
        execute_query("DELETE FROM Track WHERE TrackID=?", (tid,))
        execute_query("DELETE FROM ArtistTrack WHERE TrackID=?", (tid,))
        execute_query("DELETE FROM TrackPlaylist WHERE TrackID=?", (tid,))
        messagebox.showinfo("Success", f"Track {tid} deleted.")


# ----------------------------
# Run the App
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicDBApp(root)
    root.mainloop()
