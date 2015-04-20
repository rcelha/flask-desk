image_name=rcelha/flask_desk_application
container_name=rcelha_flask_desk_application_run
prev := $(shell docker images -q ${image_name})

main:
		@echo "Options are build_image|build"

build:
		@echo Build;

run: build_image
		@echo Run flask app
		docker-compose -f docker-compose.prod.yml up

build_image:
		@echo Build docker image;
		docker-compose -f docker-compose.prod.yml stop
		docker-compose -f docker-compose.prod.yml rm --force app
		docker build -t ${image_name} .
		docker rmi ${prev}
