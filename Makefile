HANDOUT=challenge.py Dockerfile Makefile
DOCKER_TAG=shuffle
PORT=1337

handout.tar.xz: $(HANDOUT)
	tar -cavf $@ $^

build: $(HANDOUT) flag.txt
	docker build --tag $(DOCKER_TAG) --build-arg PORT=$(PORT) .

start: build
	make stop || true
	docker run --rm --detach --publish $(PORT):$(PORT) $(DOCKER_TAG) > .dockerid
	@echo "$(DOCKER_TAG) is running on port $(PORT)"

stop: 
	test -e .dockerid && docker kill `cat .dockerid`
	rm -f .dockerid

logs:
	test -e .dockerid && docker logs --follow `cat .dockerid`
	
.PHONY: build start stop logs
	
