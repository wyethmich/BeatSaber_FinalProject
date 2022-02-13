docker-all: docker-build docker-run docker-start
	@echo "docker-all done"

docker-build:
	@echo "setting up network"
	-docker network create bs-predictor-network
	@echo "network setup done"
	@echo "building the image from docker file..."
	docker build --pull -t bs-predictor .
	@echo "image built"

docker-net:
	docker network create bs-predictor-network
	@echo "network created"

docker-run:
	@echo "starting the service in container..."
	-docker run -d -p 27017-27019:27017-27019 --net-alias mongodb --name bs-mongodb -itd --network=bs-predictor-network mongo	
	docker run -v /home/:/home/ -p 8080:8080 --name bs-predic-server -itd --network=bs-predictor-network bs-predictor

service:
	@echo "creating the service..."
	pip install --upgrade pip
	pip install -r requirements.txt

start:
	@echo "starting the service"
	python server.py

docker-stop:
	@echo "stopping the service"
	docker container stop bs-predic-server
	docker stop bs-mongodb
	@echo "service stopped"

docker-start:
	@echo "starting the service"
	docker start bs-mongodb
	docker container start bs-predic-server
	@echo "service started"

docker-remove:
	@echo "removing files"
	-docker network disconnect bs-predictor-network bs-predic-server
	-docker network disconnect bs-predictor-network bs-mongodb
	docker rm -f bs-predic-server
	docker rmi -f bs-predictor
	docker rm -f bs-mongodb
	docker network rm bs-predictor-network
	@echo "image removed"

docker-reset-run:
	docker rm -f bs-predic-server
	docker rm -f bs-mongodb
	@echo "containers removed"

docker-clean: docker-stop docker-remove
	@echo "docker service stopped and image removed"
