# Detect Docker Compose command (docker-compose or docker compose)
ifeq ($(shell command -v docker-compose),)
	COMPOSE_CMD := docker compose
else
	COMPOSE_CMD := docker-compose
endif

DATA_PATH := /home/$(USER)/data/

ENV_PATH = ./srcs/.env
COMPOSE_FILE := ./srcs/docker-compose.yml
DEV_COMPOSE_FILE := ./srcs/docker-compose.dev.yml

all: run

setup:
	@echo "Setting up the environment for ft_transcendence..."
	@mkdir -p ./secrets
	@chmod 777 ./secrets
	@docker volume rm srcs_frontend_build 2>/dev/null || true

stop:
	@echo "Stopping the services for ft_transcendence..."
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) down

run: stop setup
	@echo "Running the services for ft_transcendence..."
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) up --build -d && \
	echo "Services are up and running.\n\nThe app is accessible in a browser at https://localhost:8443\n\n" || echo "Error: Unable to run the services."

dev: stop setup
	@echo "Running development mode..."
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) -f $(DEV_COMPOSE_FILE) up --build backend postgres || true

restart: stop run

list:
	@echo "List of services running for ft_transcendence..."
	@docker ps -a

exec:
	@docker exec -it $(word 2, $(MAKECMDGOALS)) bash

volume:
	@echo "List of volumes for ft_transcendence..."
	@docker volume ls

clean-build:
	@echo "Removing exited containers..."
	@docker ps -aq --filter "status=exited" | xargs -r docker rm -v

clean:
	@echo "Cleaning up the environment for ft_transcendence..."
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) down
	@docker container prune -f
	@docker image prune -a -f
	@docker volume prune -f
	@docker network prune -f
	@rm -rf ./secrets
	@rm -rf ./srcs/requirements/frontend/build
	@rm -f ./srcs/requirements/frontend/package-lock.json

prune:
	@echo "Pruning the entire system..."
	@docker system prune -a -f
	@docker volume prune -a

.PHONY: setup run restart list volume clean
