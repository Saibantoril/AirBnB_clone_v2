#!/usr/bin/python3

import os.path
from datetime import datetime
from fabric.api import env, local, put, run

env.hosts = ['100.25.19.204', '54.157.159.85']


def do_pack():
    # Create a tar gzipped archive of the directory web_static
    now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    archive = 'versions/web_static_{}.tgz'.format(now)

    # Make sure the 'versions' directory exists
    local('mkdir -p versions')

    # Create the archive
    if local('tar -czvf {} web_static'.format(archive)).failed:
        return None
    return archive


def do_deploy(archive_path):
    # Distribute an archive to a web server
    if not os.path.isfile(archive_path):
        return False

    # Extract the name of the archive without the file extension
    archive_name = os.path.splitext(os.path.basename(archive_path))[0]

    # Create a directory for the new release
    if run('mkdir -p /data/web_static/releases/{}/'.format(archive_name)).failed:
        return False

    # Upload the archive to the remote server
    if put(archive_path, '/tmp/').failed:
        return False

    # Extract the contents of the archive into the new release directory
    if run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(os.path.basename(archive_path), archive_name)).failed:
        return False

    # Remove the uploaded archive
    if run('rm /tmp/{}'.format(os.path.basename(archive_path))).failed:
        return False

    # Move the contents of the web_static directory to the new release directory
    if run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(archive_name, archive_name)).failed:
        return False

    # Remove the old symlink
    if run('rm -rf /data/web_static/current').failed:
        return False

    # Create a new symlink to the new release directory
    if run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(archive_name)).failed:
        return False

    return True


def deploy():
    # Create and distribute an archive to a web server
    archive = do_pack()
    if not archive:
        return False
    return do_deploy(archive)
