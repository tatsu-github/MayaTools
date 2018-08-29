# -*- coding: utf-8 -*-
'''

some scripts for Maya render setup utility

'''
from maya import cmds, mel
import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.app.renderSetup.model.connectionOverride as connectionOverride

def getRenderLayerNameList:
    layer_objects = renderSetup.instance().getRenderLayers()  # get layer object list
    layer_names = []
    for i in layer_objects:
        layer_names.append(i.name())  # (object).name() return object name
    return layer_names

    # other way, to get renderSetupLayer node list with maya.cmds
    # It returns the same result as the above function
    layer_list = cmds.ls(type='renderSetupLayer')
    
