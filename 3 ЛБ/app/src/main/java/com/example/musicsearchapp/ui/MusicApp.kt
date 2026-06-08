package com.example.musicsearchapp.ui

import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.PlaylistAdd
import androidx.compose.material.icons.automirrored.filled.PlaylistPlay
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import coil.compose.AsyncImage
import com.example.musicsearchapp.data.MusicData
import com.example.musicsearchapp.data.Track
import com.example.musicsearchapp.data.Playlist

sealed class Screen(val route: String, val icon: androidx.compose.ui.graphics.vector.ImageVector, val label: String) {
    object Search : Screen("search", Icons.Default.Search, "Search")
    object Library : Screen("library", Icons.Default.LibraryMusic, "Library")
}

@Composable
fun MusicApp() {
    val navController = rememberNavController()
    val viewModel: MusicViewModel = viewModel()
    val currentTrack by viewModel.currentTrack.collectAsState()

    Scaffold(
        bottomBar = {
            Column {
                currentTrack?.let { track ->
                    MiniPlayer(track = track)
                }
                BottomNavigationBar(navController)
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Screen.Search.route,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(Screen.Search.route) {
                SearchScreen(viewModel)
            }
            composable(Screen.Library.route) {
                LibraryScreen(viewModel)
            }
        }
    }
}

@Composable
fun BottomNavigationBar(navController: NavHostController) {
    val items = listOf(Screen.Search, Screen.Library)
    NavigationBar {
        val navBackStackEntry by navController.currentBackStackEntryAsState()
        val currentRoute = navBackStackEntry?.destination?.route
        items.forEach { screen ->
            NavigationBarItem(
                icon = { Icon(screen.icon, contentDescription = screen.label) },
                label = { Text(screen.label) },
                selected = currentRoute == screen.route,
                onClick = {
                    navController.navigate(screen.route) {
                        popUpTo(navController.graph.startDestinationId) { saveState = true }
                        launchSingleTop = true
                        restoreState = true
                    }
                }
            )
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SearchScreen(viewModel: MusicViewModel) {
    val query by viewModel.searchQuery.collectAsState()
    val tracks by viewModel.filteredTracks.collectAsState()
    val listenLater by viewModel.listenLater.collectAsState()
    val downloaded by viewModel.downloadedTracks.collectAsState()
    val playlists by viewModel.playlists.collectAsState()

    var showPlaylistDialog by remember { mutableStateOf<Track?>(null) }

    if (showPlaylistDialog != null) {
        AddToPlaylistDialog(
            playlists = playlists,
            onDismiss = { showPlaylistDialog = null },
            onPlaylistSelected = { playlistId ->
                viewModel.addTrackToPlaylist(playlistId, showPlaylistDialog!!)
                showPlaylistDialog = null
            },
            onCreatePlaylist = { name ->
                viewModel.createPlaylist(name)
            }
        )
    }

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        TextField(
            value = query,
            onValueChange = { viewModel.onSearchQueryChange(it) },
            modifier = Modifier.fillMaxWidth(),
            placeholder = { Text("Search by artist, album, genre...") },
            leadingIcon = { Icon(Icons.Default.Search, contentDescription = null) },
            trailingIcon = {
                if (query.isNotEmpty()) {
                    IconButton(onClick = { viewModel.onSearchQueryChange("") }) {
                        Icon(Icons.Default.Clear, contentDescription = "Clear")
                    }
                }
            }
        )
        Spacer(modifier = Modifier.height(8.dp))
        
        Row(
            modifier = Modifier.fillMaxWidth().horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            val genres = listOf("All") + MusicData.genres
            genres.forEach { genre ->
                FilterChip(
                    selected = if (genre == "All") query.isEmpty() else query.equals(genre, ignoreCase = true),
                    onClick = { viewModel.onSearchQueryChange(if (genre == "All") "" else genre) },
                    label = { Text(genre) }
                )
            }
        }
        
        Spacer(modifier = Modifier.height(8.dp))
        LazyColumn {
            items(tracks) { track ->
                TrackItem(
                    track = track,
                    isListenLater = listenLater.contains(track.id),
                    isDownloaded = downloaded.contains(track.id),
                    onPlay = { viewModel.playTrack(track) },
                    onListenLater = { viewModel.toggleListenLater(track.id) },
                    onDownload = { viewModel.downloadTrack(track.id) },
                    onAddToPlaylist = { showPlaylistDialog = track }
                )
            }
        }
    }
}

@Composable
fun LibraryScreen(viewModel: MusicViewModel) {
    val listenLaterIds by viewModel.listenLater.collectAsState()
    val downloadedIds by viewModel.downloadedTracks.collectAsState()
    val playlists by viewModel.playlists.collectAsState()
    
    var selectedTab by remember { mutableStateOf(0) }
    val tabs = listOf("Listen Later", "Downloaded", "Playlists")

    Column(modifier = Modifier.fillMaxSize().padding(16.dp)) {
        Text("Your Library", style = MaterialTheme.typography.headlineMedium)
        SecondaryScrollableTabRow(selectedTabIndex = selectedTab, edgePadding = 0.dp) {
            tabs.forEachIndexed { index, title ->
                Tab(selected = selectedTab == index, onClick = { selectedTab = index }, text = { Text(title) })
            }
        }
        Spacer(modifier = Modifier.height(16.dp))
        
        when(selectedTab) {
            0 -> TrackList(MusicData.allTracks.filter { listenLaterIds.contains(it.id) }, viewModel, listenLaterIds, downloadedIds)
            1 -> TrackList(MusicData.allTracks.filter { downloadedIds.contains(it.id) }, viewModel, listenLaterIds, downloadedIds)
            2 -> PlaylistList(playlists)
        }
    }
}

@Composable
fun TrackList(tracks: List<Track>, viewModel: MusicViewModel, listenLaterIds: Set<String>, downloadedIds: Set<String>) {
    if (tracks.isEmpty()) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("No tracks here.")
        }
    } else {
        LazyColumn {
            items(tracks) { track ->
                TrackItem(
                    track = track,
                    isListenLater = listenLaterIds.contains(track.id),
                    isDownloaded = downloadedIds.contains(track.id),
                    onPlay = { viewModel.playTrack(track) },
                    onListenLater = { viewModel.toggleListenLater(track.id) },
                    onDownload = { viewModel.downloadTrack(track.id) },
                    onAddToPlaylist = {} // Simplified
                )
            }
        }
    }
}

@Composable
fun PlaylistList(playlists: List<Playlist>) {
    if (playlists.isEmpty()) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text("No playlists created.")
        }
    } else {
        LazyColumn {
            items(playlists) { playlist ->
                ListItem(
                    headlineContent = { Text(playlist.name) },
                    supportingContent = { Text("${playlist.tracks.size} tracks") },
                    leadingContent = { Icon(Icons.AutoMirrored.Filled.PlaylistPlay, contentDescription = null) }
                )
            }
        }
    }
}

