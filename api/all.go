package handler

import (
	"context"
	"encoding/json"
	"net/http"
	"net/url"
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
	ctx := r.Context()

	offset, err := getOffset(r.URL.Query())
	if err != nil {
		sendBadRequestResp(w, "Invalid page number")
		return
	}

	news, err := getNews(ctx, offset)
	if err != nil {
		sendServerErrorResp(w, err)
		return
	}

	sendResp(w, news)
}

func getOffset(query url.Values) (int, error) {
	page := query.Get("page")
	if page == "" {
		page = "1"
	}

	pageInt, err := strconv.Atoi(page)
	if err != nil {
		return 0, err
	}

	offset := (pageInt - 1) * PAGE_SIZE
	return offset, nil
}

func getNews(ctx context.Context, offset int) ([]bson.M, error) {
	client, err := getMongoClient()
	if err != nil {
		return nil, err
	}
	collection := client.Database("news").Collection("prothomalo")

	pipeline := []bson.M{
		{"$sort": bson.M{"published_time": -1}},
		{"$skip": offset},
		{"$limit": PAGE_SIZE},
	}

	cursor, err := collection.Aggregate(ctx, pipeline)
	if err != nil {
		return nil, err
	}

	var results []bson.M
	err = cursor.All(ctx, &results)
	if err != nil {
		return nil, err
	}

	return results, nil
}

func getMongoClient() (*mongo.Client, error) {
	if mongoClient != nil {
		return mongoClient, nil
	}

	client, err := mongo.NewClient(options.Client().ApplyURI(os.Getenv("MONGO_URI")))
	if err != nil {
		return nil, err
	}

	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	err = client.Connect(ctx)
	if err != nil {
		return nil, err
	}

	mongoClient = client
	return mongoClient, nil
}

func sendResp(w http.ResponseWriter, r interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(r)
}

func sendBadRequestResp(w http.ResponseWriter, reason string) {
	w.WriteHeader(http.StatusBadRequest)
	w.Write([]byte(reason))
}

func sendServerErrorResp(w http.ResponseWriter, err error) {
	w.WriteHeader(http.StatusInternalServerError)
	w.Write([]byte(err.Error()))
}
