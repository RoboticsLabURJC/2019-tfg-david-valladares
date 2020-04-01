#!/bin/bash

change_import(){
    DIR=$1
    DIRNAME_IN=$2

    for OUTPUT in $(ls -d $DIR/*/)
    do
        dirin=$OUTPUT/$DIRNAME_IN

        for FILE in $(ls $dirin/*.ipynb)
        do
	    echo $FILE
            #sed -i 's/PiBot.dameRobot()/PiBot()/g' $dirin/$FILE
            sed -i 's/PiBot.dameRobot()/PiBot()/g' $FILE

            #sed -i 's/import PiBot/from pibot.pibot import PiBot/g' $dirin/$FILE
	    sed -i 's/import\ PiBot/from pibot.pibot import PiBot/g' $FILE

        
        done
        
    done


}

change_websim_name(){
    DIR=$1
    NAME=$2

    #ls -d $DIR/*/
    #printf "\n\n"

    for FOLDER in $(ls -d $DIR/*)
    do
        echo "antes:"
        echo $FOLDER/
        echo "despues:"
        mv $FOLDER/test_websim $FOLDER/sigue_linea_websim
        mv $FOLDER/sigue_linea_websim/test_websim.xml $FOLDER/sigue_linea_websim/sigue_linea_websim.xml
        echo $FOLDER
        printf "\n"
    done
}


change_import users choca_gira_us
change_import users sigue_linea_ir
change_import users sigue_pelota_picam

change_websim_name users sigue_linea_websim