@Composable
fun TrackItem(
    track: Track,
    isListenLater: Boolean,
    isDownloaded: Boolean,
    onPlay: () -> Unit,
    onListenLater: () -> Unit,
    onDownload: () -> Unit,
    onAddToPlaylist: () -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).clickable { onPlay() },
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Row(
            modifier = Modifier.padding(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            AsyncImage(
                model = track.coverUrl,
                contentDescription = null,
                modifier = Modifier.size(64.dp),
                contentScale = ContentScale.Crop
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(track.title, style = MaterialTheme.typography.titleMedium)
                Text("${track.artist} • ${track.album}", style = MaterialTheme.typography.bodySmall)
                Text(track.genre, style = MaterialTheme.typography.labelSmall, color = Color.Gray)
            }
            IconButton(onClick = onListenLater) {
                Icon(
                    imageVector = if (isListenLater) Icons.Default.Favorite else Icons.Default.FavoriteBorder,
                    contentDescription = "Listen Later",
                    tint = if (isListenLater) Color.Red else Color.Gray
                )
            }
            IconButton(onClick = onAddToPlaylist) {
                Icon(Icons.AutoMirrored.Filled.PlaylistAdd, contentDescription = "Add to Playlist")
            }
            IconButton(onClick = onDownload) {
                Icon(
                    imageVector = if (isDownloaded) Icons.Default.DownloadDone else Icons.Default.Download,
                    contentDescription = "Download",
                    tint = if (isDownloaded) Color.Blue else Color.Gray
                )
            }
        }
    }
}

@Composable
fun AddToPlaylistDialog(
    playlists: List<Playlist>,
    onDismiss: () -> Unit,
    onPlaylistSelected: (String) -> Unit,
    onCreatePlaylist: (String) -> Unit
) {
    var newPlaylistName by remember { mutableStateOf("") }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add to Playlist") },
        text = {
            Column {
                if (playlists.isEmpty()) {
                    Text("No playlists yet.")
                } else {
                    playlists.forEach { playlist ->
                        TextButton(onClick = { onPlaylistSelected(playlist.id) }) {
                            Text(playlist.name)
                        }
                    }
                }
                HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
                TextField(
                    value = newPlaylistName,
                    onValueChange = { newPlaylistName = it },
                    placeholder = { Text("New Playlist Name") }
                )
                Button(onClick = { 
                    if (newPlaylistName.isNotBlank()) {
                        onCreatePlaylist(newPlaylistName)
                        newPlaylistName = ""
                    }
                }) {
                    Text("Create")
                }
            }
        },
        confirmButton = {
            TextButton(onClick = onDismiss) { Text("Close") }
        }
    )
}

@Composable
fun MiniPlayer(track: Track) {
    Surface(
        color = MaterialTheme.colorScheme.primaryContainer,
        modifier = Modifier.fillMaxWidth()
    ) {
        Row(
            modifier = Modifier.padding(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            AsyncImage(
                model = track.coverUrl,
                contentDescription = null,
                modifier = Modifier.size(48.dp),
                contentScale = ContentScale.Crop
            )
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(track.title, style = MaterialTheme.typography.titleSmall)
                Text(track.artist, style = MaterialTheme.typography.bodySmall)
            }
            IconButton(onClick = { /* Play/Pause logic */ }) {
                Icon(Icons.Default.PlayArrow, contentDescription = "Play")
            }
        }
    }
}
