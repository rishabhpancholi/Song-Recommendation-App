document.addEventListener("DOMContentLoaded",function(){
    let links = document.querySelectorAll(".custom-nav-link");
    links.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add("active");
        }
    });

    const moodFilter = document.getElementById("moodFilter");
    const songsContainer = document.querySelector(".row");

    function updateSongs(songs) {
        songsContainer.innerHTML = ""; 
        
        songs.forEach(song => {
            let songHTML = 
                `<div class="col-md-4 mb-4">
                    <div class="card song-card">
                         <img src="${ song.image_url ? song.image_url : 'static/default.png' }" alt="Album Image"></img>
                        <div class="card-body">
                            <h5 class="card-title">${ song.track_name.toUpperCase() }</h5>
                            <p class="card-text"><strong>Artist: ${ song.artist_name.toUpperCase() }</strong> </p>
                            <p class="card-text"><strong>Genre: ${ song.playlist_genre.toUpperCase() }</strong></p>
                             <a href="${ song.spotify_url }" class="btn btn-primary" target="_blank">Listen on Spotify</a>
                        </div>
                    </div>
                </div>`;
            songsContainer.innerHTML += songHTML;
        });
    }

    moodFilter.addEventListener("change", function () {
        let selectedMood = moodFilter.value;
        
        fetch("/filter_songs_mood", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mood: selectedMood })
        })
        .then(response => response.json())
        .then(data => updateSongs(data))
        .catch(error => console.error("Error fetching songs:", error));
    });
});