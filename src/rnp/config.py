#!/usr/bin/env python
# * coding: utf8 *
'''
config.py
A module that holds items that may change
'''


#: path to the connection sde files
BASE_PATH = 'C:\\GIS\\ArcGISPro\\Projects\\UIC_GDB_Editing\\'

#: sde connection names for the users
CONNECTIONS = {
    'uic_admin': 'Development_DBA_UICADMIN.sde',
    'surrogate': 'Development_DBA_UICADMIN.sde',
    'quality_assurance': 'Development_DBA_UICADMIN.sde',
    'ryan': 'Development_DBA_RParker.sde',
    'mark': 'Development_DBA_MStanger.sde',
    'porter': 'Development_DBA_PHenze.sde'
}

#: path where reconcile logs wil be written
LOG_PATH = 'C:\\temp'

#: you can mostly ignore these
VERSION = '1.2.0'
DBO = 'sde'
ADMIN_SCHEMA = 'UICADMIN'
