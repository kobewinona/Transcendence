FROM node:18-alpine

# Set the metadata for the image an author
LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

# Create app directory
WORKDIR /usr/src/app

# Copy package.json and yarn.lock
COPY package.json yarn.lock ./

# Install app dependencies
RUN yarn install

# Bundle app source
COPY . .

# Build the app
RUN yarn build
