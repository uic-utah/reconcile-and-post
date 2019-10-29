# reconcile-and-post
cli to reconcile and post versions as well as create them

## usage

activate the arcgis python to get access to arcpy

`conda activate arcgispro-py3`

run the tool as a module

`python -m rnp --action=all`
`python -m rnp --action=create`
`python -m rnp --action=delete`
`python -m rnp --action=reconcile`


for me in development with a funky db

`python -m rnp --action=create --sde-folder=C:\dev\uic --admin-schema=dbo --dbo-schema=dbo`
