from maya import cmds

def get_bbox_xyz():
    bbox = cmds.exactWorldBoundingBox(cmds.ls(sl=True, type='transform')[0])
    xmin, ymin, zmin, xmax, ymax, zmax = bbox[0], bbox[1], bbox[2], bbox[3], bbox[4], bbox[5]
    width = xmax - xmin
    height = ymax - ymin
    depth = zmax - zmin
    return width, height, depth
  
