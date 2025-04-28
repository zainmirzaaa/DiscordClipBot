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
