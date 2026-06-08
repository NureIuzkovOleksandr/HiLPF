package com.example.musicsearchapp.ui

import androidx.lifecycle.ViewModel
import com.example.musicsearchapp.data.MusicData
import com.example.musicsearchapp.data.Track
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class MusicViewModel : ViewModel() {
    private val _searchQuery = MutableStateFlow("")
    val searchQuery: StateFlow<String> = _searchQuery.asStateFlow()

    private val _listenLater = MutableStateFlow<Set<String>>(emptySet())
    val listenLater: StateFlow<Set<String>> = _listenLater.asStateFlow()

    private val _downloadedTracks = MutableStateFlow<Set<String>>(emptySet())
    val downloadedTracks: StateFlow<Set<String>> = _downloadedTracks.asStateFlow()

    private val _currentTrack = MutableStateFlow<Track?>(null)
    val currentTrack: StateFlow<Track?> = _currentTrack.asStateFlow()

    private val _playlists = MutableStateFlow<List<com.example.musicsearchapp.data.Playlist>>(emptyList())
    val playlists: StateFlow<List<com.example.musicsearchapp.data.Playlist>> = _playlists.asStateFlow()

    val filteredTracks = MutableStateFlow(MusicData.allTracks)

    fun createPlaylist(name: String) {
        val newPlaylist = com.example.musicsearchapp.data.Playlist(
            id = java.util.UUID.randomUUID().toString(),
            name = name
        )
        _playlists.value = _playlists.value + newPlaylist
    }

    fun addTrackToPlaylist(playlistId: String, track: Track) {
        _playlists.value = _playlists.value.map {
            if (it.id == playlistId) {
                it.copy(tracks = it.tracks + track)
            } else it
        }
    }

    fun onSearchQueryChange(query: String) {
        _searchQuery.value = query
        filteredTracks.value = if (query.isEmpty()) {
            MusicData.allTracks
        } else {
            MusicData.allTracks.filter {
                it.title.contains(query, ignoreCase = true) ||
                        it.artist.contains(query, ignoreCase = true) ||
                        it.album.contains(query, ignoreCase = true) ||
                        it.genre.contains(query, ignoreCase = true)
            }
        }
    }

    fun toggleListenLater(trackId: String) {
        val current = _listenLater.value.toMutableSet()
        if (current.contains(trackId)) {
            current.remove(trackId)
        } else {
            current.add(trackId)
        }
        _listenLater.value = current
    }

    fun downloadTrack(trackId: String) {
        val current = _downloadedTracks.value.toMutableSet()
        current.add(trackId)
        _downloadedTracks.value = current
    }

    fun playTrack(track: Track) {
        _currentTrack.value = track
    }
}
