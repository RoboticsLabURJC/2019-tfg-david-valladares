#!/bin/bash

# ==========================================================================
# Script que actualiza el contenido de la página de portada de la aplicación
# de JdeRobot-Kids-App
# ==========================================================================


Error(){
    printf "\nError."
}

# Update data
git pull origin master

# Update index.html
git add ../jderobot_server/jderobot_kids/templates/jderobot_kids/index.html

# Push to repository
git push origin master