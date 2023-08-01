.PHONY:

# build-dev: # Build the development environment (bad implementation)
#     docker run --name spacex_tor_db_dev -e POSTGRES_USER=tor_api_admin -e POSTGRES_PASSWORD='!$Azr2986HZa_tgz!&' -e POSTGRES_DB=tor_api -p 5432:5432 -d postgres
# 	docker build src/. --tag flask_app_dev
#
# run-dev: # Run the development environment (bad implementation)
#     docker run --name spacex_tor_api_dev flask_app_dev -p 8000:8000
# 	docker exec spacex_tor_api_dev flask run --port 8000
#
# down-dev: # turn down the development environment (bad implementation)
#     docker stop spacex_tor_db_dev
#     docker stop spacex_tor_api_dev
# 	docker rm spacex_tor_db_dev
# 	docker rm spacex_tor_api_dev

build-prod: # Build the production environment
	docker-compose build --no-cache

run-prod: ## Run the production environment
	docker-compose down && docker-compose up -d

down-prod: ## Run the production environment
	docker-compose down


