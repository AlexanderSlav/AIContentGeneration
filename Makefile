NAME=aicontentcreator

.PHONY: build
build:
	docker build -t $(NAME) .

.PHONY: run
run:
	docker run -it --rm --name=$(NAME) $(NAME) /bin/bash

.PHONY: stop
stop:
	docker stop $(NAME)
