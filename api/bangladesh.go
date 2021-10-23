package handler

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"go.mongodb.org/mongo-driver/bson"
)

var BANGLADESH_NEWS_CATEGORIES = [...]string{
	"রাজধানী",
	"জেলা",
	"করোনাভাইরাস",
	"অপরাধ",
	"পরিবেশ",
	"bangladesh",
}

func GetBangladeshNews(w http.ResponseWriter, r *http.Request) {
	page := r.URL.Query().Get("page")
	if page == "" {
		page = "1"
	}

	pageInt, err := strconv.Atoi(page)
	if err != nil {
		log.Fatal(err)
	}

	offset := (pageInt - 1) * PAGE_SIZE

	news, err := getBangladeshNews(offset)
	if err != nil {
		log.Fatal(err)
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(news)
}

func getBangladeshNews(offset int) (*[]bson.M, error) {

	client := getMongoClient()
	collection := client.Database("news").Collection("prothomalo")

	pipeline := []bson.M{
		{"$match": bson.M{"category": bson.M{"$in": BANGLADESH_NEWS_CATEGORIES}}},
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
