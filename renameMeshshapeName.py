# rename mesh shape node name based on parent transform node
from maya import cmds

trans_list = cmds.listRelatives(ad=True, pa=True, type='transform')
for i in trans_list:
    shape = cmds.listRelatives(i, c=True, pa=True, type='mesh')
    if shape and shape[0] != trans + 'Shape':
        try:
            cmds.rename(shape[0], i + 'Shape')
            print 'Result:// renamed ', shape[0], '>>', i+'Shape'
        except:
            pass
