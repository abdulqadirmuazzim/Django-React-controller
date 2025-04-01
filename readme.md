# Django-React Music Playlist Controller

## Overview
The **Django-React Music Playlist Controller** is a full-stack web application that enables users to create, join, and manage virtual song rooms where they can collaboratively control music playback. This project integrates **Django (backend)** with **React (frontend)** and **Spotify API**, allowing users to control Spotify playback in real-time.

## Features
- **User Authentication & Authorization**: Secure login and authentication system.
- **Music Room Creation**: Users can create rooms where others can join and participate.
- **Spotify Integration**:
  - Play, pause, and control Spotify playback within the app.
  - Vote to skip tracks when in a room.
  - Authorization system using the Spotify API.
- **Real-time Updates**:
  - Uses Django Channels & WebSockets for real-time updates in rooms.
- **Interactive Frontend**:
  - Built using React.js with Material-UI components for an engaging user experience.
- **Secure Authentication**:
  - User authentication and authorization using Django’s built-in authentication system.
- **Integrated API Services**:
  - Seamless integration with the Spotify API for music streaming.

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Frontend**: React.js, Webpack, Babel, Material-UI
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **Other Dependencies**: Spotipy, Requests, Python-dotenv, Whitenoise

## Installation Guide
### Backend Setup
1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/django-react-music-controller.git
  
2. Install Python dependencies:
   ```sh
   pip install -r Pipfile
   ```  ```
3. Navigate to the backend directory:
   ```sh
   cd playlist
   ```
4. Apply database migrations:
   ```sh
   python manage.py migrate
   ```
5. Start the Django backend server:
   ```sh
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```sh
   cd playlist/frontend
   ```
2. Install frontend dependencies:
   ```sh
   npm install
   ```
3. Run frontend in development mode:
   ```sh
   npm start
   ```

## Usage
- **Music Player**: Users can **play, pause, and skip** songs in shared rooms.
- **Group Music Rooms**: Create, join, and interact with others in collaborative listening sessions.
- **Spotify Integration**: Users can authenticate via **Spotify** and sync their accounts for music control.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## License
This project is licensed under the MIT License.
