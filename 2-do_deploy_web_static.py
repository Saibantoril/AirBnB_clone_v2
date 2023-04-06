#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers, using the function do_deploy
"""

import os.path
from fabric.api import *

env.hosts = ['52.87.219.241', '54.242.162.151']
env.user = 'ubuntu'

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers, using the function do_deploy
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload archive to the web server
        put(archive_path, "/tmp/")

        # Get filename without extension
        filename = archive_path.split("/")[-1]
        name = filename.split(".")[0]

        # Create directory for the archive
        run("sudo mkdir -p /data/web_static/releases/{}".format(name))

        # Uncompress archive
        run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(filename, name))

        # Remove archive
        run("sudo rm /tmp/{}".format(filename))

        # Move files to the proper directory
        run("sudo mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name, name))

        # Remove unnecessary directory
        run("sudo rm -rf /data/web_static/releases/{}/web_static".format(name))

        # Remove old symbolic link and create new one
        run("sudo rm -f /data/web_static/current")
        run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False
