all:
	python -m Pyro5.nameserver

run_server:
	python server/main.py

run_client:
	python client/main.py
