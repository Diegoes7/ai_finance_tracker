1. Stop and remove all containers and volumes, if have and want to start fresh:

      docker compose down --volumes --remove-orphans

2. Build images:

      docker compose build

3. Start containers and trigger seed.sql: from the root directory of the project

      docker compose up -d
4. Need to pull in the container specific model:
   
      docker-compose exec ollama ollama pull llama3    
