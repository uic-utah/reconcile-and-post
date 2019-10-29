# reconcile-and-post

cli to reconcile and post versions as well as create them

## usage

1. download the project from the link above
1. edit the `config.py` file with the correct values
1. open the command line and change directories to the `src` folder within this project
   - `cd c:\dev\reconcile-and-post\src`
1. activate the arcgis python conda environment to get access to arcpy
   - `conda activate arcgispro-py3`
1. run the tool as a module to perform all of the actions. Reconcile versions, delete the versions, create the version tree
   - `python -m rnp --action=all`
1. run the tool to create the versions
   - `python -m rnp --action=create`
1. run the tool to delete the versions
   - `python -m rnp --action=delete`
1. run the tool to reconcile the versions
   - `python -m rnp --action=reconcile`
