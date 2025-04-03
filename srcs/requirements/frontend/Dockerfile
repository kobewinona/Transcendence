# BASE IMAGE & AUTHOR INFORMATION
FROM node:20 AS build

LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

ARG VITE_API_URL
ARG VITE_WS_URL

ENV VITE_API_URL=$VITE_API_URL
ENV VITE_WS_URL=$VITE_WS_URL

# SET WORKING DIRECTORY
WORKDIR /usr/src/app

# INSTALL YARN DEPENDENCIES
COPY package.json yarn.lock ./
RUN yarn install
COPY . .
RUN yarn build

# EXECUTION STATUS MESSAGE
CMD ["echo", "Frontend build completed successfully"]
