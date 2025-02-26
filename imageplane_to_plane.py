import maya.cmds as cmds

def imageplane_to_polyplane():
    selected = cmds.ls(sl=True, l=True)

    if not selected:
        return

    for i in selected:
        if cmds.objectType(i, isType='transform'):
            img_plane = cmds.listRelatives(i, c=True, type='imagePlane')[0]
        elif cmds.objectType(i, isType='imagePlane'):
            img_plane = i
        else:
            continue

        # Get connected camera
        cameras = cmds.listConnections(img_plane, type='camera')
        if not cameras:
            continue
        
        camera = cameras[0]

        # Get imageplane Bounding Box
        bbox = cmds.exactWorldBoundingBox(img_plane)
        min_x, min_y, min_z, max_x, max_y, max_z = bbox
        width = max_x - min_x
        height = max_y - min_y

        # Create poly plane
        plane = cmds.polyPlane(width=width, height=height, subdivisionsX=1, subdivisionsY=1, name=f'{camera}_{img_plane}_geo')[0]
        cmds.parent(plane, camera, r=True)
        cmds.setAttr(f'{plane}.rotateX', 90)
        img_plane_depth = cmds.getAttr(f'{img_plane}.depth')
        cmds.setAttr(f'{plane}.translateZ', (img_plane_depth*-1))
        cmds.parent(plane, w=True)

        # Texture
        texture_path = cmds.getAttr(f'{img_plane}.imageName')
        if texture_path:
            shader = cmds.shadingNode('lambert', asShader=True, name=f'{img_plane}_shader')
            shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=f'{shader}SG')
            cmds.connectAttr(f'{shader}.outColor', f'{shading_group}.surfaceShader')

            file_node = cmds.shadingNode('file', asTexture=True, name=f'{img_plane}_file')
            cmds.setAttr(f'{file_node}.fileTextureName', texture_path, type='string')
            cmds.connectAttr(f'{file_node}.outColor', f'{shader}.color')
            colorspace = cmds.getAttr(f'{img_plane}.colorSpace')
            cmds.setAttr(f'{file_node}.colorSpace', colorspace, type='string')

            cmds.sets(plane, edit=True, forceElement=shading_group)


def main():
    imageplane_to_polyplane()

main()
