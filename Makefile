export GOPATH=$(shell go env GOPATH):$(shell pwd)


send_tcp:
	clear;go run sendr.go

start_server:
	clear;python3 server.py

db:
	clear;python3 build_database.py

test:
	clear;python3 test.py