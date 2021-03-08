var chiLambda *chiadapter.ChiLambda

// handler is the function called by the lambda.
func handler(ctx context.Context, req events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	return chiLambda.ProxyWithContext(ctx, req)
}

// main is called when a new lambda starts, so don't
// expect to have something done for every query here.
func main() {
	// init go-chi router
	r := chi.NewRouter()
	r.HandleFunc("/*", func(w http.ResponseWriter, r *http.Request) {
		body, _ := ioutil.ReadAll(r.Body)
		_ = render.Render(w, r, &apiResponse{
			Status: http.StatusOK,
			URL: r.URL.String(),
			RequestBody: string(body),
		})
	})
	
	chiLambda = chiadapter.New(r)
	// start the lambda with a context
	lambda.StartWithContext(context.Background(), hndler)
}a
