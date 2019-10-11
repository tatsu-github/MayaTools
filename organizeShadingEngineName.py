from maya import cmds
def orgSgName():
    mts = cmds.ls(sl=True, mat=True)
    if not mts:
        mts = cmds.ls(mat=True)
    exception_list = ['lambert1', 'particleCloud1', 'shadingGlow1']
    for ex in exception_list:
        if ex in mts:
            mts.remove(ex)
 
    for i in mts:
        sg = cmds.listConnections(i, t='shadingEngine')
        if not sg:
            print '//Result: ', i, 'does not have SG, skipped', '\n'
            continue
        if len(sg) >= 2:
            print '//Result: ', i, 'has multiple SG, skipped', '\n'
            continue
        else:
            sg_name = i + '_SG'
            cmds.rename(sg[0], sg_name)
            print '//Result: renamed', sg[0], 'to', sg_name
