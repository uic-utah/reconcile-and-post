# reconcile-and-post

cli to reconcile and post versions as well as create them

## usage

1. download the project from the link above
1. edit the `config.py` file with the correct values
1. open the command line and change directories to the `src` folder within this project
   - `cd c:\dev\reconcile-and-post\src`
1. activate the arcgis python conda environment to get access to arcpy
   - `conda activate arcgispro-py3`
   
You are now ready to run the tool. The tool is organized as a python module so to run the module you have to pass a special flag to python. `python -m` 

You can use the tool in a few different ways. You can perform different `action`'s. The first action is `create`. This creates the version tree. `delete` does the opposite and deletes all the versions. `reconcile` creates the RNP versions and reconciles them. Finally, there is an `all` action which is the **default** and will perform all the other actions. 

1. run the tool as a module to perform all of the actions.
   - `python -m rnp` or more specifically `python -m rnp --action=all`
   
     This assumes that there is already a version tree available.

1. run the tool to create the versions
   - `python -m rnp --action=create`
1. run the tool to delete the versions
   - `python -m rnp --action=delete`
1. run the tool to reconcile the versions
   - `python -m rnp --action=reconcile`
