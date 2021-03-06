from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

import sys
import os.path

def __initialize__():
    env.user = 'dcramer'
    env.password = ''
    env.key_filename = os.path.expanduser('~/.ssh/id_rsa.pub')
    env.core = True
    env.python_version = '.'.join(map(str, sys.version_info[0:2]))
    # django-south
    env.south = True
    env.domain_name = ''
    env.project_name = 'galaxyvalidator'
    env.path_to_settings = os.path.join(env.path, 'settings.py')
    #env.media_root = os.path.join(env.path, 'media')
    env.repo_copy = os.path.join(env.path, 'sources', env.project_name)
    env.repo_url = 'git@github.com:dcramer/galaxyvalidator.git'

def www():
    env.hosts = ['sars.nibbits.com']
    env.system_type = 'production'
    env.path = '/home/dcramer/galaxyvalidator.com/'
    env.virtualenv_path = '/home/dcramer/.virtualenvs/galaxyvalidator/'
    __initialize__()

def local():
    env.path = os.path.expanduser('~/Development/galaxyvalidator/')
    env.virtualenv_path = os.path.expanduser('~/.virtualenvs/galaxyvalidator/')
    env.system_type = 'dev'
    __initialize__()

def setup():
    require('virtualenv_path')
    require('hosts')
    require('path')
    require('repo_url')
    
    sudo('aptitude install -y python-setuptools')
    sudo('easy_install pip')
    sudo('easy_install virtualenv')
    sudo('easy_install virtualenvwrapper')
    sudo('aptitude install -y unzip')
    sudo('aptitude install -y apache2')
    sudo('aptitude install -y python-dev')
    # lxml
    # sudo('aptitude install -y libxml2-dev')
    # sudo('aptitude install -y libxslt1-dev')
    # pil
    sudo('aptitude install -y libjpeg62-dev')
    sudo('aptitude install -y libpng12-0-dev')
    # pygame
    # sudo('aptitude install -y libsdl-image1.2')
    # sudo('aptitude install -y libsdl-mixer1.2')
    # sudo('aptitude install -y libsdl-ttf2.0-0')
    sudo('aptitude install -y libmysqlclient-dev')
    sudo('aptitude install -y memcached')
    sudo('aptitude install -y libapache2-mod-wsgi')
    sudo('aptitude install -y subversion')
    sudo('aptitude install -y git-core')
    sudo('aptitude install -y mercurial')

    # the rest runs as our user
    run('rm -rf %(repo_copy)s' % dict(path=env.path, repo_copy=env.repo_copy))
    run('git clone %(repo_url)s %(repo_copy)s' % dict(repo_url=env.repo_url, repo_copy=env.repo_copy))
    run('mkdir -p %(path)s && cd %(path)s && virtualenv --clear --no-site-packages %(virtualenv_path)s' % dict(path=env.path, virtualenv_path=env.virtualenv_path))
    run('cd %(path)s && mkdir -p releases/%(project_name)s cache sphinx/{data,run,log} packages sources logs' % dict(path=env.path, project_name=env.project_name))
    run('ln -fs %(path)sreleases/%(project_name)s/current/%(project_name)s %(path)sproject' % dict(path=env.path, project_name=env.project_name))
    run('touch %(path_to_settings)s' % dict(path_to_settings=env.path_to_settings))
    #update_owner(env.path, 'www-data', 'www-data')
    #update_mode(env.path, '770')

def deploy(version=None):
    import time

    if version is None:
        env.release = time.strftime('%Y%m%d%H%M%S')
        update_sources()
        install_sources()
        install_requirements()
        symlink_current_release()
        syncdb()
        #synccompress()
        #update_media()
        compile()
        #install_site()
    else:
        env.release = version

        if env.core:
            run('cd %(path)s && rm releases/%(project_name)s/previous; mv releases/%(project_name)s/current releases/%(project_name)s/previous;' % dict(path=env.path, project_name=env.project_name))
            run('cd %(path)sreleases/%(project_name)s/ && rm -f current && ln -fs %(project_name)s-%(release)s current' % dict(path=env.path, release=env.release, project_name=env.project_name))

    run('%(virtualenv_path)sbin/python %(path)sreleases/%(project_name)s/current/setup.py develop' % dict(path=env.path, project_name=env.project_name, virtualenv_path=env.virtualenv_path))
    restart_web()

