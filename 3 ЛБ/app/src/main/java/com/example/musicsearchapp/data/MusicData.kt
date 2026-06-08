package com.example.musicsearchapp.data

object MusicData {
    val allTracks = listOf(
        Track(
            "1", "Blinding Lights", "The Weeknd", "After Hours", "Pop", "3:20",
            "https://upload.wikimedia.org/wikipedia/en/e/e6/The_Weeknd_-_Blinding_Lights.png",
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
        ),
        Track(
            "2", "Bohemian Rhapsody", "Queen", "A Night at the Opera", "Rock", "5:55",
            "https://upload.wikimedia.org/wikipedia/en/9/9f/Bohemian_Rhapsody.png",
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"
        ),
        Track(
            "3", "Shape of You", "Ed Sheeran", "÷", "Pop", "3:53",
            "https://upload.wikimedia.org/wikipedia/en/4/45/Divide_cover.png",
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"
        ),
        Track(
            "4", "Smells Like Teen Spirit", "Nirvana", "Nevermind", "Grunge", "5:01",
            "https://upload.wikimedia.org/wikipedia/en/b/b7/NirvanaNevermindalbumcover.jpg",
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
        ),
        Track(
            "5", "Levitating", "Dua Lipa", "Future Nostalgia", "Pop", "3:23",
            "https://upload.wikimedia.org/wikipedia/en/f/f5/Dua_Lipa_-_Future_Nostalgia_%28Official_Album_Cover%29.png",
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"
        )
    )

    val genres = allTracks.map { it.genre }.distinct()
}
