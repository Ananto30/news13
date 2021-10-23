package handler

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

const PAGE_SIZE = 20

var mongoClient *mongo.Client

func GetAllNews(w http.ResponseWriter, r *http.Request) {
	page := r.URL.Query().Get("page")
	if page == "" {
		page = "1"
	}

	pageInt, err := strconv.Atoi(page)
	if err != nil {
		log.Fatal(err)
	}

	offset := (pageInt - 1) * PAGE_SIZE

	news, err := getNews(offset)
	if err != nil {
		log.Fatal(err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(news)
}

func getNews(offset int) (*[]bson.M, error) {

	client := getMongoClient()
	collection := client.Database("news").Collection("prothomalo")

	pipeline := []bson.M{
		{"$sort": bson.M{"published_time": -1}},
		{"$skip": offset},
		{"$limit": PAGE_SIZE},
	}

	cursor, err := collection.Aggregate(context.TODO(), pipeline)
	if err != nil {
		return nil, err
	}

	var results []bson.M
	err = cursor.All(context.TODO(), &results)
	if err != nil {
		return nil, err
	}

	return &results, nil
}

func getMongoClient() *mongo.Client {
	if mongoClient != nil {
		return mongoClient
	}
	client, err := mongo.NewClient(options.Client().ApplyURI(os.Getenv("MONGO_URI")))
	if err != nil {
		log.Fatal(err)
	}
	ctx, _ := context.WithTimeout(context.Background(), 10*time.Second)
	err = client.Connect(ctx)
	if err != nil {
		log.Fatal(err)
	}
	mongoClient = client
	return mongoClient
}
