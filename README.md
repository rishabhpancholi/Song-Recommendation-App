# 🎵 ListenIt! - Song Recommendation App

🚀 **Song Recommendation Engine** is a web application that helps users discover songs tailored to their taste. The model combines **content-based filtering** and **clustering** techniques to offer personalized music recommendations based on genres, mood, and audio features.

🔗 **Live Demo:** [Song Recommendation Engine](https://listenit.onrender.com/recommendation)

---

## 🌟 Features

- 🎧 **Top 50 Popular Songs**  
  Browse the most popular tracks across genres. Easily **filter by genre**

- 🔍 **Song-Based Recommendations**  
  Select a song to view the **top 10 similar songs** using content-based filtering.  
  Bonus: The song list is **filterable by genre** for precise discovery.

- 🎵 **Mood-Based Recommendations**  
  Choose a **mood** (Happy, Chill, Energetic, etc.) to get songs from that emotional cluster, powered by **clustering on audio features** like tempo, energy, valence, and more.

- 🌐 **Deployed with Flask & Render** for global accessibility.

- ⚡ **Fast & Interactive UI** for seamless user experience.

---

## 🛠️ Tech Stack

- **Backend:** Flask, Python  
- **Frontend:** HTML, CSS, Bootstrap  
- **DL and ML Models:**  
  - Content-Based Filtering using song metadata & lyrics using Word2Vec Embeddings.
  - Clustering using audio features (e.g., KMeans)  
- **Data Source:** Songs dataset with Spotify audio features  
- **Deployment:** Render

---

## 🚀 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/rishabhpancholi/Song-Recommendation-App.git
cd Song-Recommendation-App

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

The application will be live at `http://127.0.0.1:5000/`


## 📷 Screenshots
![image](Song-1.png) 
![image](Song-2.png)
![image](Song-3.png)

## 🤝 Contributing
Feel free to open issues or contribute by submitting pull requests!

---
🌟 _If you like this project, don't forget to star the repository!_ ⭐
