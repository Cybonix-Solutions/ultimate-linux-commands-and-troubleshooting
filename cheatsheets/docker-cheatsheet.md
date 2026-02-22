# Docker Cheatsheet

Common Docker commands for container management and troubleshooting.

[⬅ Back to Main Index](README.md)

## Topic: Container Lifecycle

| Command | Description |
|---------|-------------|
| `docker run IMAGE` | Create and start container |
| `docker run -it IMAGE bash` | Interactive with terminal |
| `docker run -d IMAGE` | Run detached (background) |
| `docker run --rm IMAGE` | Remove container when stopped |
| `docker run --name myapp IMAGE` | Assign name |
| `docker run -p 8080:80 IMAGE` | Map port 8080→80 |
| `docker run -v /host:/container IMAGE` | Bind mount |
| `docker run -e VAR=value IMAGE` | Set environment variable |
| `docker start CONTAINER` | Start stopped container |
| `docker stop CONTAINER` | Graceful stop (SIGTERM) |
| `docker kill CONTAINER` | Force stop (SIGKILL) |
| `docker restart CONTAINER` | Stop then start |
| `docker rm CONTAINER` | Remove stopped container |
| `docker rm -f CONTAINER` | Force remove (even running) |

## Topic: Container Inspection

| Command | Description |
|---------|-------------|
| `docker ps` | Running containers |
| `docker ps -a` | All containers (including stopped) |
| `docker logs CONTAINER` | View logs |
| `docker logs -f CONTAINER` | Follow logs |
| `docker logs --tail 100 CONTAINER` | Last 100 lines |
| `docker inspect CONTAINER` | Full details (JSON) |
| `docker top CONTAINER` | Running processes |
| `docker stats` | Live resource usage |
| `docker port CONTAINER` | Port mappings |

## Topic: Executing in Containers

| Command | Description |
|---------|-------------|
| `docker exec -it CONTAINER bash` | Interactive shell |
| `docker exec CONTAINER command` | Run command |
| `docker exec -u root CONTAINER cmd` | Run as root |
| `docker cp file CONTAINER:/path` | Copy file into container |
| `docker cp CONTAINER:/path file` | Copy file from container |

## Topic: Images

| Command | Description |
|---------|-------------|
| `docker images` | List local images |
| `docker pull IMAGE:TAG` | Download image |
| `docker push IMAGE:TAG` | Push to registry |
| `docker build -t NAME:TAG .` | Build from Dockerfile |
| `docker tag IMAGE NEW:TAG` | Tag image |
| `docker rmi IMAGE` | Remove image |
| `docker image prune` | Remove unused images |
| `docker history IMAGE` | Show image layers |
| `docker save IMAGE > file.tar` | Export image |
| `docker load < file.tar` | Import image |

## Topic: Volumes

| Command | Description |
|---------|-------------|
| `docker volume ls` | List volumes |
| `docker volume create NAME` | Create volume |
| `docker volume rm NAME` | Remove volume |
| `docker volume inspect NAME` | Volume details |
| `docker volume prune` | Remove unused volumes |
| `-v NAME:/path` | Mount named volume |
| `-v /host:/container` | Bind mount |
| `-v /host:/container:ro` | Read-only mount |

## Topic: Networks

| Command | Description |
|---------|-------------|
| `docker network ls` | List networks |
| `docker network create NAME` | Create network |
| `docker network rm NAME` | Remove network |
| `docker network inspect NAME` | Network details |
| `docker network connect NET CONTAINER` | Connect container |
| `--network=NAME` | Use network when running |
| `--network=host` | Use host networking |

## Topic: Cleanup

| Command | Description |
|---------|-------------|
| `docker system df` | Disk usage |
| `docker system prune` | Remove unused data |
| `docker system prune -a` | Remove all unused (images too) |
| `docker container prune` | Remove stopped containers |
| `docker image prune -a` | Remove all unused images |

## Topic: Docker Compose

| Command | Description |
|---------|-------------|
| `docker compose up` | Start services |
| `docker compose up -d` | Start detached |
| `docker compose up --build` | Rebuild images |
| `docker compose down` | Stop and remove containers |
| `docker compose down -v` | Also remove volumes |
| `docker compose ps` | List services |
| `docker compose logs -f SERVICE` | Follow service logs |
| `docker compose exec SERVICE bash` | Shell into service |
| `docker compose restart SERVICE` | Restart service |
| `docker compose config` | Validate compose file |

## Topic: Useful Patterns

```bash
# Run one-off command and remove
docker run --rm -it ubuntu:22.04 bash

# Stop all containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all images
docker rmi $(docker images -q)

# Get container IP
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' CONTAINER

# Shell into running container
docker exec -it $(docker ps -q -f name=myapp) bash

# Check container health
docker inspect --format='{{.State.Health.Status}}' CONTAINER
```
