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

	categories, err := collection.Distinct(ctx, "category", bson.M{})
	if err != nil {
		return nil, err
	}

	var result []string
	for _, category := range categories {
		if c, ok := category.(string); ok {
			result = append(result, c)
		}
	}

	return result, nil
}
