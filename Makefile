.PHONY: all run start install clean

all: install start run

clean:
	@scripts/clean | :

install:
	@scripts/install | :

start:
	@scripts/start_server | :

run:
	@scripts/run | :
