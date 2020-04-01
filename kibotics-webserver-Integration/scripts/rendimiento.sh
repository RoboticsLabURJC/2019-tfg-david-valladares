#!/bin/bash
for i in {1..12}
do
   docker run -d --rm --cpus=3.5 -e DISPLAY=:0 -e JDEROBOT_SIMULA0TION_TYPE=REMOTE -v /etc/letsencrypt/archive/kibotics.org:/etc/kids-certs/kibotics.org:ro --entrypoint /entrypoint_kidsweb.sh -v /tmp/siguelineaIR:/home/jderobot/volume/user/exercise:rw  -p 20000-21000:8888 -p 20000-21000:8080 -it  dockerhub.jderobot.org:5000/kibotics_simulation sigue_pelota_picam.world
done

