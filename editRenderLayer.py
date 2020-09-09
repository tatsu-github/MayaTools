# override attr
cmds.editRenderLayerAdjustment('aiAOV_Z.enabled')

# override all mtoa aovs
for i in cmds.ls(type='aiAOV'):
  cmds.editRenderLayerAdjustment(i + '.enabled')
