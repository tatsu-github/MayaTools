# -*- coding: utf-8 -*-

'''

some scripts for Maya render setup utility
operation confirmed in maya 2018 Update3

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

def getLayerObjectFromLayerName():
    # if not exists layer name object, then renderSetup command return error
    # so using try statement
    layer_name = 'charaA'  # any layer name you want
    try:
        render_layer = renderSetup.instance().getRenderLayer(layer_name)
        return render_layer
    except:
        print 'not exists'
        return False

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
    
def createAbsoluteOverride():
    layer_name = 'charaA'  # any layer name
    collection_name = 'visibilityOff'  # any collection name
    target_collection = renderSetup.instance().getRenderLayer(layer_name).getCollectionByName(collection_name)
    cmds.polyCube(n='dummyObj')
    abs_override = target_collection.createAbsoluteOverride('dummyObjShape', 'primaryVisibility')
    abs_override.setName(layer_name + '_visibleOff')
    abs_override.setAttrValue(0)
    cmds.delete('dummyObj')
    # additional notes："createAbsoluteOverride" method
    # it needs two arg, one is a node name(which has a attribute to override) and the other is attr name.
    # and node name must actually exist in the scene
    # for this reason it needs dummy object
    
def createShaderOverride():
    layer = renderSetup.instance().createRenderLayer('mask')  # create layer
    mask_collection = layer.createCollection('collection_mask')  # create collection
    red_collection = mask_collection.createCollection('collection_red')  # create sub collection
    filterType, customFilter = selector.Filters.getFiltersFor('shadingEngine')  # set sub collection value
    red_collection.getSelector().setPattern('*')
    red_collection.getSelector().setFilterType(filterType)
    red_collection.getSelector().setCustomFilterValue(customFilter)
    red_override = red_collection.createOverride('aiSurfaceShader', 'shaderOverride')  # create shader override
    red_override.setName('override_mask_red')
    mat_name = 'mask_red'  # any material you want to use override
    cmds.connectAttr(mat_name + '.outColor', 'override_mask_red.attrValue', f=True)  # connect attr material to shader override
    
    
    
    
