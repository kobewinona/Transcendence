# Use OWASP ModSecurity CRS Apache image
FROM owasp/modsecurity-crs:3-apache-202308071108

# Set metadata for the image (authors)
LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

# Ensure the "apache" user exists
RUN getent passwd apache || useradd -r -M -s /sbin/nologin apache

# Install required utilities and clean unnecessary files
RUN apt-get update && apt-get install -y apache2-utils procps inotify-tools && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy main Apache configuration files
COPY ./conf/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./conf/httpd-vhosts.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf
COPY ./conf/grafana-vhost.conf /usr/local/apache2/conf/extra/grafana-vhost.conf

# Copy ModSecurity configuration and rules
COPY ./conf/modsecurity.conf /usr/local/apache2/conf/modsecurity.conf
COPY ./conf/unicode.mapping /usr/local/apache2/conf/unicode.mapping
COPY ./conf/crs-setup.conf /usr/local/apache2/conf/crs-setup.conf
COPY ./conf/rules/ /usr/local/apache2/conf/rules/

# Ensure logs and required directories exist, set permissions
RUN mkdir -p /usr/local/apache2/run /etc/modsecurity.d /opt/owasp-crs /var/log && \
    touch /usr/local/apache2/logs/access.log /usr/local/apache2/logs/error.log && \
    touch /var/log/modsec_debug.log /var/log/modsec_audit.log && \
    chown -R apache:apache \
        /usr/local/apache2/logs \
        /usr/local/apache2/run \
        /usr/local/apache2/conf \
        /etc/modsecurity.d \
        /opt/owasp-crs \
        /var/log/modsec_debug.log /var/log/modsec_audit.log && \
    chmod -R 750 /usr/local/apache2/conf && \
    chmod -R 770 /usr/local/apache2/logs /usr/local/apache2/run /etc/modsecurity.d /opt/owasp-crs && \
    chmod 640 /var/log/modsec_debug.log /var/log/modsec_audit.log

# Remove the auto-generate certficate by the image
RUN echo '#!/bin/sh\nexit 0' > /usr/local/bin/generate-certificate && chmod +x /usr/local/bin/generate-certificate

# Switch to non-root user for security

# Expose necessary ports
EXPOSE 8080 8443

# Start Apache in foreground
# CMD ["httpd-foreground"]

COPY tools/watch_and_reload.sh /usr/local/bin/watch_and_reload.sh
RUN chmod +x /usr/local/bin/watch_and_reload.sh
USER apache

CMD ["/bin/sh", "-c", "httpd-foreground & /usr/local/bin/watch_and_reload.sh"]
