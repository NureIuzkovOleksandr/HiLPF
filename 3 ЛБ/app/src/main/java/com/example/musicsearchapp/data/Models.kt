package com.example.musicsearchapp.data

data class Track(
    val id: String,
    val title: String,
    val artist: String,
    val album: String,
    val genre: String,
    val duration: String,
    val coverUrl: String,
    val audioUrl: String,
    var isDownloaded: Boolean = false
)

data class Playlist(
    val id: String,
    val name: String,
    val tracks: List<Track> = emptyList()
)
