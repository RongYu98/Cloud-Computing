FROM nginx:alpine

# COPY hw0.html /usr/share/nginx/html # running this in the hw0 html page?
COPY hw0.html /var/www/html
# COPY /home/ubuntu/Cloud-Computing/Dockerfile /usr/share/nginx/html

# COPY /etc/nginx/nginx.conf /etc/nginx/nginx.conf
# the above is not the right path.....