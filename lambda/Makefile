.PHONY: pingme
pingme:
	go mod pingme

test:
	go test -race ./...

build:
	go build -mod=pingme .

lambda-build:
	GOOS=darwin go build -mod=pingme -o /asset-output/main
