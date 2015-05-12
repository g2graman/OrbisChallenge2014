.PHONY: all run start install

all: install start run

install:
	@scripts/install | :

start:
	@scripts/start_server | :

run:
	@scripts/run | :
