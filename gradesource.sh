#!/bin/bash

# gradesource.sh
# By Chu Shao
# Jan 13, 2013
# To run, gradesource.sh

# This script was written to automate the process of gradesource uploading. 
# To use, once all the config parameters are hardcoded in, just run gradesource.sh
# 
# There will be a folder called upload. keep ONLY ONE csv file in there and that csv file
# must 
#   A: Be formated as the gradesource CSV input file
#   B: have the assignment ID as its filename. (IE, Assignment # 12345 = 12345.csv)
#      To lookup assignment ID, read the README.


# Static config
login="INSERTLOGINHERE"
courseID="INSERTCOURSEIDHERE"

#Grabs the assignment ID
cd ./upload
assignmentID=`ls | grep .csv | cut -d '.' -f1`

#Checks assignment ID is a number
if ! [[ "$assignmentID" =~ ^[0-9]+$ ]] ; then
    echo "error, CSV file name malformed"
    exit 1
fi

echo 'Your assignment ID  is' $assignmentID
echo 'If incorrect, please hit Control-C'
sleep 5

cp $assignmentID.csv ../temp.csv

cd ../
#Python Magic
python -c 'import gradesourceuploader; gradesourceuploader.updateScoresByEmail("'$login'", "'$courseID'", "'$assignmentID'", "temp.csv", "0")'

rm temp.csv

