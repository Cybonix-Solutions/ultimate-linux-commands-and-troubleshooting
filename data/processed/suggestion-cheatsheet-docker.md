# Docker Cheatsheet - Suggested Addition

**Target:** cheatsheets/docker-cheatsheet.md (new file)
**Priority:** High (essential for modern infrastructure)

---

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

---

## Topic: Container Inspection

| Command | Description |
|---------|-------------|
| `docker ps` | Running containers |
| `docker ps -a` | All containers (including stopped) |
| `docker ps -q` | Only container IDs |
| `docker logs CONTAINER` | View logs |
| `docker logs -f CONTAINER` | Follow logs |
| `docker logs --tail 100 CONTAINER` | Last 100 lines |
| `docker logs --since 1h CONTAINER` | Last hour |
| `docker inspect CONTAINER` | Full container details (JSON) |
| `docker top CONTAINER` | Running processes |
| `docker stats` | Live resource usage |
| `docker diff CONTAINER` | Changed files |
| `docker port CONTAINER` | Port mappings |

---

## Topic: Executing in Containers

| Command | Description |
|---------|-------------|
| `docker exec -it CONTAINER bash` | Interactive shell |
| `docker exec CONTAINER command` | Run command |
| `docker exec -u root CONTAINER command` | Run as root |
| `docker attach CONTAINER` | Attach to main process |
| `docker cp file CONTAINER:/path` | Copy file into container |
| `docker cp CONTAINER:/path file` | Copy file from container |

---

## Topic: Images

| Command | Description |
|---------|-------------|
| `docker images` | List local images |
| `docker pull IMAGE:TAG` | Download image |
| `docker push IMAGE:TAG` | Push to registry |
| `docker build -t NAME:TAG .` | Build from Dockerfile |
| `docker build -f Dockerfile.dev .` | Specify Dockerfile |
| `docker tag IMAGE NEW_NAME:TAG` | Tag image |
| `docker rmi IMAGE` | Remove image |
| `docker image prune` | Remove unused images |
| `docker history IMAGE` | Show image layers |
| `docker save IMAGE > file.tar` | Export image to tar |
| `docker load < file.tar` | Import image from tar |

---

## Topic: Volumes and Networks

**Volumes:**
| Command | Description |
|---------|-------------|
| `docker volume ls` | List volumes |
| `docker volume create NAME` | Create volume |
| `docker volume rm NAME` | Remove volume |
| `docker volume inspect NAME` | Volume details |
| `docker volume prune` | Remove unused volumes |
| `-v NAME:/container/path` | Mount named volume |
| `-v /host/path:/container/path` | Bind mount |
| `-v /host/path:/container/path:ro` | Read-only mount |

**Networks:**
| Command | Description |
|---------|-------------|
| `docker network ls` | List networks |
| `docker network create NAME` | Create network |
| `docker network rm NAME` | Remove network |
| `docker network inspect NAME` | Network details |
| `docker network connect NET CONTAINER` | Connect container |
| `docker network disconnect NET CONTAINER` | Disconnect |
| `--network=NAME` | Use network when running |
| `--network=host` | Use host networking |

---

## Topic: Cleanup Commands

| Command | Description |
|---------|-------------|
| `docker system df` | Disk usage |
| `docker system prune` | Remove unused data |
| `docker system prune -a` | Remove all unused (including images) |
| `docker container prune` | Remove stopped containers |
| `docker image prune` | Remove dangling images |
| `docker image prune -a` | Remove all unused images |
| `docker volume prune` | Remove unused volumes |
| `docker network prune` | Remove unused networks |

---

## Topic: Docker Compose

| Command | Description |
|---------|-------------|
| `docker compose up` | Start services |
| `docker compose up -d` | Start detached |
| `docker compose up --build` | Rebuild images |
| `docker compose down` | Stop and remove containers |
| `docker compose down -v` | Also remove volumes |
| `docker compose ps` | List services |
| `docker compose logs` | View logs |
| `docker compose logs -f SERVICE` | Follow service logs |
| `docker compose exec SERVICE bash` | Shell into service |
| `docker compose build` | Build images |
| `docker compose pull` | Pull images |
| `docker compose restart SERVICE` | Restart service |
| `docker compose stop` | Stop services |
| `docker compose start` | Start stopped services |
| `docker compose config` | Validate compose file |

---

## Topic: Dockerfile Quick Reference

```dockerfile
FROM ubuntu:22.04                  # Base image
LABEL maintainer="email@example"   # Metadata
ENV VAR=value                      # Environment variable
WORKDIR /app                       # Set working directory
COPY . .                           # Copy files from build context
COPY --chown=user:group . .        # Copy with ownership
ADD url /path                      # Copy + extract + remote URL
RUN apt-get update && apt-get install -y pkg  # Run command
RUN --mount=type=cache,target=/var/cache/apt apt-get install -y pkg
EXPOSE 8080                        # Document port (doesn't publish)
USER nonroot                       # Switch user
VOLUME /data                       # Define mount point
ENTRYPOINT ["executable"]          # Main command
CMD ["arg1", "arg2"]               # Default arguments
HEALTHCHECK CMD curl -f http://localhost/
```

**Multi-stage build:**
```dockerfile
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

FROM alpine:latest
COPY --from=builder /app/myapp /myapp
CMD ["/myapp"]
```

---

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

# Follow logs from all containers
docker compose logs -f

# Shell into running container
docker exec -it $(docker ps -q -f name=myapp) bash

# Export container filesystem
docker export CONTAINER > container.tar

# Check container health
docker inspect --format='{{.State.Health.Status}}' CONTAINER
```