def rollback():
    require('hosts')
    require('path')
    require('core')

    if env.core:
        run('cd %(path)s && mv releases/%(project_name)s/current releases/%(project_name)s/_previous' % dict(path=env.path, project_name=env.project_name))
        run('cd %(path)s && mv releases/%(project_name)s/previous releases/%(project_name)s/current' % dict(path=env.path, project_name=env.project_name))
        run('cd %(path)s && mv releases/%(project_name)s/_previous releases/%(project_name)s/previous' % dict(path=env.path, project_name=env.project_name))

    restart_web()

def update_sources():
    require('repo_copy')
    require('repo_url')
    run("cd %(repo_copy)s && \
         git pull" % dict(repo_url=env.repo_url, repo_copy=env.repo_copy))

def install_sources():
    require('repo_copy')
    require('release', provided_by=[deploy, setup])
    require('core')
    require('path')
    require('system_type')
    require('project_name')
    require('path_to_settings')
    
    if env.core:
        run('cd %(repo_copy)s && git archive --format=tar HEAD | gzip >%(path)spackages/%(project_name)s-%(release)s.tar.gz' % dict(repo_copy=env.repo_copy, path=env.path, release=env.release, project_name=env.project_name))
        run('cd %(path)sreleases/%(project_name)s/ && mkdir %(project_name)s-%(release)s && cd %(project_name)s-%(release)s && tar zxf ../../../packages/%(project_name)s-%(release)s.tar.gz' % dict(path=env.path, release=env.release, project_name=env.project_name))
        run('cd %(path)spackages/ && rm %(project_name)s-%(release)s.tar.gz' % dict(path=env.path, release=env.release, project_name=env.project_name))
        run('ln -fs %(path_to_settings)s %(path)sreleases/%(project_name)s/%(project_name)s-%(release)s/%(project_name)s/local_settings.py' % dict(path=env.path, release=env.release, system_type=env.system_type, project_name=env.project_name, path_to_settings=env.path_to_settings))

def install_site():
    require('domain_name')
    run('cp %(path)sreleases/%(project_name)s/current/%(project_name)s/%(domain_name)s.conf /etc/apache2/sites-available/' % dict(path=env.path, domain_name=env.domain_name, project_name=env.project_name))
    run('cd /etc/apache2/sites-available/; a2ensite %(domain_name)s' % dict(domain_name=env.domain_name))

def install_requirements():
    require('virtualenv_path')
    require('release', provided_by=[deploy, setup])
    require('path')
    require('project_name')

    #run('cd %(path)s && pip install -E . -f http://pypi.python.org/packages/source/p/path.py/path-2.2.zip path' % dict(path=env.path))
    run('cd %(path)s && %(virtualenv_path)sbin/pip install -E %(virtualenv_path)s -f ipython' % dict(path=env.path, virtualenv_path=env.virtualenv_path))
    
    run('cd %(path)s && %(virtualenv_path)sbin/pip install -E %(virtualenv_path)s -r %(path)sreleases/%(project_name)s/%(project_name)s-%(release)s/requirements.txt' % dict(path=env.path, release=env.release, project_name=env.project_name, virtualenv_path=env.virtualenv_path))

def symlink_current_release():
    require('release', provided_by=[deploy, setup])
    require('path')
    require('core')
    require('project_name')

    if env.core:
        #update_owner('%(path)sreleases/%(project_name)s/%(project_name)s-%(release)s/' % dict(path=env.path, release=env.release), 'www-data', 'www-data')
        #update_mode('%(path)sreleases/%(project_name)s/%(project_name)s-%(release)s/' % dict(path=env.path, release=env.release, project_name=env.project_name), '770')
        with settings(warn_only=True):
            result = run('cd %(path)s && rm -f releases/%(project_name)s/previous && mv releases/%(project_name)s/current releases/%(project_name)s/previous' % dict(path=env.path, project_name=env.project_name))
        if result.failed and not confirm("Failed to create restore point. Continue anyways?"):
            abort("Aborting at user request.")
        run('cd %(path)sreleases/%(project_name)s/ && rm -f current && ln -fs %(project_name)s-%(release)s current' % dict(path=env.path, release=env.release, project_name=env.project_name))
        run('ln -fs %(path)sreleases/%(project_name)s/current/%(project_name)s %(virtualenv_path)slib/python%(python_version)s/site-packages/%(project_name)s' % dict(path=env.path, project_name=env.project_name, python_version=env.python_version, virtualenv_path=env.virtualenv_path))

