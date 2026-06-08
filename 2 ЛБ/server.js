const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
require('dotenv').config();

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname)));

app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

const tracks = [];
const playlists = [];
const users = [];

app.post('/api/auth/register', (req, res) => {
  const { username, email, password } = req.body;
  if (!username || !email || !password) {
    return res.status(400).json({ error: 'Всі поля обов\'язкові' });
  }
  if (users.some(u => u.username === username)) {
    return res.status(400).json({ error: 'Користувач вже існує' });
  }
  const user = {
    id: Date.now(),
    username,
    email,
    password
  };
  users.push(user);
  res.json({ message: 'Користувач успішно зареєстрований', user });
});

app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  const user = users.find(u => u.username === username && u.password === password);
  if (!user) {
    return res.status(401).json({ error: 'Невірне ім\'я користувача або пароль' });
  }
  res.json({
    message: 'Успішний вхід',
    user: { id: user.id, username: user.username, email: user.email }
  });
});

app.get('/api/tracks', (req, res) => {
  const { genre, search } = req.query;
  let result = tracks;
  if (genre) {
    result = result.filter(t => t.genre.toLowerCase() === genre.toLowerCase());
  }
  if (search) {
    result = result.filter(t =>
      t.title.toLowerCase().includes(search.toLowerCase()) ||
      t.artist.toLowerCase().includes(search.toLowerCase())
    );
  }
  res.json(result);
});

app.get('/api/tracks/:id', (req, res) => {
  const track = tracks.find(t => t.id == req.params.id);
  if (!track) {
    return res.status(404).json({ error: 'Трек не знайдено' });
  }
  res.json(track);
});

app.post('/api/tracks', (req, res) => {
  const { title, artist, genre, duration, fileName } = req.body;
  if (!title || !artist || !genre) {
    return res.status(400).json({ error: 'Всі поля обов\'язкові' });
  }
  const track = {
    id: Date.now(),
    title,
    artist,
    genre,
    duration: duration || 0,
    fileName: fileName || 'audio.mp3',
    url: `/uploads/music/${fileName}`,
    uploadedAt: new Date().toISOString()
  };
  tracks.push(track);
  res.json({ message: 'Трек успішно завантажено', track });
});

app.delete('/api/tracks/:id', (req, res) => {
  const index = tracks.findIndex(t => t.id == req.params.id);
  if (index === -1) {
    return res.status(404).json({ error: 'Трек не знайдено' });
  }
  const [deletedTrack] = tracks.splice(index, 1);
  res.json({ message: 'Трек видалено', track: deletedTrack });
});

app.get('/api/playlists', (req, res) => {
  res.json(playlists);
});

app.post('/api/playlists', (req, res) => {
  const { name, description, userId } = req.body;
  if (!name) {
    return res.status(400).json({ error: 'Назва плейлисту обов\'язкова' });
  }
  const playlist = {
    id: Date.now(),
    name,
    description: description || '',
    userId: userId || null,
    tracks: [],
    createdAt: new Date().toISOString()
  };
  playlists.push(playlist);
  res.json({ message: 'Плейлист створено', playlist });
});

app.get('/api/playlists/:id', (req, res) => {
  const playlist = playlists.find(p => p.id == req.params.id);
  if (!playlist) {
    return res.status(404).json({ error: 'Плейлист не знайдено' });
  }
  res.json(playlist);
});

app.post('/api/playlists/:id/tracks', (req, res) => {
  const { trackId } = req.body;
  const playlist = playlists.find(p => p.id == req.params.id);
  if (!playlist) {
    return res.status(404).json({ error: 'Плейлист не знайдено' });
  }
  const track = tracks.find(t => t.id == trackId);
  if (!track) {
    return res.status(404).json({ error: 'Трек не знайдено' });
  }
  if (!playlist.tracks.includes(trackId)) {
    playlist.tracks.push(trackId);
  }
  res.json({ message: 'Трек додано до плейлисту', playlist });
});

app.delete('/api/playlists/:id/tracks/:trackId', (req, res) => {
  const playlist = playlists.find(p => p.id == req.params.id);
  if (!playlist) {
    return res.status(404).json({ error: 'Плейлист не знайдено' });
  }
  playlist.tracks = playlist.tracks.filter(t => t != req.params.trackId);
  res.json({ message: 'Трек видалено з плейлисту', playlist });
});

app.get('/api/genres', (req, res) => {
  const genres = [...new Set(tracks.map(t => t.genre))];
  res.json(genres);
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'Сервер працює' });
});

app.get('/', (req, res) => {
  res.json({
    message: 'Music Streaming API Server',
    version: '1.0.0',
    endpoints: {
      auth: {
        register: 'POST /api/auth/register',
        login: 'POST /api/auth/login'
      },
      tracks: {
        getAll: 'GET /api/tracks',
        getOne: 'GET /api/tracks/:id',
        create: 'POST /api/tracks',
        delete: 'DELETE /api/tracks/:id'
      },
      playlists: {
        getAll: 'GET /api/playlists',
        create: 'POST /api/playlists',
        getOne: 'GET /api/playlists/:id',
        addTrack: 'POST /api/playlists/:id/tracks',
        removeTrack: 'DELETE /api/playlists/:id/tracks/:trackId'
      }
    }
  });
});

app.use((req, res) => {
  res.status(404).json({ error: 'Маршрут не знайдено' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Music Streaming Server запущено на http://localhost:${PORT}`);
});
