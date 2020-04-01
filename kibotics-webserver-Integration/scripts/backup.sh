#!/bin/bash

# --------------------------------------------------------------------------------------------------------
# Backup script to JdeRobotAcademy and JdeRobotKids platforms. Clear backups with 15 or more days in disk.
# ---------------------------------------- Francisco Perez & Ignacio Arranz ------------------------------

BACKUP_DIR=/home/jderobot/Documents/KiboticsBackups
KEEP_BACKUPS_FOR=15 #days
PASS=JdeRobotP0str3

function run_backup(){

    mysqldump -uroot -p$PASS --opt kibotics > /var/backups/Kibotics/$(date +%Y_%m_%d_%H_%M)_backup_kibotics.sql;
    mysqldump -uroot -p$PASS --opt kibotics > /home/jderobot/Documents/KiboticsBackups/$(date +%Y_%m_%d_%H_%M)_backup_kibotics.sql
    #mysqldump --defaults-extra-file=/etc/mysqldump.cnf --opt db_JdeRobotKidsApp > /etc/mysql/backups/JdeRobotKids/$(date +%Y_%m_%d_%H_%M)_bac$

}

function delete_old_backups(){

  echo "Deleting $BACKUP_DIR/*.sql older than $KEEP_BACKUPS_FOR days"
  find $BACKUP_DIR -type f -name "*.sql" -mtime +$KEEP_BACKUPS_FOR -exec rm {} \;
  find $BACKUP_DIR -type f -name "*.tar" -mtime +$KEEP_BACKUPS_FOR -exec rm {} \;

}


#=========================
#RUN SCRIPT
#==========================
delete_old_backups
run_backup

