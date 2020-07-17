FROM nginx

ADD ./config /etc/nginx/conf.d
ADD ./static /static

ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["nginx", "-g", "daemon off;"]
