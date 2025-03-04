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

from . import config
from .models import VersionInfo


def main():
    '''Main entry point for program. Parse arguments and delegate.
    '''

    print(f'Reconcile and Post version: {config.VERSION}{os.linesep}')

    parser = OptionParser()
    parser.set_usage(
        '''
Activate the arcgis pro environment
    `activate arcgispro-py3`

Execute the tool as a module
    `python -m rnp --action=all`
    `python -m rnp --action=create`
    `python -m rnp --action=delete`
    `python -m rnp --action=reconcile`'''
    )

    choices = ('all', 'reconcile', 'delete', 'create')
    parser.add_option('-a', '--action', default='all', action='store', choices=choices, help=f'Choose the options from {", ".join(choices)}. Default: all')
    parser.add_option('-c', '--sde-folder', default=config.BASE_PATH, action='store', dest='base_path', help='The path to the folder containing the sde files')
    parser.add_option('-s', '--admin-schema', default=config.ADMIN_SCHEMA, action='store', dest='admin_schema', help='The admin for the database. Default: UICAdmin')
    parser.add_option('-o', '--dbo-schema', default=config.DBO, action='store', dest='dbo_schema', help='The dbo owner schema. Default: sde')

    (options, _) = parser.parse_args()

    admin = VersionInfo(
        connection=os.path.join(options.base_path, config.CONNECTIONS['uic_admin']),
        fully_qualified_version_name=f'{options.dbo_schema}.DEFAULT',
        fully_qualified_rnp_version_name=None,
        reconciles_into=None,
    )
    surrogate = VersionInfo(
        connection=admin.connection,
        fully_qualified_version_name=f'{options.admin_schema}.UIC_Surrogate_Default',
        fully_qualified_rnp_version_name=None,
        reconciles_into=admin.fully_qualified_version_name,
    )
    quality_assurance = VersionInfo(
        connection=admin.connection,
        fully_qualified_version_name=f'{options.admin_schema}.UIC_QA',
        fully_qualified_rnp_version_name=None,
        reconciles_into=surrogate.fully_qualified_version_name,
    )
    ryan = VersionInfo(
        connection=os.path.join(options.base_path, config.CONNECTIONS['ryan']),
        fully_qualified_version_name='RPARKER.UIC_RParker',
        fully_qualified_rnp_version_name=f'{options.admin_schema}.UIC_RnP_RParker',
        reconciles_into=quality_assurance.fully_qualified_version_name,
    )
    mark = VersionInfo(
        connection=os.path.join(options.base_path, config.CONNECTIONS['mark']),
        fully_qualified_version_name='MSTANGER.UIC_MStanger',
        fully_qualified_rnp_version_name=f'{options.admin_schema}.UIC_RnP_MStanger',
        reconciles_into=quality_assurance.fully_qualified_version_name,
    )
    porter = VersionInfo(
        connection=os.path.join(options.base_path, config.CONNECTIONS['porter']),
        fully_qualified_version_name='PHENZE.UIC_PHenze',
        fully_qualified_rnp_version_name=f'{options.admin_schema}.UIC_RnP_PHenze',
        reconciles_into=quality_assurance.fully_qualified_version_name,
    )

    reconcile_versions_order = [
        porter,
        ryan,
        mark,
        quality_assurance,
        surrogate,
    ]

    create_version_order = [
        surrogate,
        quality_assurance,
        ryan,
        mark,
        porter,
    ]
    
    if options.action == 'reconcile' or options.action == 'all':
        reconcile_and_post_versions(reconcile_versions_order, admin.connection, config.LOG_PATH)

    if options.action == 'delete' or options.action == 'all':
        delete_versions(reconcile_versions_order, admin.connection)

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

        required_versions = [version for version in versions if version.fully_qualified_version_name.lower() not in all_versions]

        if len(required_versions) > 0:
            print(f'missing the following required versions: {", ".join([version.fully_qualified_version_name for version in required_versions])}')

            return

        #: Create RnP versions if they don't exist
        missing_rnp_versions = [version for version in versions if version.fully_qualified_rnp_version_name not in all_versions]

        for missing_version in missing_rnp_versions:
            missing_version.create_rnp_version(admin_connection)

        #: Reconcile/Post RnP Versions to QA
        for version_info in versions:
            version_info.reconcile(admin_connection, log_path)

        arcpy.management.ClearWorkspaceCache(admin_connection)

        print(f'finished{os.linesep}')


def delete_versions(versions, admin_connection):
    print(f'trying to delete {sum(version.version_count for version in versions)} versions. some may not exist')

    with arcpy.EnvManager(workspace=admin_connection):
        print('testing if delete can be run')

        has_rnp = len([version for version in arcpy.da.ListVersions(admin_connection) if 'rnp' in version.name.lower()]) > 0

        if not has_rnp:
            print('Reconcile and Post versions have not been created. Exiting')

            sys.exit(-1)

    print('checks pass, deleting versions')

    for version in versions:
        version.delete(admin_connection)

    print(f'finished{os.linesep}')


def create_versions(versions):
    print(f'creating {len(versions)} versions')

    for version in versions:
        version.create()

    print(f'finished{os.linesep}')


if __name__ == '__main__':
    sys.exit(main())
