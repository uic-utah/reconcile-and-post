# reconcile-and-post

cli to reconcile and post versions as well as create them

## usage

### one time items (or when updating versions)

1. download the project from the link above
1. edit the `config.py` file with the correct values

### easy path

1. browse to `reconcile-and-post-master\src`
1. click on the `*.bat` file for what you would like to do

### command line usage

1. open the command line and change directories to the `src` folder within this project
   - `cd c:\dev\reconcile-and-post\src`
1. activate the arcgis python conda environment to get access to arcpy
   - `"C:\Program Files\ArcGIS\Pro\bin\Python\Scripts\proenv.bat"`
   - or `activate arcgispro-py3`

You are now ready to run the tool. The tool is organized as a python module so to run the module you have to pass a special flag to python. `python -m`

You can use the tool in a few different ways by passing the `action` flag. The first action is `create`. This creates the version tree. `delete` does the opposite and deletes all the versions. `reconcile` creates the RNP versions and reconciles them. Finally, there is an `all` action which is the **default** and will perform all the other actions.

1. run the tool as a module to perform all of the actions.
   - `python -m rnp` or more specifically `python -m rnp --action=all`

     This assumes that there is already a version tree available.

1. run the tool to create the versions
   - `python -m rnp --action=create`
1. run the tool to delete the versions
   - `python -m rnp --action=delete`
1. run the tool to reconcile the versions
   - `python -m rnp --action=reconcile`

#### troubleshooting

if your terminal starts in another drive letter than where you downloaded type the drive letter only to switch. for example `c:`

if you see `No module named rnp` then you need to `cd` to the `src` folder within the project you downloaded. For example `cd c:\dev\reconcile-and-post\src`.
