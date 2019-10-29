#!/usr/bin/env python
# * coding: utf8 *
'''
config.py
A module that holds items that may change
'''


VERSION = '1.0.0'

BASE_PATH = 'C:\\GIS\\ArcGISPro\\Projects\\UIC_GDB_Editing\\'
LOG_PATH = 'C:\\temp'

DBO = 'sde'
ADMIN_SCHEMA = 'UICADMIN'

CONNECTIONS = {
    'uic_admin': 'Development_DBA_UICADMIN.sde',
    'surrogate': 'Development_DBA_UICADMIN.sde',
    'quality_assurance': 'Development_DBA_UICADMIN.sde',
    'brianna': 'Development_DBA_BAriotti.sde',
    'candace': 'Development_DBA_CCady.sde',
    'ryan': 'Development_DBA_RParker.sde',
    'lenora': 'Development_DBA_LenoraS.sde'
}