def syncdb():
    require('path')
    require('project_name')
    cmds = ['syncdb']
    if env.south:
        cmds.append('migrate')
    #cmds.append('loaddata fixtures/auth_user.json')
    
    run("cd %(path)sreleases/%(project_name)s/current/%(project_name)s/ && %(commands)s" % dict(
        path=env.path,
        project_name=env.project_name,
        commands=' && '.join('%sbin/python manage.py %s' % (env.virtualenv_path, command,) for command in cmds),
    ))

# def ve_run(cmd):
#     run("cd %(path)sreleases/%(project_name)s/current/%(project_name)s/ && %(command)s" % dict(
#         path=env.path,
#         project_name=env.project_name,
#     )

def finalize_purchases(deal_id):
    require('path')
    require('project_name')
    cmds = ['finalize_purchases %s' % deal_id]
    
    run("cd %(path)sreleases/%(project_name)s/current/%(project_name)s/ && %(commands)s" % dict(
        path=env.path,
        project_name=env.project_name,
        commands=' && '.join('%sbin/python manage.py %s' % (env.virtualenv_path, command,) for command in cmds),
    ))

def give_deal(deal_id, email):
    require('path')
    require('project_name')
    cmds = ['give_deal %s %s' % (deal_id, email)]
    
    run("cd %(path)sreleases/%(project_name)s/current/%(project_name)s/ && %(commands)s" % dict(
        path=env.path,
        project_name=env.project_name,
        commands=' && '.join('%sbin/python manage.py %s' % (env.virtualenv_path, command,) for command in cmds),
    ))

def run_manage_command(command):
    require('virtualenv_path')
    require('path')
    require('project_name')
    run("cd %(path)sreleases/%(project_name)s/current/%(project_name)s/ && \
         %(virtualenv_path)sbin/python manage.py %(command)s" % dict(virtualenv_path=env.virtualenv_path, path=env.path, project_name=env.project_name, command=command))

@runs_once
def synccompress():
    run_manage_command('synccompress --force')

@runs_once
def update_media():
    require('path')
    require('media_root')
    run ('mkdir -p %(media_root)s/' % dict(path=env.path, media_root=env.media_root, project_name=env.project_name))

def compile():
    require('virtualenv_path')
    require('path')
    require('project_name')
    with settings(warn_only=True):
        result = run("%(virtualenv_path)sbin/python -c \"import compileall; import re; compileall.compile_dir('%(path)sreleases/%(project_name)s/current/%(project_name)s/',force=True, quiet=True)\"" % dict(path=env.path, project_name=env.project_name, virtualenv_path=env.virtualenv_path))
    if result.failed and not confirm("Failed to compile site. Continue anyways?"):
        abort("Aborting at user request.")

def update_owner(path, user, group):
    sudo("chown -R %(user)s:%(group)s %(path)s" % dict(path=path, user=user, group=group))

def update_mode(path, mode):
    sudo("chmod -R %(mode)s %(path)s" % dict(path=path, mode=mode))

def restart_web():
    require('path')
    require('project_name')
    run('touch %(path)sreleases/%(project_name)s/current/%(project_name)s/handler.wsgi' % dict(path=env.path, project_name=env.project_name))

def restart_memcached():
    sudo('/etc/init.d/memcached restart')

def init_search():
    require('path')
    require('project_name')
    run('cd %(path)sreleases/%(project_name)s/current/ && PATH=%(path)sbin:$PATH DJANGO_SETTINGS_MODULE=%(project_name)s.settings indexer --config %(path)sreleases/iplatform/current/iplatform/conf/sphinx.py --all' % dict(path=env.path, project_name=env.project_name))

def update_search():
    require('path')
    require('project_name')
    run('cd %(path)sreleases/%(project_name)s/current/ && PATH=%(path)sbin:$PATH DJANGO_SETTINGS_MODULE=%(project_name)s.settings indexer --config %(path)sreleases/iplatform/current/iplatform/conf/sphinx.py --all --rotate' % dict(path=env.path, project_name=env.project_name))

def restart_search():
    require('path')
    require('project_name')
    run('kill -9 $(cat %(path)ssphinx/run/searchd.pid); cd %(path)sreleases/%(project_name)s/current/ && PATH=%(path)sbin:$PATH DJANGO_SETTINGS_MODULE=%(project_name)s.settings searchd --config %(path)sreleases/iplatform/current/iplatform/conf/sphinx.py' % dict(path=env.path, project_name=env.project_name))