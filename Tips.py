# print attrs from selected node
for i in maya.cmds.listAttr(cmds.ls(sl=True)[0]):print(i)

# get file name without extention
from maya import cmds
file_name = (cmds.file(q=True, sn=True, shn=True)).split('.')[0]

# change working units to Centimeter
cmds.currentUnit(linear='cm')

# print Maya plug-in path
from maya import cmds, mel
path = mel.eval('getenv "MAYA_PLUG_IN_PATH"')
path_list = path.split(':')
for i in path_list:
    print i
    
# get module path
import maya.app.renderSetup.model.collection as collection
print collection.__file__

# get textrue path from selected file node
sel = cmds.ls(sl=True)[0]
print cmds.getAttr(sel+'.fileTextureName')

# set file node colorspace
cmds.setAttr(filenode + '.colorSpace', 'sRGB', type='string')

# create disc to selected objects
for i in cmds.ls(sl=True, type='transform'):
    disc = cmds.polyDisc(sides=3, subdivisionMode=4, subdivisions=3, radius=1)
    disc = cmds.rename(disc, 'disc_' + i)
    const = cmds.parentConstraint(i, disc, weight=1)
    cmds.delete(const)

# Default View LUT
cmds.colorManagementPrefs(e = True,  viewTransformName = "sRGB (ACES)" )
    
# add color management file rules
cmds.colorManagementPrefs(e=True, ocioRulesEnabled=False)
proj = 'myProject'
srgb = ['jpg', 'jpeg', 'tif', 'png']
raw = ['exr']
for i in srgb + raw:
    rule_name = proj + '_' + i
    try:
        if cmds.colorManagementFileRules(rule_name, query=True, pattern=True):
            cmds.colorManagementFileRules(remove=rule_name)
    except RuntimeError:
        pass
    if i in srgb:
        cmds.colorManagementFileRules(add=rule_name, pattern='*', extension=i, colorSpace='Utility - sRGB - Texture')
    else:
        cmds.colorManagementFileRules(add=rule_name, pattern='*', extension=i, colorSpace='Utility - Raw')
