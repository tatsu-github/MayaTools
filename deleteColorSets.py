from maya import cmds
for i in cmds.ls(sl=True):
    color_sets = cmds.polyColorSet(i, q=True, acs=True)
    if color_sets:
        for color_set in color_sets:
            cmds.polyColorSet(i, delete=True, cs=color_set)       
