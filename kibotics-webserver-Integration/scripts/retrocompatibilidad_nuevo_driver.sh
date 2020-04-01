#!/bin/bash

change_import(){
    DIR=$1
    DIRNAME_IN=$2

    for FOLDER in $(ls -d $DIR/*)
    do
        USER_FOLDER=$FOLDER/$DIRNAME_IN

        for EXERCISE in $(ls $USER_FOLDER/*.ipynb)
    	do
            printf "\n111111111111111111111\n"
            printf "Exercise: "
            printf $EXERCISE
            printf "\n22222222222222222222222222\n"
        	sed -i 's/PiBot.dameRobot()/PiBot()/g' $EXERCISE
        	sed -i 's/import PiBot/from piBot import PiBot/g' $EXERCISE
    	done
        printf "===========\n\n\n\n"
    done


}


change_import users choca_gira_us
change_import users sigue_linea_ir
change_import users sigue_pelota_picam