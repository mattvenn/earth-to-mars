# Installation

use apt-get install to install:

* numpy
* matplotlib 
* scipy

use pip to install requirements.txt:

    sudo pip install -r requirements.txt

install supervisord

    sudo apt-get install supervisor

and 
    sudo cp mc.conf /etc/supervisor/conf.d

then 

    sudo supervisorctl reread
    sudo supervisorctl reload

Setup a cronjob to rebuild graphs every minute:

    * * * * * cd earth-to-mars/missioncontrol/mc; ./update_group.py
