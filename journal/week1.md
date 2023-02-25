# Week 1 — App Containerization

## Required Homework/Tasks

### Containerize Application (Dockerfiles, Docker Compose)

- Created a [Dockerfile](../backend-flask/Dockerfile) in ./backend-flask and a [Dockerfile](../frontend-react-js/Dockerfile) ./frontend-reactjs to create docker images.

- Created a [docker-compose.yml](../docker-compose.yml) file in the main directory to be able to define and run multi-container applications (Flask, ReactJS, Postgres and DynamoDB)

### Document the Notification Endpoint for the OpenAI Document

- Briefly went over the [OpenAPI Specifications](https://spec.openapis.org/oas/latest.html) documentation  

- Updated [openapi-3.0.yml](../backend-flask/openapi-3.0.yml) to add a new notifications endpoint

### Write a Flask Backend Endpoint for Notifications

- Created a notification endpoint by:
    - Creating [notification_activities](../backend-flask/services/notifications_activities.py) 
    - Updating [app.py](../backend-flask/app.py)

### Write a React Page for Notifications

- Fixed up the notificaton page by:
    - Creating [NotificationsFeedPage.css](../frontend-react-js/src/pages/NotificationsFeedPage.css)
    - Creating [NotificationsFeedPage.js](../frontend-react-js/src/pages/NotificationsFeedPage.js)
    - Updating [App.js](../frontend-react-js/src/App.js)

### Run DynamoDB Local Container and ensure it works

- Made appropriate changes to the [docker-compose.yml](../docker-compose.yml) using a prebuilt image ([amazon/dynamodb-local](https://hub.docker.com/r/amazon/dynamodb-local))
- Ran "docker compose up" and tested it with examples from [100 Days of Cloud](https://github.com/100DaysOfCloud/challenge-dynamodb-local)

### Run Postgres Container and ensure it works

- Made appropriate changes to the [docker-compose.yml](../docker-compose.yml) using a prebuilt image ([postgres](https://hub.docker.com/_/postgres))
- Ran "docker compose up" and tested it connecting via psql

```bash
$ psql -U postgres -h localhost postgres
```


## Homework Challenges

### Run the dockerfile CMD as an external script

### Push and tag a image to DockerHub (they have a free tier)

### Use multi-stage building for a Dockerfile build

### Implement a healthcheck in the V3 Docker compose file

### Research best practices of Dockerfiles and attempt to implement it in your Dockerfile

### Learn how to install Docker on your localmachine and get the same containers running outside of Gitpod / Codespaces

### Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes. 
