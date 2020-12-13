init:
	python -m venv env
	source env/bin/activate
	pip install -r requirements.txt

lint:
	pycodestyle

tests:
	python -m unittest

protoc:
	python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/src/server/*.proto
