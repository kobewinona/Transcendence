# FROM nginx:stable

# LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

# COPY conf/nginx.conf /etc/nginx/nginx.conf

# RUN chmod 644 /etc/nginx/nginx.conf && chown root:root /etc/nginx/nginx.conf

# EXPOSE 80 443

# ENTRYPOINT [ "nginx", "-g", "daemon off;" ]

# Step 1 : Use Debian image
FROM debian:bullseye-slim

# Step 2 : Install usefull dependencies
RUN apt-get update && apt-get install -y \
    g++ flex bison curl apache2-dev doxygen libyajl-dev ssdeep \
    liblua5.2-dev libgeoip-dev libtool dh-autoreconf libcurl4-gnutls-dev \
    libxml2 libpcre++-dev libxml2-dev git liblmdb-dev libpkgconf3 \
    lmdb-doc pkgconf zlib1g-dev libssl-dev wget make \
    systemctl vim \
    && apt-get clean

# Step 3 : Install ModSecurity
RUN git clone --depth 1 -b v3.0.12 https://github.com/SpiderLabs/ModSecurity.git \
    && cd ModSecurity \
    && git submodule init \
    && git submodule update \
    && ./build.sh \
    && ./configure \
    && make \
    && make install \
    && cd ..

# Step 4 : Install modsecurity-nginx and NGINX
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

# # Step 5 : Copy the config files
COPY conf/nginx.conf /usr/local/nginx/conf/nginx.conf
COPY conf/modsecurity.conf /usr/local/nginx/conf/modsecurity.conf
COPY conf/unicode.mapping /usr/local/nginx/conf/unicode.mapping
COPY conf/owasp-crs /usr/local/nginx/conf/owasp-crs

# # Step 6 : Configure the NGINX User
RUN useradd -r -M -s /sbin/nologin nginx

# # Step 7 : Expose port 443 and 80, and start NGINX
EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]