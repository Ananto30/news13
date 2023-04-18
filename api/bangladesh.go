package handler

import (
	"context"
	"net/http"

	"go.mongodb.org/mongo-driver/bson"
)

var BANGLADESH_NEWS_CATEGORIES = []string{
	"রাজধানী",
	"জেলা",
	"করোনাভাইরাস",
	"অপরাধ",
	"পরিবেশ",
	"bangladesh",
}

func GetBangladeshNews(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	offset, err := getOffset(r.URL.Query())
	if err != nil {
		sendBadRequestResp(w, "Invalid page number")
		return
	}

	news, err := getBangladeshNews(ctx, offset)
	if err != nil {
		sendServerErrorResp(w, err)
		return
	}

	sendResp(w, news)
}

func getBangladeshNews(ctx context.Context, offset int) ([]bson.M, error) {
	client, err := getMongoClient()
	if err != nil {
		return nil, err
	}
	collection := client.Database("news").Collection("prothomalo")

	pipeline := []bson.M{
		{"$match": bson.M{"category": bson.M{"$in": BANGLADESH_NEWS_CATEGORIES}}},
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
