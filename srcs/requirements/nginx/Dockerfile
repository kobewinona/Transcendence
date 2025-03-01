FROM debian:bullseye-slim

LABEL org.opencontainers.image.authors="Lera, Dima, Jeremy"

# Install dependencies
RUN apt-get update && apt-get install -y \
    g++ flex bison curl apache2-dev doxygen libyajl-dev ssdeep \
    liblua5.2-dev libgeoip-dev libtool dh-autoreconf libcurl4-gnutls-dev \
    libxml2 libpcre++-dev libxml2-dev git liblmdb-dev libpkgconf3 \
    lmdb-doc pkgconf zlib1g-dev libssl-dev wget make \
    systemctl vim \
    && apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install ModSecurity
RUN git clone --depth 1 -b v3.0.12 https://github.com/SpiderLabs/ModSecurity.git \
    && cd ModSecurity \
    && git submodule init \
    && git submodule update \
    && ./build.sh \
    && ./configure \
    && make \
    && make install \
    && cd ..

# Install modsecurity-nginx and nginx
RUN wget http://nginx.org/download/nginx-1.27.3.tar.gz \
    && tar -xzf nginx-1.27.3.tar.gz \
    && git clone https://github.com/SpiderLabs/ModSecurity-nginx.git \
    && cd nginx-1.27.3 \
    && ./configure --user=nginx --group=nginx \
       --with-pcre-jit --with-debug --with-compat \
       --with-http_ssl_module --with-http_realip_module \
       --add-dynamic-module=../ModSecurity-nginx \
    && make modules \
    && make install \
    && ln -s /usr/local/nginx/sbin/nginx /usr/local/sbin/nginx \
    && cd ..

# Copy the config files
COPY conf/nginx.conf /usr/local/nginx/conf/nginx.conf
COPY conf/modsecurity.conf /usr/local/nginx/conf/modsecurity.conf
COPY conf/unicode.mapping /usr/local/nginx/conf/unicode.mapping
COPY conf/owasp-crs /usr/local/nginx/conf/owasp-crs

# Configure the nginx user
RUN useradd -r -M -s /sbin/nologin nginx

# Expose port 443 and 80, and start nginx
EXPOSE 80 443

# Copy entrypoint script and make it executable
COPY ./tools/entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

CMD ["nginx", "-g", "daemon off;"]