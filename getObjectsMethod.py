from maya import cmds

# get top node info
sel = cmds.ls(sl=True, type='transform')

# get mesh info
meshes = cmds.listRelatives(sel[0], ad=True, type='mesh')
print meshes

# get shading engine
sgs_tmp = cmds.listConnections(meshes, t='shadingEngine')
sgs = list(set(sgs_tmp))
print sgs

# get spcecific material
mts = cmds.listConnections(sgs, t='aiStandardSurface')
print mts

# get file node
files = cmds.listConnections(mts, t='file')
print files

# get connection src
src = cmds.connectionInfo(plug_name, sfd=True)
