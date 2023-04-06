#!/usr/bin/env bash

# This script sets up the web server for deployment of web_static by:
# - Installing Nginx if not already installed
# - Creating the necessary directory structure for web_static deployment
# - Creating a fake HTML file to test Nginx configuration
# - Creating a symbolic link /data/web_static/current linked to /data/web_static/releases/test/
# - Giving ownership of /data/ to the ubuntu user and group recursively
# - Updating Nginx configuration to serve /data/web_static/current/ to hbnb_static

# Install Nginx if not already installed

if ! which nginx > /dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create directory structure for web_static deployment
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared /data/web_static/current

# Create a fake HTML file to test Nginx configuration
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link /data/web_static/current linked to /data/web_static/releases/test/
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve /data/web_static/current/ to hbnb_static
sudo sed -i "/listen 80 default_server;/a location /hbnb_static/ {\n\talias /data/web_static/current/;\n\t}" /etc/nginx/sites-available/default

# Restart Nginx to apply configuration changes
sudo service nginx restart
