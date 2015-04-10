image_name=rcelha/flask_desk_application
container_name=rcelha_flask_desk_application_run
prev := $(shell docker images -q ${image_name})

main:
		@echo "Options are build_image|build"

build:
		@echo Build;

run: build_image
		@echo Run flask app
		docker run -it --rm --name="${container_name}" -p 5000:5000 ${image_name} 

build_image:
		@echo Build docker image;
		docker build -t ${image_name} .
		docker rmi ${prev}
