# pre(post) render mel
cmds.setAttr('defaultRenderGlobals.preMel', 'select -cl', type='string')

# pre(post) layer mel
cmds.setAttr('defaultRenderGlobals.preRenderLayerMel', 'select -cl', type='string')

# pre(post) frame mel
cmds.setAttr('defaultRenderGlobals.preRenderMel', 'select -cl', type='string')
