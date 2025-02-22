# Step 1 : Use Debian image
FROM debian:bullseye-slim

# Step 2 : Install usefull dependencies
RUN apt-get update && apt-get install -y \
    g++ flex bison curl apache2-dev doxygen libyajl-dev ssdeep \
    liblua5.2-dev libgeoip-dev libtool dh-autoreconf libcurl4-gnutls-dev \
    libxml2 libpcre++-dev libxml2-dev git liblmdb-dev libpkgconf3 \
    lmdb-doc pkgconf zlib1g-dev libssl-dev wget make \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Step 3 : Install ModSecurity
RUN set -e && \
    git clone --depth 1 -b v3.0.12 https://github.com/SpiderLabs/ModSecurity.git && \
    cd ModSecurity && \
    git submodule init && \
    git submodule update && \
    ./build.sh && \
    ./configure && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf ModSecurity /var/tmp/*

# Step 4 : Install modsecurity-nginx and NGINX
RUN set -e && \
    wget http://nginx.org/download/nginx-1.27.3.tar.gz && \
    tar -xzf nginx-1.27.3.tar.gz && \
    git clone https://github.com/SpiderLabs/ModSecurity-nginx.git && \
    cd nginx-1.27.3 && \
    ./configure --user=nginx --group=nginx \
       --with-pcre-jit --with-debug --with-compat \
       --with-http_ssl_module --with-http_realip_module \
       --add-dynamic-module=../ModSecurity-nginx && \
    make -j$(nproc) modules && \
    make install && \
    mkdir -p /usr/local/nginx/modules && \
    cp objs/ngx_http_modsecurity_module.so /usr/local/nginx/modules/ && \
    ln -s /usr/local/nginx/sbin/nginx /usr/local/sbin/nginx && \
    cd .. && \
    rm -rf nginx-1.27.3 nginx-1.27.3.tar.gz ModSecurity-nginx /var/tmp/*

# Step 5 : Copy the config files
RUN mkdir -p /usr/local/nginx/conf
COPY conf/nginx.conf /usr/local/nginx/conf/nginx.conf
COPY conf/modsecurity.conf /usr/local/nginx/conf/modsecurity.conf
COPY conf/unicode.mapping /usr/local/nginx/conf/unicode.mapping
COPY conf/owasp-crs /usr/local/nginx/conf/owasp-crs

# Step 6 : Configure the NGINX User
RUN chown -R www-data:www-data /usr/local/nginx/

RUN mkdir -p /usr/local/nginx/logs \
    && touch /usr/local/nginx/logs/modsec_debug.log \
    && chown -R www-data:www-data /usr/local/nginx/logs

# Step 7 : Creat repo for logs
RUN mkdir -p /var/log/nginx /var/log/modsecurity \
    && touch /var/log/nginx/access.log /var/log/nginx/error.log \
    && touch /var/log/modsecurity/modsec_debug.log \
    && chown -R www-data:www-data /var/log/nginx /var/log/modsecurity

# Step 8 : Copy the script entrypoint
COPY tools/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Step 9 : Expose port 443 and 80, and start NGINX
EXPOSE 80 443
CMD ["/entrypoint.sh"]
