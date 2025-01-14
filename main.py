from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QTextEdit, QHBoxLayout, QFrame
from PyQt6.QtGui import QPixmap, QFont, QPalette, QColor, QDesktopServices
from PyQt6.QtCore import Qt, QUrl
from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get
from io import BytesIO
from PIL import Image
import webbrowser

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    try:
        auth_string = f"{client_id}:{client_secret}"
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
        url = "https://accounts.spotify.com/api/token"
        headers = {"Authorization": f"Basic {auth_base64}", "Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        result.raise_for_status()
        json_result = json.loads(result.content)
        return json_result["access_token"]
    except Exception as e:
        print(f"Error fetching token: {e}")
        return None

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def make_request(url, headers):
    try:
        result = get(url, headers=headers)
        result.raise_for_status()
        return json.loads(result.content)
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search?q={}&type=artist&limit=1".format(artist_name)
    headers = get_auth_header(token)
    data = make_request(url, headers)
    return data["artists"]["items"][0] if data and "artists" in data and "items" in data["artists"] and data["artists"]["items"] else None

def get_artist_details(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    return make_request(url, headers)

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    data = make_request(url, headers)
    return data["tracks"] if data and "tracks" in data else []

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album&limit=5"
    headers = get_auth_header(token)
    data = make_request(url, headers)
    return data["items"] if data and "items" in data else []

class SpotifyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Spotify Artist Search")
        self.setGeometry(0, 0, QApplication.primaryScreen().size().width(), 700)
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(20, 20, 20))
        self.setPalette(palette)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Enter Artist Name:")
        self.label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.label.setStyleSheet("color: white;")
        layout.addWidget(self.label)
        
        self.entry = QLineEdit()
        self.entry.setStyleSheet("background-color: white; color: black; padding: 5px;")
        layout.addWidget(self.entry)
        
        self.button = QPushButton("Search")
        self.button.setStyleSheet("background-color: #1DB954; color: white; font-weight: bold; padding: 10px;")
        self.button.clicked.connect(self.search_artist)
        layout.addWidget(self.button)
        
        self.artist_label = QLabel("Artist Info:")
        self.artist_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.artist_label.setStyleSheet("color: #1DB954; margin-top: 10px;")
        info_header_layout = QHBoxLayout()
        info_header_layout.addWidget(self.artist_label)
        self.artist_name_label = QLabel("")
        self.artist_name_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.artist_name_label.setStyleSheet("color: #1DB954; margin-left: 10px;")
        info_header_layout.addWidget(self.artist_name_label)
        layout.addLayout(info_header_layout)
        self.artist_name_label = QLabel("")
        self.artist_name_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.artist_name_label.setStyleSheet("color: white;")
        layout.addWidget(self.artist_name_label)
        
        info_layout = QHBoxLayout()
        
        self.image_label = QLabel()
        info_layout.addWidget(self.image_label)
        
        details_layout = QVBoxLayout()
        
        self.artist_details = QListWidget()
        details_layout.addWidget(self.artist_details)
        
        self.song_label = QLabel("Artist Top 10 Songs:")
        self.song_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.song_label.setStyleSheet("color: #1DB954; margin-top: 10px;")
        details_layout.addWidget(self.song_label)
        
        self.song_list = QListWidget()
        details_layout.addWidget(self.song_list)
        
        self.album_label = QLabel("Artist Recent Albums:")
        self.album_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.album_label.setStyleSheet("color: #1DB954; margin-top: 10px;")
        details_layout.addWidget(self.album_label)
        
        self.album_list = QListWidget()
        details_layout.addWidget(self.album_list)
        
        info_layout.addLayout(details_layout)
        layout.addLayout(info_layout)
        
        self.spotify_link = QLabel("Spotify Profile")
        self.spotify_link.setTextFormat(Qt.TextFormat.RichText)
        self.spotify_link.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.spotify_link.setOpenExternalLinks(True)
        self.spotify_link.setStyleSheet("color: #1DB954; font-size: 14px;")
        layout.addWidget(self.spotify_link)
        
        self.setLayout(layout)
    
    def search_artist(self):
        artist_name = self.entry.text()
        if not artist_name:
            QMessageBox.warning(self, "Input Error", "Please enter an artist name!")
            return
        
        token = get_token()
        if not token:
            QMessageBox.critical(self, "Error", "Failed to fetch Spotify token!")
            return
        
        artist = search_for_artist(token, artist_name)
        if not artist:
            QMessageBox.critical(self, "Not Found", "Artist not found!")
            return
        
        self.artist_name_label.setText(f"{artist['name']}")
        
        if "images" in artist and artist["images"]:
            image_url = artist["images"][0]["url"]
            image_data = get(image_url).content
            image = Image.open(BytesIO(image_data))
            image = image.resize((120, 120))
            image = QPixmap()
            image.loadFromData(image_data)
            self.image_label.setPixmap(image)
        
        artist_id = artist["id"]
        details = get_artist_details(token, artist_id)
        if details:
            self.artist_details.clear()
            self.artist_details.addItem(f"Followers: {details['followers']['total']}")
            self.artist_details.addItem(f"Genres: {', '.join(details['genres'])}")
            self.artist_details.addItem(f"Popularity: {details['popularity']}")
            self.spotify_link.setText(f"<a href='{details['external_urls']['spotify']}'>Open in Spotify</a>")
        
        self.song_list.clear()
        for song in get_songs_by_artist(token, artist_id):
            self.song_list.addItem(song["name"])
        
        self.album_list.clear()
        for album in get_albums_by_artist(token, artist_id):
            self.album_list.addItem(album["name"])

if __name__ == "__main__":
    app = QApplication([])
    window = SpotifyApp()
    window.show()
    app.exec()





















