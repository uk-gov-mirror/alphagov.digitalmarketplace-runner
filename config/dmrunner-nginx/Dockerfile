FROM alpine:3.5

RUN apk update && \
    apk add nginx && \
    adduser -D -u 1000 -g 'www' www && \
    mkdir -p /run/nginx && \
    touch /run/nginx/nginx.pid

COPY ./nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

ENTRYPOINT ["/usr/sbin/nginx", "-g", "daemon off;"]
