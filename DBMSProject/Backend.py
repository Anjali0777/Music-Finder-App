# Backend.py
import sqlite3

DB_PATH = "music.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


# Helper: run query
def _run(query, params=(), fetch=False, many=False):
    conn = get_connection()
    cur = conn.cursor()
    if many:
        cur.executemany(query, params)
        res = None
    else:
        cur.execute(query, params)
        res = cur.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return res


# Playlist functions
def create_playlist(name, created_date):
    _run("INSERT OR IGNORE INTO Playlist (Name, CreatedDate) VALUES (?, ?)", (name, created_date))


def get_playlist_names():
    rows = _run("SELECT Name FROM Playlist", fetch=True)
    return [r[0] for r in rows] if rows else []


def get_playlist_id_by_name(name):
    r = _run("SELECT PlaylistID FROM Playlist WHERE Name=?", (name,), fetch=True)
    return r[0][0] if r else None


# Track functions
def get_track_names():
    rows = _run("SELECT Name FROM Track", fetch=True)
    return [r[0] for r in rows] if rows else []


def get_track_id_by_name(name):
    r = _run("SELECT TrackID FROM Track WHERE Name=?", (name,), fetch=True)
    return r[0][0] if r else None


def add_track_to_playlist(playlist_id, track_id):
    _run("INSERT OR IGNORE INTO TrackPlaylist (PlaylistID, TrackID) VALUES (?, ?)", (playlist_id, track_id))


# Insert artist and album
def insert_artist_with_album(artist_name, album_name):
    _run("INSERT OR IGNORE INTO Artist (Name) VALUES (?)", (artist_name,))
    artist_id = _run("SELECT ArtistID FROM Artist WHERE Name=?", (artist_name,), fetch=True)[0][0]

    _run("INSERT OR IGNORE INTO Album (Name) VALUES (?)", (album_name,))
    album_id = _run("SELECT AlbumID FROM Album WHERE Name=?", (album_name,), fetch=True)[0][0]

    _run("INSERT OR IGNORE INTO ArtistAlbum (ArtistID, AlbumID) VALUES (?, ?)", (artist_id, album_id))
    return artist_id, album_id


# Search album by id
def search_album_by_id(album_id):
    r = _run("SELECT Name FROM Album WHERE AlbumID=?", (album_id,), fetch=True)
    return r[0][0] if r else None


# Playlist view: list tracks in playlist by playlist name
def get_tracks_in_playlist_by_name(playlist_name):
    query = """
    SELECT Track.Name
    FROM Track
    JOIN TrackPlaylist ON Track.TrackID = TrackPlaylist.TrackID
    JOIN Playlist ON TrackPlaylist.PlaylistID = Playlist.PlaylistID
    WHERE Playlist.Name = ?
    """
    rows = _run(query, (playlist_name,), fetch=True)
    return [r[0] for r in rows] if rows else []


# Find artist by track name
def find_artist_by_track_name(track_name):
    query = """
    SELECT Artist.Name
    FROM Artist
    JOIN ArtistTrack ON Artist.ArtistID = ArtistTrack.ArtistID
    JOIN Track ON ArtistTrack.TrackID = Track.TrackID
    WHERE Track.Name = ?
    LIMIT 1
    """
    r = _run(query, (track_name,), fetch=True)
    return r[0][0] if r else None


# Tracks per genre
def tracks_per_genre():
    r = _run("SELECT Genre, COUNT(*) FROM Track GROUP BY Genre", fetch=True)
    return r or []


# Artists with album and track
def artists_with_album_and_track():
    query = """
    SELECT DISTINCT Artist.Name
    FROM Artist
    JOIN ArtistAlbum ON Artist.ArtistID = ArtistAlbum.ArtistID
    JOIN ArtistTrack ON Artist.ArtistID = ArtistTrack.ArtistID
    """
    r = _run(query, fetch=True)
    return [x[0] for x in r] if r else []


# Playlists by date
def get_playlists_after_date(date_str):
    r = _run("SELECT Name, CreatedDate FROM Playlist WHERE CreatedDate > ?", (date_str,), fetch=True)
    return r or []


# Top artist (most tracks)
def top_artist():
    query = """
    SELECT Name FROM Artist a JOIN
    (
        SELECT ArtistID, COUNT(TrackID) AS TrackCount FROM ArtistTrack
        GROUP BY ArtistID
        ORDER BY TrackCount DESC
        LIMIT 1
    ) s ON a.ArtistID = s.ArtistID
    """
    r = _run(query, fetch=True)
    return r[0][0] if r else None


# Duplicate tracks
def find_duplicate_tracks():
    query = """
    SELECT t1.Name, t1.DurationMs
    FROM Track t1
    JOIN Track t2 ON t1.Name = t2.Name AND t1.DurationMs = t2.DurationMs AND t1.TrackID <> t2.TrackID
    GROUP BY t1.Name, t1.DurationMs
    """
    r = _run(query, fetch=True)
    return r or []


# Nested query: Artists with tracks of genre not in any playlist
def nested_artists_not_in_playlist(genre):
    query = """
    SELECT DISTINCT a.Name, t.Name
    FROM Artist a
    JOIN ArtistTrack at ON a.ArtistID = at.ArtistID
    JOIN Track t ON at.TrackID = t.TrackID
    WHERE t.Genre = ? AND t.TrackID NOT IN (SELECT TrackID FROM TrackPlaylist)
    ORDER BY a.name, t.name
    """
    r = _run(query, (genre,), fetch=True)
    return r or []


# Artists above average duration
def artists_above_avg_duration():
    query = """
    SELECT Artist.Name, AVG(Track.DurationMs) AS AvgDuration
    FROM Artist
    JOIN ArtistTrack ON Artist.ArtistID = ArtistTrack.ArtistID
    JOIN Track ON ArtistTrack.TrackID = Track.TrackID
    GROUP BY Artist.ArtistID
    HAVING AvgDuration > (SELECT AVG(DurationMs) FROM Track)
    """
    r = _run(query, fetch=True)
    return r or []


# Delete track (and related entries)
def delete_track_by_id(track_id):
    _run("DELETE FROM Track WHERE TrackID=?", (track_id,))
    _run("DELETE FROM ArtistTrack WHERE TrackID=?", (track_id,))
    _run("DELETE FROM TrackPlaylist WHERE TrackID=?", (track_id,))
