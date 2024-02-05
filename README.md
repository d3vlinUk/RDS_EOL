# RDS_EOL
Used to run checks in a Lambda to determine if a RDS is soon to reach it's end of life

#Todo

* Read existing dates if they exist, and append into them
* Remove non allowed characters from the version (eg 11.22* should be 11.22git add)
