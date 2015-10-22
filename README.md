# snowdler
The software setup for the Junkfunnel Montana Data Transmitter Home Version

Install steps

#.
    sudo apt-get install nginx supervisor
    # then disable nginx in with systemd as we will control it with supervisor

    # sudo update-rc.d nginx disable
    sudo systemctl disable nginx

    rm /etc/nginx/site-enabled/default
    ln -s /home/pi/snowlder/configs/nginx_default /etc/nginx/sites-enabled/

systemd is the OS's init system that gets everything running.  Even though it handles autstarting nginx just fine, having supervisor do it means that supervisor is managing everything that doesn't come default with debaian, and everything that has to do with our app.  It makes life a lot easier when you run `sudo supervisorctl status` ad see just your tools, versus `sudo systemctl status` which talks about every single service.

    sudo pip3 install -r requirements.txt
    sudo mkdir /var/log/gunicorn
    sudo chown pi /var/log/gunicorn

#. hookup our supervisor config (symlink into etc)
    sudo ln -s ~/snowdler/configs/supervisor-programs.conf /etc/supervisor/conf.d/supervisor-programs.conf


