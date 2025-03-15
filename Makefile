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

all: setup run

setup:
	@echo "Setting up the environment for ft_transcendence..."
	@mkdir -p ./secrets
	@chmod 777 ./secrets
	@chmod +x ./srcs/requirements/backend/tools/entrypoint.sh
	@docker volume rm srcs_frontend_build 2>/dev/null || true
	@docker build -t backend_setup --build-arg LOCK_ONLY=true -f srcs/requirements/backend/Dockerfile srcs/requirements/backend


run: setup
	@echo "Running the services for ft_transcendence..."
	@bash ./srcs/requirements/tools/create_ssl_cert.sh
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) up --build -d && \
	echo "Services are up and running.\n\nThe app is accessible in a browser at https://localhost\n\n" || echo "Error: Unable to run the services."

dev: setup
	@echo "Running development mode..."
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) -f $(DEV_COMPOSE_FILE) up --build -d backend postgres
	@echo "\n\nThe app is accessible in a browser at http://localhost:5173\n\n"
	@docker logs backend -f


stop:
	@echo "Stopping the services for ft_transcendence..."
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) down

restart: stop run

list:
	@echo "List of services running for ft_transcendence..."
	@docker ps -a

volume:
	@echo "List of volumes for ft_transcendence..."
	@docker volume ls

clean:
	@echo "Cleaning up the environment for ft_transcendence..."
	@$(COMPOSE_CMD) -f $(COMPOSE_FILE) down
	@docker stop $(docker ps -qa) 2>/dev/null || true
	@docker rm $(docker ps -qa) 2>/dev/null || true
	@docker rmi -f $(docker images -qa) 2>/dev/null || true
	@docker volume rm $(docker volume ls -q) 2>/dev/null || true
	@docker network rm $(docker network ls -q) 2>/dev/null || true
	@rm -rf ./secrets
	@rm -rf ./srcs/requirements/frontend/build
	@rm -rf ./srcs/requirements/frontend/package-lock.json

prune: clean
	@echo "Pruning the environment for ft_transcendence..."
	@docker system prune -a

.PHONY: setup run restart list volume clean
