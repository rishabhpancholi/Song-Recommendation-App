document.addEventListener("DOMContentLoaded", function () {

    let links = document.querySelectorAll(".custom-nav-link");
    links.forEach(link => {
        if (link.href === window.location.href) {
            link.classList.add("active");
        }
    });

    const genreFilter = document.getElementById("genreFilter");
    const songsList = document.getElementById("songsList");
    const recommendButton = document.getElementById("recommendButton");
    const recommendationsContainer = document.querySelector(".recommendations");

    let selectedSong = "";

    function attachSongClickListeners() {
        document.querySelectorAll(".song-item").forEach(item => {
            item.addEventListener("click", function () {
                selectedSong = this.getAttribute("data-song"); 
    
                document.querySelectorAll(".song-item").forEach(el => el.classList.remove("active"));
                this.classList.add("active");
    
                recommendButton.disabled = false;
            });
        });
     }

    function updateSongsList(songs) {
        songsList.innerHTML = ""; 
    
        songs.forEach(song => {
            let songHTML = `<li class="list-group-item song-item" data-song="${song.track_name}">
                <strong>${song.track_name.toUpperCase()}</strong> - ${song.artist_name.toUpperCase()}
            </li>`;
            songsList.innerHTML += songHTML;
        });
    
        attachSongClickListeners();
    }

     genreFilter.addEventListener("change", function () {
        let selectedGenre = genreFilter.value;
        
        fetch("/filter_songs_recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ genre: selectedGenre })
        })
        .then(response => response.json())
        .then(data => updateSongsList(data))
        .catch(error => console.error("Error fetching songs:", error));
    });

    function recommendSongs(recommendations) {

        const rowDiv = document.createElement('div');
        rowDiv.classList.add('row');
        
        recommendations.forEach(recommendation => {
            let songHTML = 
                `<div class="col-md-4 mb-4">
                    <div class="card song-card">
                         <img src="${ recommendation.image_url ? recommendation.image_url : 'static/default.png' }" alt="Album Image"></img>
                        <div class="card-body">
                            <h5 class="card-title">${ recommendation.track_name.toUpperCase() }</h5>
                            <p class="card-text"><strong>Artist: ${ recommendation.artist_name.toUpperCase() }</strong> </p>
                            <p class="card-text"><strong>Genre: ${ recommendation.playlist_genre.toUpperCase() }</strong></p>
                             <a href="${ recommendation.spotify_url }" class="btn btn-primary" target="_blank">Listen on Spotify</a>
                        </div>
                    </div>
                </div>`;
            rowDiv.innerHTML += songHTML;
        });

        recommendationsContainer.appendChild(rowDiv);
    }

    recommendButton.addEventListener("click",function(){
        if (!selectedSong) return;

        recommendationsContainer.innerHTML = ""; 

         console.log("Selected Song for Recommendations:", selectedSong);

        fetch("/get_recommendations",{
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ song: selectedSong })
        })
        .then(response => response.json())
        .then(data => recommendSongs(data))
        .catch(error => console.error("Error fetching recommendations:", error));
    });

    attachSongClickListeners();
});