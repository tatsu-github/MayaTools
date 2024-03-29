# -*- coding: utf-8 -*-
'''

scripts for Maya render setup utility
operation confirmed in maya 2018 Update3 and MtoA 3.1.0

'''

from maya import cmds, mel
import maya.app.renderSetup.model.override as override
import maya.app.renderSetup.model.selector as selector
import maya.app.renderSetup.model.collection as collection
import maya.app.renderSetup.model.renderLayer as renderLayer
import maya.app.renderSetup.model.renderSetup as renderSetup
import maya.app.renderSetup.model.connectionOverride as connectionOverride


# Get render layer name list
def getRenderLayerNameList():
    layer_objects = renderSetup.instance().getRenderLayers()  # get layer object list
    layer_list = []
    for i in layer_objects:
        layer_list.append(i.name())  # (object).name() return object name
    return layer_list

    # other way, to get renderSetupLayer node list with maya.cmds
    # it returns the same result as the above function
    # layer_list = cmds.ls(type='renderSetupLayer')

# Switch to current layer
def switchToCurrentLayer():
    layer_objects = renderSetup.instance().getRenderLayers()
    renderSetup.instance().switchToLayer(layer_objects[0])
    
# Delete all render layer
def deleteAllRenderLayer():
    render_layers = renderSetup.instance().getRenderLayers()
    for i in render_layers:
        renderLayer.delete(i)

# Get render layer object from specific layer name
def getLayerObjectFromLayerName():
    # if the specified layer does not exist, renderSetup returns error
    # so using try statement
    layer_name = 'charaA'  # any layer name
    try:
        render_layer = renderSetup.instance().getRenderLayer(layer_name)
        return render_layer
    except:
        print 'not exists'
        return False

# Get collection objects from specific layer name
def getCollectionObjectsFromLayerObject():
    layer_name = 'charaA' # any name
    render_layer = renderSetup.instance().getRenderLayer(layer_name)
    collections = render_layer.getCollections()
    return collections

# Get collections name from specific layer name
def getCollectionsNameFromLayerName():
    layer_name = 'charaA'  # any name
    render_layer = renderSetup.instance().getRenderLayer(layer_name)
    collection_objects = render_layer.getCollections()
    collection_names = []
    for i in collection_objects:
        collection_names.append(i.name())
    return collection_names

# Set maya object to collection
def setMayaObjectToCollection():
    sel = cmds.ls(sl=True)  # it must be list even if it is a single object
    layer_name = 'charaA'  # any layer name
    collection_name = 'visibilityOff'  # any collection name
    target_collection = renderSetup.instance().getRenderLayer(layer_name).getCollectionByName(collection_name)
    target_collection.getSelector().staticSelection.set(sel)  # set maya object to collection
    # additional notes："staticSelection" method
    # set：overwrite value regardless of the current
    # add：add value to current
    # remove：remove value from current

# Get objects included in specific collection
def getCollectionItems():
    layer_name = 'charaA'  # any layer name
    collection_name = 'visibilityOff'  # any collection name
    target_collection = renderSetup.instance().getRenderLayer(layer_name).getCollectionByName(collection_name)
    objects_in_collection = target_collection.getSelector().staticSelection.asList()
    return objects_in_collection

# Create absolute override below specific collection
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

# Create shader override    
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

# Create AOVs override    
def createAovOverride():
    layer_name = 'charaA'  # any layer
    layer = renderSetup.instance().getRenderLayer(layer_name)  # any layer
    aov_collection = layer.aovCollectionInstance()
    aov_name = 'diffuse_albedo'  # any AOV
    sub_colle = collection.create(layer_name+'_'+aov_name, collection.AOVChildCollection.kTypeId, aovName=aov_name)
    aov_collection.appendChild(sub_colle)
    override = sub_colle.createAbsoluteOverride('aiAOV_'+aov_name, 'enabled')  #(aov name, attr name)
    override.setAttrValue(0)  # override value
    override.setName(layer_name+'_'+aov_name)

# Create render setting override
def createRenderSetttingoverride():
    layer_name = 'charaA'  # any layer
    render_layer = renderSetup.instance().createRenderLayer(layer_name) 
    set_colle = render_layer.renderSettingsCollectionInstance()
    attr_name = 'AASamples'
    override = set_colle.createAbsoluteOverride('defaultArnoldRenderOptions', attr_name)
    override.setAttrValue(5)
    override.setName(layer_name+'_'+attr_name)
    
    
    
    
    
