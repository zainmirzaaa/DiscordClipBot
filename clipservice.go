package main

import (
	"encoding/json"
	"log"
	"net/http"
)

type Clip struct {
	ID   string `json:"id"`
	Link string `json:"link"`
}

func clipsHandler(w http.ResponseWriter, r *http.Request) {
	// TODO: fetch from Azure Blob, mocked for now
	results := []Clip{
		{ID: "1", Link: "https://azure.blob/clip1.mp4"},
		{ID: "2", Link: "https://azure.blob/clip2.mp4"},
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(results)
}

func main() {
	http.HandleFunc("/clips", clipsHandler)
	log.Println("clip service running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}


type ClipMeta struct {
	ID       string `json:"id"`
	Link     string `json:"link"`
	Uploaded string `json:"uploaded"`
}

func enrichClips(clips []string) []ClipMeta {
	res := []ClipMeta{}
	for i, c := range clips {
		res = append(res, ClipMeta{
			ID: fmt.Sprintf("%d", i+1),
			Link: c,
			Uploaded: "2025-08-27",
		})
	}
	return res
}


var mongoClient *mongo.Client

func init() {
	mongoClient = connectMongo("mongodb://localhost:27017")
}

func saveClip(id, link string) {
	coll := mongoClient.Database("discord_ai").Collection("clips")
	_, err := coll.InsertOne(context.TODO(), Clip{ID: id, Link: link})
	if err != nil {
		log.Println("save error:", err)
	}
}


func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"ok": true}`))
}

func main() {
	http.HandleFunc("/clips", clipsHandler)
	http.HandleFunc("/health", healthHandler)
	log.Println("clip service running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}


func insertClip(id, link string) {
	coll := mongoClient.Database("discord_ai").Collection("clips")
	_, err := coll.InsertOne(context.TODO(), Clip{ID: id, Link: link})
	if err != nil {
		log.Println("insert error:", err)
	}
}

func addClipHandler(w http.ResponseWriter, r *http.Request) {
	var c Clip
	if err := json.NewDecoder(r.Body).Decode(&c); err != nil {
		http.Error(w, "bad request", 400); return
	}
	insertClip(c.ID, c.Link)
	w.Write([]byte(`{"ok": true}`))
}


func main() {
	http.HandleFunc("/clips", clipsHandler)
	http.HandleFunc("/clip", addClipHandler) // new route
	http.HandleFunc("/health", healthHandler)
	log.Println("clip service running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}


func countHandler(w http.ResponseWriter, r *http.Request) {
	coll := mongoClient.Database("discord_ai").Collection("clips")
	n, err := coll.CountDocuments(context.TODO(), bson.D{})
	if err != nil {
		http.Error(w, "db error", 500); return
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]int64{"count": n})
}

