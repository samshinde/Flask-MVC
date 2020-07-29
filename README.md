## AnyServe Forun Project

# pre requisite

- Install docker, docker-compose
- Docker => https://docs.docker.com/v17.09/engine/installation/linux/docker-ce/ubuntu/#install-docker-ce-1
- Docker-Compose => https://docs.docker.com/compose/install/

# build and start project

- sudo docker-compose build
- suod docker-compose up -d

# to see logs of the service

- sudo docker-compose logs -f <<service_name>>
- e.g. sudo docker-compose logs -f web-app

# todo

1. Add see data in the application
2. Booking management facility
3. Flask Admin functionality

