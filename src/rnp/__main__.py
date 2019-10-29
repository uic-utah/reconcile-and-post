#!/usr/bin/env python
# * coding: utf8 *
'''
rnp.py
A module that helps create uic versions and reconcile and post them
'''

import os
import sys
from optparse import OptionParser

import arcpy
from .models import VersionInfo


def main():
    '''Main entry point for program. Parse arguments and delegate.
    '''

    base_path = 'C:\\GIS\\ArcGISPro\\Projects\\UIC_GDB_Editing\\'
    dbo = 'sde'
    admin_schema = 'UICADMIN'
    log_path = 'C:\\temp'

    parser = OptionParser()
    parser.set_usage('''
Activate the arcgis pro environment
    `activate arcgispro-py3`

Execute the tool as a module
    `python -m rnp --action=all`
    `python -m rnp --action=create`
    `python -m rnp --action=delete`
    `python -m rnp --action=reconcile`''')

    choices = ('all', 'reconcile', 'delete', 'create')
    parser.add_option('-a', '--action', default='all', action='store', choices=choices, help=f'Choose the options from {", ".join(choices)}. Default: all')
    parser.add_option('-c', '--sde-folder', default=base_path, action='store', dest='base_path', help='The path to the folder containing the sde files')
    parser.add_option('-s', '--admin-schema', default=admin_schema, action='store', dest='admin_schema', help='The admin for the database. Default: UICAdmin')
    parser.add_option('-o', '--dbo-schema', default=dbo, action='store', dest='dbo_schema', help='The dbo owner schema. Default: sde')

    (options, _) = parser.parse_args()

    admin = VersionInfo(
        connection=os.path.join(options.base_path, 'Development_DBA_UICADMIN.sde'),
        version_name=f'{options.dbo_schema}.DEFAULT',
        rnp_version_name=None,
        reconciles_into=None,
    )
    surrogate = VersionInfo(
        connection=admin.connection,
        version_name=f'{options.admin_schema}.UIC_Surrogate_Default',
        rnp_version_name=None,
        reconciles_into=admin.version_name,
    )
    qa = VersionInfo(
        connection=admin.connection,
        version_name=f'{options.admin_schema}.UIC_QA',
        rnp_version_name=None,
        reconciles_into=surrogate.version_name,
    )
    brianna = VersionInfo(
        connection=os.path.join(options.base_path, 'Development_DBA_BAriotti.sde'),
        version_name='UIC_BAriotti',
        rnp_version_name='UIC_RnP_BAriotti',
        reconciles_into=qa.version_name,
    )
    candace = VersionInfo(
        connection=os.path.join(options.base_path, 'Development_DBA_CCady.sde'),
        version_name='CCADY.UIC_CCady',
        rnp_version_name='UIC_RnP_CCady',
        reconciles_into=qa.version_name,
    )
    ryan = VersionInfo(
        connection=os.path.join(options.base_path, 'Development_DBA_RParker.sde'),
        version_name='UIC_RParker',
        rnp_version_name='UIC_RnP_RParker',
        reconciles_into=qa.version_name,
    )
    lenora = VersionInfo(
        connection=os.path.join(options.base_path, 'Development_DBA_LenoraS.sde'),
        version_name='UIC_LenoraS',
        rnp_version_name='UIC_RnP_LenoraS',
        reconciles_into=qa.version_name,
    )

    reconcile_versions_order = [
        candace,
        # brianna,
        # ryan,
        # lenora,
        qa,
        surrogate,
    ]

    create_version_order = [
        surrogate,
        qa,
        candace
    ]

    if options.action == 'reconcile' or options.action == 'all':
        reconcile_and_post_versions(reconcile_versions_order, admin.connection, log_path)

    if options.action == 'delete' or options.action == 'all':
        delete_versions(reconcile_versions_order)

    if options.action == 'create' or options.action == 'all':
        create_versions(create_version_order)


def reconcile_and_post_versions(versions, admin_connection, log_path):
    '''method to reconcile and post versions
    versions: array of VersionInfo objects
    admin_connection: the UIC Admin sde connection path
    log_path: the file path to where the reconcile and post log are stored
    '''
    print('reconcile and posting')

    with arcpy.EnvManager(workspace=admin_connection):
        all_versions = [version.name.lower() for version in arcpy.da.ListVersions(admin_connection)]

        required_versions = [version for version in versions if version.version_name.lower() not in all_versions]

        if len(required_versions) > 0:
            print(f'missing the following required versions: {", ".join([version.version_name for version in required_versions])}')

            return

        #: Create RnP versions if they don't exist
        missing_rnp_versions = [version for version in versions if version.rnp_version_name not in all_versions]

        for missing_version in missing_rnp_versions:
            missing_version.create_rnp_version(admin_connection)

        #: Reconcile/Post RnP Versions to QA
        for version_info in versions:
            version_info.reconcile(admin_connection, log_path)

        arcpy.management.ClearWorkspaceCache(admin_connection)

        print('finished')


def delete_versions(versions):
    print(f'deleting {len(versions)} versions')

    for version in versions:
        version.delete()

    print('finished')


def create_versions(versions):
    print(f'creating {len(versions)} versions')

    for version in versions:
        version.create()

    print('finished')


if __name__ == '__main__':
    sys.exit(main())
