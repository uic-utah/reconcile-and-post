
#---Last Revised: April 24, 2019---

import arcpy
import sys
import datetime, time

from arcpy import env

#---The Connection Files---
uicAdmin = r'C:\GIS\ArcGISPro\Projects\UIC_GDB_Editing\Development_DBA_UICADMIN.sde'
uicBAriotti = r'C:\GIS\ArcGISPro\Projects\UIC_GDB_Editing\Development_DBA_BAriotti.sde'
uicCCady = r'C:\GIS\ArcGISPro\Projects\UIC_GDB_Editing\Development_DBA_CCady.sde'
uicRParker = r'C:\GIS\ArcGISPro\Projects\UIC_GDB_Editing\Development_DBA_RParker.sde'
uicLenoraS = r'C:\GIS\ArcGISPro\Projects\UIC_GDB_Editing\Development_DBA_LenoraS.sde'

#---The Versions---
default = 'sde.DEFAULT'
uicSurrogate = 'UICADMIN.UIC_Surrogate_Default'
uicQA = 'UICADMIN.UIC_QA'
cCady = 'CCADY.UIC_CCady'
bAriotti = 'BARIOTTI.UIC_BAriotti'
rParker = 'RPARKER.UIC_RParker'
lenoras = 'LENORAS.UIC_LenoraS'

#---The RnP Versions---
cCady_rnp = 'UICADMIN.UIC_RnP_CCady'
bAriotti_rnp = 'UICADMIN.UIC_RnP_BAriotti'
rParker_rnp = 'UICADMIN.UIC_RnP_RParker'
lenoras_rnp = 'UICADMIN.UIC_RnP_LenoraS'

#---Reconcile and Post---
def RandP_Versions():

    arcpy.env.workspace = uicAdmin

    #---Check for necessary versions
    versionLst = []
    sourceVersions = [default, uicSurrogate, uicQA, cCady, bAriotti, rParker, lenoras]
    log = r'C:\\'

    for version in arcpy.da.ListVersions(uicAdmin):
        versionLst.append(version.name)
    for sVersion in sourceVersions:
        if sVersion not in versionLst:
            print 'Insufficient Versions Exist'
            sys.exit()
        else:
            continue


    #---Create RnP versions if they don't exist
    if cCady_rnp not in versionLst:
        try:
            arcpy.CreateVersion_management(uicAdmin, cCady, 'UIC_RnP_CCady', 'PRIVATE')
        except:
            print 'Could not create ' + cCady_rnp
            sys.exit()

    if bAriotti_rnp not in versionLst:
        try:
            arcpy.CreateVersion_management(uicAdmin, bAriotti, 'UIC_RnP_BAriotti', 'PRIVATE')
        except:
            print 'Could not create ' + bAriotti_rnp
            sys.exit()

    if rParker_rnp not in versionLst:
        try:
            arcpy.CreateVersion_management(uicAdmin, rParker, 'UIC_RnP_RParker', 'PRIVATE')
        except:
            print 'Could not create ' + rParker_rnp
            sys.exit()

    if lenoras_rnp not in versionLst:
        try:
            arcpy.CreateVersion_management(uicAdmin, lenoras, 'UIC_RnP_LenoraS', 'PRIVATE')
        except:
            print 'Could not create ' + lenoras_rnp
            sys.exit()

    today = str(datetime.date.today())


    #---Reconcile/Post RnP Versions to QA
    print 'Reconcile and Post ' + cCady_rnp
    arcpy.ReconcileVersions_management(uicAdmin, 'ALL_VERSIONS', uicQA, cCady_rnp, 'LOCK_ACQUIRED', 'ABORT_CONFLICTS', \
                                       'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', '#', log + cCady_rnp + '_RnP' + today + '.txt')

    print 'Reconcile and Post ' + bAriotti_rnp
    arcpy.ReconcileVersions_management(uicAdmin, 'ALL_VERSIONS', uicQA, bAriotti_rnp, 'LOCK_ACQUIRED', 'ABORT_CONFLICTS', \
                                       'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', '#', log + bAriotti_rnp + '_RnP' + today + '.txt')


    print 'Reconcile and Post ' + rParker_rnp
    arcpy.ReconcileVersions_management(uicAdmin, 'ALL_VERSIONS', uicQA, rParker_rnp, 'LOCK_ACQUIRED', 'ABORT_CONFLICTS', \
                                       'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', '#', log + rParker_rnp + '_RnP' + today + '.txt')


    print 'Reconcile and Post ' + lenoras_rnp
    arcpy.ReconcileVersions_management(uicAdmin, 'ALL_VERSIONS', uicQA, lenoras_rnp, 'LOCK_ACQUIRED', 'ABORT_CONFLICTS', \
                                       'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', '#', log + lenoras_rnp + '_RnP' + today + '.txt')


    #---Reconcile/Post QA Version to Surrogate
    print 'Reconcile and Post ' + uicQA
    arcpy.ReconcileVersions_management(uicAdmin, 'ALL_VERSIONS', uicSurrogate, uicQA, 'LOCK_ACQUIRED', 'ABORT_CONFLICTS', \
                                       'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', '#', log + uicQA + '_RnP' + today + '.txt')

    #---Reconcile/Post Surrogate to Default
    print 'Reconcile and Post ' + uicSurrogate
    arcpy.ReconcileVersions_management(uicAdmin, 'ALL_VERSIONS', default, uicSurrogate, 'LOCK_ACQUIRED', 'ABORT_CONFLICTS', \
                                       'BY_OBJECT', 'FAVOR_EDIT_VERSION', 'POST', '#', log + uicSurrogate + '_RnP' + today + '.txt')

    arcpy.ClearWorkspaceCache_management(uicAdmin)

    print ''


#---Delete old versions---
def deleteVersions():

    arcpy.env.workspace = uicAdmin

    childList = [bAriotti_rnp, cCady_rnp, rParker_rnp, lenoras_rnp, bAriotti, cCady, rParker, lenoras, uicQA, uicSurrogate]
    ownerDict = {'UICADMIN':uicAdmin, 'CCADY':uicCCady, 'BARIOTTI':uicBAriotti, 'RPARKER':uicRParker, 'LENORAS':uicLenoraS}

    for deleteChild in childList:
        sdeConnection = ownerDict[deleteChild.split('.')[0]]
        versionName = deleteChild.split('.')[1]

        arcpy.DeleteVersion_management(sdeConnection, versionName)
        print 'DELETED ' + deleteChild

    print ''


#---Re-Create Versions---
def createVersions():

    arcpy.CreateVersion_management(uicAdmin, default, uicSurrogate.split('.')[1], 'PROTECTED')
    print 'Created ' + uicSurrogate
    arcpy.CreateVersion_management(uicAdmin, uicSurrogate, uicQA.split('.')[1], 'PROTECTED')
    print 'Created ' + uicQA
    arcpy.CreateVersion_management(uicCCady, uicQA, cCady.split('.')[1], 'PROTECTED')
    print 'Created ' + cCady
    arcpy.CreateVersion_management(uicBAriotti, uicQA, bAriotti.split('.')[1], 'PROTECTED')
    print 'Created ' + bAriotti
    arcpy.CreateVersion_management(uicRParker, uicQA, rParker.split('.')[1], 'PROTECTED')
    print 'Created ' + rParker
    arcpy.CreateVersion_management(uicLenoraS, uicQA, lenoras.split('.')[1], 'PROTECTED')
    print 'Created ' + lenoras

#---Function Calls---
RandP_Versions()
deleteVersions()
createVersions()

