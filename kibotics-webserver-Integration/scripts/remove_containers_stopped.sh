jderobot@postre:~/JdeRobot-Kids-App/scripts$ cat remove_containers_stopped.sh
#!/bin/bash


docker rm $(docker ps -a -q -f 'status=exited' -f 'ancestor=94ac1bdaae91')
