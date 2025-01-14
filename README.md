# Spotify Artist Search

A **desktop application** built using **PyQt6** that allows users to search for an artist on **Spotify** and view their **top songs, recent albums, and profile details**.

## Features
- **Search for any artist** using Spotify API
- **Displays artist information** (followers, genres, popularity)
- **Shows the artist's top 10 songs**
- **Lists the artist's recent albums**
- **Displays artist images**
- **Provides a clickable link to the artist's Spotify profile**
- **Responsive and visually appealing UI**

## Installation
### 1. Clone the repository
```bash
git clone https://github.com/GauthamSathishD/spotify-artist-search.git
cd spotify-artist-search
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Setup
### 1. Get Spotify API Credentials
- Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
- Create a new application
- Copy your **Client ID** and **Client Secret**

### 2. Create a `.env` file in the project root and add:
```
CLIENT_ID=your_spotify_client_id
CLIENT_SECRET=your_spotify_client_secret
```

## Running the Application
```bash
python spotify_ui.py
```

## Technologies Used
- **Python 3**
- **PyQt6** (GUI framework)
- **Spotify API** (Data source)
- **Requests** (API handling)
- **Pillow** (Image processing)
- **dotenv** (Environment variable management)

## Screenshots
<img width="1509" alt="Screenshot 2025-01-14 at 2 30 11 AM" src="https://github.com/user-attachments/assets/50a50ea8-01b7-4dad-bc8e-e2727aff0c40" />


## Author
Developed by **Gautham Sathish** 



