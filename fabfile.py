import os

from fabric.api import *

@task
def prod():
    env.hosts = ['open13.ca']
    env.user = 'open13'
    env.base_dir = '/home/open13'
    _env_setup()
    
def _env_setup():
    env.virtualenv_bin = os.path.join(env.base_dir, '.virtualenvs', 'open13', 'bin')
    env.python = os.path.join(env.virtualenv_bin, 'python')
    env.django_dir = os.path.join(env.base_dir, 'open13', 'website')
    
@task
def deploy():
    pull()
    statics()
    reload()
    
@task
def pull():
    with cd(os.path.join(env.base_dir, 'billy')):
        run('git pull')
    with cd(os.path.join(env.base_dir, 'open13')):
        run('git pull')
        
@task
def statics():
    with cd(env.django_dir):
        run('%s manage.py collectstatic --noinput' % env.python)
        
@task
def reload():
    with cd(env.base_dir):
        run('kill -HUP `cat gunicorn/gunicorn.pid`')