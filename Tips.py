# print attrs from selected node
for i in maya.cmds.listAttr(http://maya.cmds.ls(sl=True)[0]):print(i)

# get file name without extention
from maya import cmds
file_name = (cmds.file(q=True, sn=True, shn=True)).split('.')[0]
