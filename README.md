# snowdler
The software setup for the Junkfunnel Montana Data Transmitter Home Version

Install steps

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

    sudo mkdir /var/log/django
    sudo chown pi /var/log/django


hookup our supervisor config (symlink into etc)
    sudo ln -s ~/snowdler/configs/supervisor-programs.conf /etc/supervisor/conf.d/supervisor-programs.conf

Install the gpio python lib # I think this is already in by default

    sudo apt-get install python3-rpi.gpio


## for the Nokia screen ##

    git clone git://git.drogon.net/wiringPi
    cd wiringPi
    ./build

test that with
    ./build/gpio/gpio readall

more installs
    sudo pip3 install wiringpi2
    sudo apt-get install python3-dev python3-pil

    sudo pip3 install spidev


## Repair wifi dropout issue: ##
    sudo nano /etc/modprobe.d/8192cu.conf

and paste the following in
    # Disable power saving
    options 8192cu rtw_power_mgnt=0

Then reboot with sudo reboot

more info here: https://rtl8192cu.googlecode.com/hg/document/HowTo_enable_the_power_saving_functionality.pdf


## for dev env:
sudo apt-get remove python3-pip
sudo easy_install3 pip
