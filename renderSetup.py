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


def getRenderLayerNameList():
    layer_objects = renderSetup.instance().getRenderLayers()  # get layer object list
    layer_list = []
    for i in layer_objects:
        layer_list.append(i.name())  # (object).name() return object name
    return layer_list

    # other way, to get renderSetupLayer node list with maya.cmds
    # it returns the same result as the above function
    # layer_list = cmds.ls(type='renderSetupLayer')
    
def deleteAllRenderSetup():
    render_setup = renderSetup.instance()
    render_layers = render_setup.getRenderLayers()
    for i in render_layers:
        renderLayer.delete(i)

def getRenderLayerObjectFromName():
    # if not exists layer name object, then renderSetup command return error
    # so using try statement
    layer_name = 'charaA'  # any layer name you want
    try:
        render_layer = renderSetup.instance().getRenderLayer(layer_name)
    except:
        print 'not exists'    

def getCollectionObjectsFromLayerObject():
    layer_name = 'charaA' # any name
    render_layer = renderSetup.instance().getRenderLayer(layer_name)
    collections = render_layer.getCollections()
    return collections

def getCollectionsNameFromLayerNames():
    layer_name = 'charaA'  # any name
    render_layer = renderSetup.instance().getRenderLayer(layer_name)
    collection_objects = render_layer.getCollections()
    collection_names = []
    for i in collection_objects:
        collection_names.append(i.name())
    return collection_names

def setMayaObjectToCollection():
    sel = cmds.ls(sl=True)  # it must be list even if it is a single object
    layer_name = 'charaA'  # any layer name
    collection_name = 'visibilityOff'  # any collection name
    target_collection = renderSetup.instance().getRenderLayer(layer_name).getCollectionByName(collection_name)
    target_collection.getSelector().staticSelection.set(sel)  # set maya object to collection
    # additional notes："staticSelection" method
    # set：overwrite value regardless of the current
    # add：add value to current
    # remove：remove value to current

def getCollectionItems():
    layer_name = 'charaA'  # any layer name
    collection_name = 'visibilityOff'  # any collection name
    target_collection = renderSetup.instance().getRenderLayer(layer_name).getCollectionByName(collection_name)
    objects_in_collection = target_collection.getSelector().staticSelection.asList()
    return objects_in_collection
    
    
