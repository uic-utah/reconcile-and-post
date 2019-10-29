#!/usr/bin/env python
# * coding: utf8 *
'''
models.py
A module that holds data structures
'''
import datetime
import os
import uuid

import arcpy


class VersionInfo():
    '''A model that holds version information for reconciling and posting
    '''

    def __init__(self, connection, fully_qualified_version_name, fully_qualified_rnp_version_name, reconciles_into):
        self.connection = connection
        self.reconciles_into = reconciles_into
        self.fully_qualified_version_name = fully_qualified_version_name
        self.version_name = _trim_schema(fully_qualified_version_name)
        self.fully_qualified_rnp_version_name = fully_qualified_rnp_version_name
        self.rnp_name = None

        if fully_qualified_rnp_version_name:
            self.rnp_name = _trim_schema(fully_qualified_rnp_version_name)

    def reconcile(self, admin_connection, log_path):
        '''reconciles the version into its parent
        '''
        if not self.fully_qualified_rnp_version_name and not self.reconciles_into:
            return

        edit_version = self.fully_qualified_rnp_version_name or self.fully_qualified_version_name

        print(f'  reconcile and posting {edit_version}')

        arcpy.management.ReconcileVersions(
            input_database=admin_connection,
            reconcile_mode='ALL_VERSIONS',
            target_version=self.reconciles_into,
            edit_versions=edit_version,
            acquire_locks='LOCK_ACQUIRED',
            abort_if_conflicts='ABORT_CONFLICTS',
            conflict_definition='BY_OBJECT',
            conflict_resolution='FAVOR_EDIT_VERSION',
            with_post='POST',
            with_delete='#',
            out_log=os.path.join(log_path, f'{str(datetime.date.today())}_{edit_version}_{uuid.uuid4().hex[:5]}.txt')
        )

    def create_rnp_version(self, admin_connection):
        '''creates a version owned by uic admin
        '''
        if not self.fully_qualified_rnp_version_name:
            return

        print(f'  creating rnp version {self.fully_qualified_rnp_version_name}')

        try:
            arcpy.management.CreateVersion(
                in_workspace=admin_connection,
                parent_version=self.fully_qualified_version_name,
                version_name=self.rnp_name,
                access_permission='PROTECTED',
            )
        except:
            print(f'    failed to create {self.fully_qualified_rnp_version_name} from {self.fully_qualified_version_name}')

    def delete(self, admin_connection):
        '''a method to delete versions and rnp versions
        '''
        if self.fully_qualified_rnp_version_name:
            print(f'  deleting {self.fully_qualified_rnp_version_name} version')

            try:
                arcpy.management.DeleteVersion(
                    in_workspace=admin_connection,
                    version_name=self.rnp_name,
                )
            except Exception as ex:
                print(f'    could not delete. does this version exist? {ex}')

        if self.fully_qualified_version_name:
            print(f'  deleting {self.fully_qualified_version_name} version')

            try:
                arcpy.management.DeleteVersion(
                    in_workspace=self.connection,
                    version_name=self.version_name,
                )
            except Exception as ex:
                print(f'could not delete. does this version exist? {ex}')

    def create(self):
        '''a method to create versions
        '''
        print(f'  creating {self.fully_qualified_version_name} from {self.reconciles_into}')

        arcpy.management.CreateVersion(
            in_workspace=self.connection,
            parent_version=self.reconciles_into,
            version_name=self.version_name,
            access_permission='PROTECTED'
        )

    def __repr__(self):
        return self.fully_qualified_version_name

def _trim_schema(fully_qualified_version_name):
    '''a method to trim the schema from a version name as arcpy barfs
    '''
    name = fully_qualified_version_name
    parts = fully_qualified_version_name.split('.')
    part_count = len(parts)

    if part_count > 1:
        name = parts[part_count - 1]

    return name
