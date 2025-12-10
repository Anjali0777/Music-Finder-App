# Frontend.py

import tkinter as tk
from tkinter import ttk, messagebox
import Backend

class MusicDBApp:
    def __init__(self, root):
        self.root = root
        root.title("Music Database Interface")
        root.geometry("900x600")

        tab_control = ttk.Notebook(root)

        # Tabs
        self.tab_create_playlist = ttk.Frame(tab_control)
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
            ("Create Playlist", self.tab_create_playlist),
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

        # Build tabs
        self.create_create_playlist_tab()
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

    # Tab 1: Create Playlist
    def create_create_playlist_tab(self):
        ttk.Label(self.tab_create_playlist, text="Playlist Name: ").grid(row=0, column=0, padx=5, pady=5)
        self.new_playlist_entry = ttk.Entry(self.tab_create_playlist, width=50)
        self.new_playlist_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.tab_create_playlist, text="Created Date (YYYY-MM-DD): ").grid(row=1, column=0, padx=5, pady=5)
        self.new_playlist_date_entry = ttk.Entry(self.tab_create_playlist, width=50)
        self.new_playlist_date_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(
            self.tab_create_playlist,
            text="Create Playlist",
            command=self.create_playlist
        ).grid(row=2, column=1, pady=10)

        # Add Tracks to Playlist
        ttk.Label(self.tab_create_playlist, text="Add Tracks to Playlist").grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Label(self.tab_create_playlist, text="Select Playlist: ").grid(row=4, column=0, padx=5, pady=5)
        self.playlist_selector = ttk.Combobox(self.tab_create_playlist, width=40)
        self.playlist_selector.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.tab_create_playlist, text="Select Track: ").grid(row=5, column=0, padx=5, pady=5)
        self.track_selector = ttk.Combobox(self.tab_create_playlist, width=40)
        self.track_selector.grid(row=5, column=1, padx=5, pady=5)

        ttk.Button(self.tab_create_playlist, text="Add Track to Playlist", command=self.add_track_to_playlist).grid(row=6, column=1, pady=10)

        self.refresh_playlist_dropdown()
        self.refresh_track_dropdown()

    def refresh_playlist_dropdown(self):
        names = Backend.get_playlist_names()
        self.playlist_selector["values"] = names

    def refresh_track_dropdown(self):
        names = Backend.get_track_names()
        self.track_selector["values"] = names

    def create_playlist(self):
        pname = self.new_playlist_entry.get().strip()
        pdate = self.new_playlist_date_entry.get().strip()

        if not pname:
            messagebox.showwarning("Input Error", "Please enter playlist name")
            return

        if not pdate:
            import datetime
            pdate = str(datetime.date.today())

        Backend.create_playlist(pname, pdate)
        messagebox.showinfo("Success", f"Playlist '{pname}' created successfully")
        self.refresh_playlist_dropdown()

    def add_track_to_playlist(self):
        playlist_name = self.playlist_selector.get()
        track_name = self.track_selector.get()

        if not playlist_name or not track_name:
            messagebox.showwarning("Input Error", "Please select playlist and track.")
            return

        pid = Backend.get_playlist_id_by_name(playlist_name)
        tid = Backend.get_track_id_by_name(track_name)

        if pid is None or tid is None:
            messagebox.showerror("Error", "Could not find playlist or track IDs")
            return

        Backend.add_track_to_playlist(pid, tid)
        messagebox.showinfo("Success", f"Added '{track_name}' to playlist '{playlist_name}'.")

    # Tab 2: Insert Artist
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

        Backend.insert_artist_with_album(artist_name, album_name)
        messagebox.showinfo("Success", f"Inserted artist '{artist_name}' with album '{album_name}'.")

    # Tab 3: Search Album by AlbumID
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
        result = Backend.search_album_by_id(album_id)
        if result:
            self.album_result.config(text=f"Album Name: {result}")
        else:
            self.album_result.config(text="Album not found.")

    # Tab 4: Playlist View (List all Tracks in Playlist)
    def create_playlist_view_tab(self):
        ttk.Label(self.tab_playlist_view, text="Playlist Name:").grid(row=0, column=0, padx=5, pady=5)
        self.playlist_name_entry = ttk.Entry(self.tab_playlist_view, width=30)
        self.playlist_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.tab_playlist_view, text="Show Tracks", command=self.show_playlist_tracks).grid(row=1, column=1,
                                                                                                       pady=10)
        self.playlist_tracks_text = tk.Text(self.tab_playlist_view, width=80, height=20)
        self.playlist_tracks_text.grid(row=2, column=0, columnspan=2, pady=10)

    def show_playlist_tracks(self):
        pname = self.playlist_name_entry.get().strip()
        if not pname:
            messagebox.showwarning("Input Error", "Please enter Playlist Name.")
            return
        results = Backend.get_tracks_in_playlist_by_name(pname)
        self.playlist_tracks_text.delete("1.0", tk.END)
        if results:
            for t in results:
                self.playlist_tracks_text.insert(tk.END, f"{t}")
        else:
            self.playlist_tracks_text.insert(tk.END, "No tracks found in this playlist.")

    # Tab 5: Artist from TrackID
    def create_artist_from_track_tab(self):
        ttk.Label(self.tab_artist_from_track, text="Track Name:").grid(row=0, column=0, padx=5, pady=5)
        self.track_name_entry = ttk.Entry(self.tab_artist_from_track, width=30)
        self.track_name_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.tab_artist_from_track, text="Find Artist", command=self.find_artist_from_track).grid(row=1,
                                                                                                             column=1,
                                                                                                             pady=10)
        self.artist_result_label = ttk.Label(self.tab_artist_from_track, text="")
        self.artist_result_label.grid(row=2, column=0, columnspan=2, pady=10)

    def find_artist_from_track(self):
        tname = self.track_name_entry.get().strip()
        if not tname:
            messagebox.showwarning("Input Error", "Please enter Track Name.")
            return
        result = Backend.find_artist_by_track_name(tname)
        if result:
            self.artist_result_label.config(text=f"Artist: {result}")
        else:
            self.artist_result_label.config(text="Artist not found.")

    # Tab 6: Tracks per Genre (Stats)
    def create_track_stats_tab(self):
        ttk.Button(self.tab_track_stats, text="Show Tracks per Genre", command=self.show_tracks_per_genre).pack(pady=10)
        self.genre_text = tk.Text(self.tab_track_stats, width=80, height=25)
        self.genre_text.pack(pady=10)

    def show_tracks_per_genre(self):
        results = Backend.tracks_per_genre()
        self.genre_text.delete("1.0", tk.END)
        for genre, count in results:
            self.genre_text.insert(tk.END, f"{genre}: {count}\n")

    # Tab 7: Artists with Album & Track
    def create_artist_album_track_tab(self):
        ttk.Button(self.tab_artist_album_track, text="Show Artists w/ Album & Track",
                   command=self.show_artists_album_track).pack(pady=10)
        self.artist_album_track_text = tk.Text(self.tab_artist_album_track, width=80, height=25)
        self.artist_album_track_text.pack(pady=10)

    def show_artists_album_track(self):
        results = Backend.artists_with_album_and_track()
        self.artist_album_track_text.delete("1.0", tk.END)
        for r in results:
            self.artist_album_track_text.insert(tk.END, f"{r}\n")

    # Tab 8: Playlists by CreatedDate
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
        results = Backend.get_playlists_after_date(date)
        self.playlist_date_text.delete("1.0", tk.END)
        for name, created in results:
            self.playlist_date_text.insert(tk.END, f"{name} ({created})\n")

    # Tab 9: Artist with Most Tracks
    def create_top_artist_tab(self):
        ttk.Button(self.tab_top_artist, text="Show Artist with Most Tracks", command=self.show_top_artist).pack(pady=10)
        self.top_artist_text = tk.Text(self.tab_top_artist, width=80, height=25)
        self.top_artist_text.pack(pady=10)

    def show_top_artist(self):
        result = Backend.top_artist()
        self.top_artist_text.delete("1.0", tk.END)
        if result:
            self.top_artist_text.insert(tk.END, f"Top Artist: {result}")
        else:
            self.top_artist_text.insert(tk.END, "No data found.")

    # Tab 10: Duplicate Tracks
    def create_duplicate_tracks_tab(self):
        ttk.Button(self.tab_duplicate_tracks, text="Find Duplicate Tracks", command=self.show_duplicate_tracks).pack(
            pady=10)
        self.duplicate_text = tk.Text(self.tab_duplicate_tracks, width=80, height=25)
        self.duplicate_text.pack(pady=10)

    def show_duplicate_tracks(self):
        results = Backend.find_duplicate_tracks()
        self.duplicate_text.delete("1.0", tk.END)
        for name, duration in results:
            self.duplicate_text.insert(tk.END, f"{name} ({duration} ms)\n")

    # Tab 11: Nested Query Artist (Tracks not in playlist)
    def create_nested_query_tab(self):
        ttk.Label(self.tab_nested_query, text="Genre:").grid(row=0, column=0, padx=5, pady=5)
        self.nested_query_entry = ttk.Entry(self.tab_nested_query, width=30)
        self.nested_query_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.tab_nested_query, text="Find Artists w/ Tracks of entered genre Not in Playlist", command=self.show_nested_artists).grid(row=1, column=1, pady=10)

        self.nested_text = tk.Text(self.tab_nested_query, width=80, height=25)
        self.nested_text.grid(row=2, column=1, pady=10)

    def show_nested_artists(self):
        gname = self.nested_query_entry.get()
        if not gname:
            messagebox.showwarning("Input Error", "Please enter Genre")
            return
        results = Backend.nested_artists_not_in_playlist(gname)

        artists = {}

        for artist, track in results:
            artists.setdefault(artist, []).append(track)

        self.nested_text.delete("1.0", tk.END)
        for artist, tracks in artists.items():
            self.nested_text.insert(tk.END, f"{artist}:\n")
            for track in tracks:
                self.nested_text.insert(tk.END, f"  - {track}\n")
            self.nested_text.insert(tk.END, "")

    # Tab 12: Average Track Duration
    def create_avg_duration_tab(self):
        ttk.Button(self.tab_avg_duration, text="Show Artists Above Avg Duration", command=self.show_avg_duration).pack(
            pady=10)
        self.avg_text = tk.Text(self.tab_avg_duration, width=80, height=25)
        self.avg_text.pack(pady=10)

    def show_avg_duration(self):
        results = Backend.artists_above_avg_duration()
        self.avg_text.delete("1.0", tk.END)

        for name, avg_duration in results:
            minutes = int(avg_duration // 60000)
            seconds = int((avg_duration % 60000) // 1000)

            self.avg_text.insert(tk.END, f"{name} - Average Duration: {minutes}:{seconds:02d}\n")

    # Tab 13: Delete Track
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
        Backend.delete_track_by_id(tid)
        messagebox.showinfo("Success", f"Track {tid} deleted.")


# ----------------------------
# Run the App
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicDBApp(root)
    root.mainloop()
