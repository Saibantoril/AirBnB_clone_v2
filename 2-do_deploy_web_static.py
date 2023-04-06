#!/usr/bin/env python3
"""
Distributes an archive to web servers using Fabric and the do_deploy function.
"""

from fabric.api import *
from os import path

env.hosts = ['52.87.219.241', '54.242.162.151']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

def do_deploy(archive_path):
    """
    Deploys web files to server
    """
    if not path.exists(archive_path):
        return False

    try:
        # Upload archive
        put(archive_path, '/tmp/')

        # Create target directory
        archive_filename = archive_path.split("/")[-1]
        archive_basename = archive_filename.split(".")[0]
        release_path = "/data/web_static/releases/" + archive_basename
        run("sudo mkdir -p " + release_path)

        # Uncompress archive and delete .tgz
        run("sudo tar -xzf /tmp/" + archive_filename + " -C " + release_path + "/")
        run("sudo rm /tmp/" + archive_filename)

        # Move contents into host web_static
        run("sudo mv " + release_path + "/web_static/* " + release_path + "/")
        run("sudo rm -rf " + release_path + "/web_static")

        # Delete pre-existing symbolic link
        run("sudo rm -rf /data/web_static/current")

        # Create new symbolic link
        run("sudo ln -s " + release_path + " /data/web_static/current")
    except Exception as e:
        print(e)
        return False

    return True

def deploy():
    """
    Runs the do_deploy function on all hosts in env.hosts
    """
    archive_path = "web_static_{}.tgz".format(datetime.now().strftime("%Y%m%d%H%M%S"))
    local("tar -czvf {} web_static/".format(archive_path))

    results = execute(do_deploy, archive_path)

    if all(results.values()):
        print("All deployments successful")
    else:
        print("Deployment failed on some hosts")
