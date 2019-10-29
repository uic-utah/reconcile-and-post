#!/usr/bin/env python
# * coding: utf8 *
'''
models.py
A module that holds data structures
'''
import datetime
import os

import arcpy


class VersionInfo():
    '''A model that holds version information for reconciling and posting
    '''

    def __init__(self, connection, version_name, rnp_version_name, reconciles_into):
        self.connection = connection
        self.reconciles_into = reconciles_into
        self.version_name = version_name
        self.trimmed_version = _trim_schema(version_name)
        self.rnp_version_name = rnp_version_name

        if rnp_version_name:
            self.trimmed_rnp = _trim_schema(rnp_version_name)

    def reconcile(self, admin_connection, log_path):
        if not self.rnp_version_name:
            return

        print(f'reconcile and posting {self.rnp_version_name}')

        arcpy.management.ReconcileVersions(
            input_database=admin_connection,
            reconcile_mode='ALL_VERSIONS',
            target_version=self.reconciles_into,
            edit_versions=self.rnp_version_name,
            acquire_locks='LOCK_ACQUIRED',
            abort_if_conflicts='ABORT_CONFLICTS',
            conflict_definition='BY_OBJECT',
            conflict_resolution='FAVOR_EDIT_VERSION',
            with_post='POST',
            with_delete='#',
            out_log=os.path.join(log_path, f'{self.rnp_version_name}_{str(datetime.date.today())}.txt')
        )

    def create_rnp_version(self, admin_connection):
        if not self.rnp_version_name:
            return

        print(f'creating rnp version {self.rnp_version_name}')

        arcpy.management.CreateVersion(
            in_workspace=admin_connection,
            parent_version=self.trimmed_version,
            version_name=self.trimmed_rmp,
            access_permission='PROTECTED')

    def delete(self):
        '''a method to delete versions and rnp versions
        '''
        if self.version_name:
            print(f'deleting {self.version_name} version')

            try:
                arcpy.management.DeleteVersion(self.connection, self.version_name)
            except:
                print(f'could not delete. does this version exist?')

        if self.rnp_version_name:
            print(f'deleting {self.rnp_version_name} version')

            try:
                arcpy.management.DeleteVersion(self.connection, self.rnp_version_name)
            except:
                print(f'could not delete. does this version exist?')

    def create(self):
        '''a method to create versions
        '''
        print(f'creating {self.version_name} from {self.reconciles_into}')

        arcpy.management.CreateVersion(
            in_workspace=self.connection,
            parent_version=self.reconciles_into,
            version_name=self.trimmed_version,
            access_permission='PROTECTED'
        )

    def __repr__(self):
        return self.version_name

def _trim_schema(version_name):
    '''a method to trim the schema from a version name as arcpy barfs
    '''
    name = version_name
    parts = version_name.split('.')
    part_count = len(parts)

    if part_count > 1:
        name = parts[part_count - 1]

    return name
