# Use OWASP ModSecurity CRS Apache image
FROM owasp/modsecurity-crs:3-apache-202308071108

# Set metadata for the image (authors)
LABEL org.opencontainers.image.authors="Dima, Wolf, Jeremy"

# Ensure the "apache" user exists
RUN getent passwd apache || useradd -r -M -s /sbin/nologin apache

# Install required utilities and clean unnecessary files
RUN apt-get update && apt-get install -y apache2-utils && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy main Apache configuration files
COPY ./conf/httpd.conf /usr/local/apache2/conf/httpd.conf
COPY ./conf/httpd-vhosts.conf /usr/local/apache2/conf/extra/httpd-vhosts.conf

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

# Switch to non-root user for security
USER apache

# Expose necessary ports
EXPOSE 80 443
    
# Start Apache in foreground
CMD ["httpd-foreground"]
