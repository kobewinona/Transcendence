# BASE IMAGE & AUTHOR INFORMATION
FROM node:20 AS build
LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

# SET WORKING DIRECTORY
WORKDIR /usr/src/app

# INSTALL YARN DEPENDENCIES
COPY package.json yarn.lock ./
RUN yarn install
COPY . .
RUN yarn build

# EXECUTION STATUS MESSAGE
CMD ["echo", "Frontend build completed successfully"]
