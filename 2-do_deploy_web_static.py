from fabric import Connection
from datetime import datetime

env.hosts = ['100.25.19.204', '54.157.159.85']

def do_deploy(archive_path):
    try:
        c = Connection(env.hosts[0])
        if not c.is_connected():
            c.connect()
        if not c.run('test -d /data/web_static/releases/').ok:
            c.sudo('mkdir -p /data/web_static/releases/')
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        c.put(archive_path, '/tmp')
        c.run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/'.format(
            archive_path.split('/')[-1]))
        c.run('sudo rm /tmp/{}'.format(archive_path.split('/')[-1]))
        c.run('sudo mv /data/web_static/releases/web_static /data/web_static/releases/{}'.
              format(timestamp))
        c.run('sudo rm -rf /data/web_static/current')
        c.run('sudo ln -s /data/web_static/releases/{} /data/web_static/current'.
              format(timestamp))
        c.close()
    except Exception as e:
        return False
    return True
