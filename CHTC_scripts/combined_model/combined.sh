#!/bin/bash


#replace ve job exit if any command returns with non-zero exit status (aka failure)
set -e


# TODO: MANAGE THE CONDA ENVIRONMENT
# replace env-name on the right hand side of this line with the name of your conda environment
ENVNAME=px
# if you need the environment directory to be named something other than the environment name, change this line
ENVDIR=$ENVNAME

# these lines handle setting up the environment; you shouldn't have to modify them
export PATH
mkdir $ENVDIR
#tar -xzf $ENVNAME.tar.gz -C $ENVDIR
#. $ENVDIR/bin/activate

# END MANAGE CONDA ENVIRONMENT

# TODO: MANAGE LARGE INPUT FILES and submit
# First, copy the compressed tar file from /staging into the working directory,
#  and un-tar it to reveal your large input file(s) or directories:
# cp /staging/groups/schrodi_group/ProjectX_2021/toy_model/toy_fin.tar.gz ./
cp /staging/groups/schrodi_group/ProjectX_2021/F2/combined/combined_raw.tar.gz ./
cp /staging/groups/schrodi_group/ProjectX_2021/toy_model/$ENVDIR.tar.gz ./
tar -xzvf combined_raw.tar.gz
tar -xzvf $ENVNAME.tar.gz
tar -xzf $ENVNAME.tar.gz -C $ENVDIR
. $ENVDIR/bin/activate


# Run the Python script, the 1,2, ... are the arguments from the .sub file
python3 regularized_toy_script.py  $1 $2 

# TODO: Before the script exits, make sure to remove the file(s) from the working directory
rm combined_raw.tar.gz ./combined/* 
rm -rf ./toy
rm $ENVNAME.tar.gz
rm -rf ./$ENVDIR

# END MANGE LARGE INPUT FILES

# MANAGE LARGE OUTPUT FILES (if needed- dont modify but use as example above- for saving model weights)
# modify this line to run your desired Python script nd move large files to staging so they're not copied to the submit server:
#tar -czvf large_stdout.tar.gz large_std.out
#cp large_stdout.tar.gz /staging/username/subdirectory
# rm large_std.out large_stdout.tar.gzand any other work you need to do
# python3 hello.py
# END MANAGE LARGE OUTPUT FILES


END
