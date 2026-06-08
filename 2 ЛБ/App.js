
import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [tracks, setTracks] = useState([]);
  const [genres, setGenres] = useState([]);
  const [selectedGenre, setSelectedGenre] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentTrack, setCurrentTrack] = useState(null);

  const API_URL = 'http://localhost:3001/api';

  useEffect(() => {
    fetchTracks();
    fetchGenres();
  }, []);

  const fetchTracks = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/tracks`);
      const data = await response.json();
      setTracks(data);
      setError(null);
    } catch (err) {
      setError('Помилка завантаження треків');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchGenres = async () => {
    try {
      const response = await fetch(`${API_URL}/genres`);
      const data = await response.json();
      setGenres(data);
    } catch (err) {
      console.error('Помилка завантаження жанрів:', err);
    }
  };

  const handleSearch = async (e) => {
    const query = e.target.value;
    setSearchQuery(query);

    if (!query) {
      fetchTracks();
      return;
    }

    try {
      const response = await fetch(`${API_URL}/search?q=${encodeURIComponent(query)}`);
      const data = await response.json();
      setTracks(data);
    } catch (err) {
      console.error('Помилка пошуку:', err);
    }
  };

  const handleGenreFilter = async (genre) => {
    setSelectedGenre(genre);

    if (genre === 'all') {
      fetchTracks();
      return;
    }

    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/genres/${genre}`);
      const data = await response.json();
      setTracks(data);
    } catch (err) {
      setError('Помилка фільтрування');
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  const handlePlayTrack = (track) => {
    setCurrentTrack(track);
    console.log('Відтворення:', track.title);
  };

  return (
    <div className="App">
      {}
      <header className="header">
        <h1>Музичний стрімінг</h1>
        <p>Слухайте улюблену музику безпосередньо тут</p>
      </header>

      {}
      <div className="search-section">
        <input
          type="text"
          placeholder="Пошук за назвою, виконавцем..."
          value={searchQuery}
          onChange={handleSearch}
          className="search-input"
        />
      </div>

      {}
      <div className="filter-section">
        <h3>Жанри:</h3>
        <div className="genre-buttons">
          <button
            className={`genre-btn ${selectedGenre === 'all' ? 'active' : ''}`}
            onClick={() => handleGenreFilter('all')}
          >
            Всі
          </button>
          {genres.map((genre) => (
            <button
              key={genre}
              className={`genre-btn ${selectedGenre === genre ? 'active' : ''}`}
              onClick={() => handleGenreFilter(genre)}
            >
              {genre}
            </button>
          ))}
        </div>
      </div>

      {}
      {currentTrack && (
        <div className="player">
          <div className="player-info">
            <h3>Зараз відтворюється</h3>
            <p className="track-title">{currentTrack.title}</p>
            <p className="track-artist">Виконавець: {currentTrack.artist}</p>
            <p className="track-genre">Жанр: {currentTrack.genre}</p>
            <p className="track-duration">{formatDuration(currentTrack.duration)}</p>
          </div>
        </div>
      )}

      {}
      <div className="tracks-section">
        <h2>Список треків</h2>

        {error && <div className="error-message">{error}</div>}

        {loading ? (
          <div className="loading">Завантаження...</div>
        ) : tracks.length === 0 ? (
          <div className="no-tracks">Треків не знайдено</div>
        ) : (
          <div className="tracks-list">
            {tracks.map((track) => (
              <div key={track.id} className="track-item">
                <div className="track-content">
                  <h4>{track.title}</h4>
                  <p className="track-meta">
                    <span>{track.artist}</span>
                    <span> • </span>
                    <span>{track.genre}</span>
                    <span> • </span>
                    <span>{formatDuration(track.duration)}</span>
                  </p>
                </div>
                <button
                  className="play-btn"
                  onClick={() => handlePlayTrack(track)}
                  title="Відтворити трек"
                >
                  Грати
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {}
      <footer className="footer">
        <p>{tracks.length} треків доступно</p>
      </footer>
    </div>
  );
}

export default App;
