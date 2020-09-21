export GOPATH=$(shell go env GOPATH):$(shell pwd)


send_tcp:
	go run sendr.go

start_server:
	python3 server.py

db:
	python3 build_database.py
