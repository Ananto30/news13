package handler

import (
	"context"
	"net/http"

	"go.mongodb.org/mongo-driver/bson"
)

func GetCategories(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()

	categories, err := getCategories(ctx)
	if err != nil {
		sendServerErrorResp(w, err)
		return
	}

	sendResp(w, categories)
}

func getCategories(ctx context.Context) ([]string, error) {
	client, err := getMongoClient()
	if err != nil {
		return nil, err
	}
	collection := client.Database("news").Collection("prothomalo")

	pipeline := []bson.M{
		{"$group": bson.M{"_id": "$category"}},
		{"$sort": bson.M{"_id": 1}},
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

	var categories []string
	for _, result := range results {
		categories = append(categories, result["_id"].(string))
	}

	return categories, nil
}
