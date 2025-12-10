import sqlite3

DB_PATH = "music.db"  # path to your SQLite database

# ----------------------------
# Database helper
# ----------------------------
def run_query(query, params=(), fetch=False):
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
# Recommendations
# ----------------------------
def get_top_tracks_dynamic(top_genres=3, top_tracks=5):
    """
    Returns a list of tuples (genre, [(track_name, popularity, album_name, artists), ...])
    """
    # Step 1: Top genres by track count
    genre_query = """
    SELECT Genre, COUNT(*) as TrackCount
    FROM Track
    GROUP BY Genre
    ORDER BY TrackCount DESC
    LIMIT ?
    """
    top_genres_list = run_query(genre_query, (top_genres,), fetch=True)

    results = []
    for genre, _ in top_genres_list:
        track_query = """
        SELECT Name, Popularity, AlbumID, TrackID
        FROM Track
        WHERE Genre = ?
        ORDER BY Popularity DESC
        LIMIT ?
        """
        tracks = run_query(track_query, (genre, top_tracks), fetch=True)

        # Fetch album names and artists for each track
        track_info = []
        for name, popularity, album_id, track_id in tracks:
            # Get album name
            album_name = run_query("SELECT Name FROM Album WHERE AlbumID=?", (album_id,), fetch=True)
            album_name = album_name[0][0] if album_name else "Unknown Album"
            # Get artists
            artist_names = run_query("""
                SELECT Artist.Name FROM Artist
                JOIN ArtistTrack ON Artist.ArtistID = ArtistTrack.ArtistID
                WHERE ArtistTrack.TrackID = ?
            """, (track_id,), fetch=True)
            artists = ", ".join([a[0] for a in artist_names]) if artist_names else "Unknown Artist"

            track_info.append((name, popularity, album_name, artists))

        results.append((genre, track_info))

    return results

# ----------------------------
# Search
# ----------------------------
def search_track_by_name(name):
    query = """
    SELECT * FROM Track WHERE Name LIKE ?
    """
    return run_query(query, ('%' + name + '%',), fetch=True)

def search_album_by_name(name):
    query = """
    SELECT Album.AlbumID, Album.Name, Track.Name
    FROM Album
    JOIN Track ON Album.AlbumID = Track.AlbumID
    WHERE Album.Name LIKE ?
    """
    return run_query(query, ('%' + name + '%',), fetch=True)

def search_artist_by_name(name):
    query = """
    SELECT Artist.ArtistID, Artist.Name, Track.Name
    FROM Artist
    JOIN ArtistTrack ON Artist.ArtistID = ArtistTrack.ArtistID
    JOIN Track ON ArtistTrack.TrackID = Track.TrackID
    WHERE Artist.Name LIKE ?
    """
    return run_query(query, ('%' + name + '%',), fetch=True)

def search_by_genre(genre):
    query = """
    SELECT Name, Genre FROM Track WHERE Genre LIKE ?
    """
    return run_query(query, ('%' + genre + '%',), fetch=True)

# ----------------------------
# Create/Delete
# ----------------------------
def create_playlist(name, created_date):
    query = """
    INSERT INTO Playlist (Name, CreatedDate) VALUES (?, ?)
    """
    run_query(query, (name, created_date))

def delete_track(track_id):
    run_query("DELETE FROM Track WHERE TrackID=?", (track_id,))
    run_query("DELETE FROM ArtistTrack WHERE TrackID=?", (track_id,))
    run_query("DELETE FROM TrackPlaylist WHERE TrackID=?", (track_id,))
