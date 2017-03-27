.PHONY: client server build

server:
	python server.py

client:
	python client.py

build:
	pip install -r requirements.txt
