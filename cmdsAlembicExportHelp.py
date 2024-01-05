cmds.AbcExport(h=True)
# AbcExport [options]
# Options:
# -h / -help  Print this message.
# 
# -prs / -preRollStartFrame double
# The frame to start scene evaluation at.  This is used to set the
# starting frame for time dependent translations and can be used to evaluate
# run-up that isn't actually translated.
# 
# -duf / -dontSkipUnwrittenFrames
# When evaluating multiple translate jobs, the presence of this flag decides
# whether to evaluate frames between jobs when there is a gap in their frame
# ranges.
# 
# -v / -verbose
# Prints the current frame that is being evaluated.
# 
# -j / -jobArg string REQUIRED
# String which contains flags for writing data to a particular file.
# Multiple jobArgs can be specified.
# 
# -jobArg flags:
# 
# -a / -attr string
# A specific geometric attribute to write out.
# This flag may occur more than once.
# 
# -as / -autoSubd
# If this flag is present and the mesh has crease edges, crease vertices or holes, 
# the mesh (OPolyMesh) would now be written out as an OSubD and crease info will be stored in the Alembic 
# file. Otherwise, creases info won't be preserved in Alembic file 
# unless a custom Boolean attribute SubDivisionMesh has been added to mesh node and its value is true. 
# 
# -atp / -attrPrefix string (default ABC_)
# Prefix filter for determining which geometric attributes to write out.
# This flag may occur more than once.
# 
# -df / -dataFormat string
# The data format to use to write the file.  Can be either HDF or Ogawa.
# The default is Ogawa.
# 
# -ef / -eulerFilter
# If this flag is present, apply Euler filter while sampling rotations.
# 
# -f / -file string REQUIRED
# File location to write the Alembic data.
# 
# -fr / -frameRange double double
# The frame range to write.
# Multiple occurrences of -frameRange are supported within a job. Each
# -frameRange defines a new frame range. -step or -frs will affect the
# current frame range only.
# 
# -frs / -frameRelativeSample double
# frame relative sample that will be written out along the frame range.
# This flag may occur more than once.
# 
# -nn / -noNormals
# If this flag is present normal data for Alembic poly meshes will not be
# written.
# 
# -pr / -preRoll
# If this flag is present, this frame range will not be sampled.
# 
# -ro / -renderableOnly
# If this flag is present non-renderable hierarchy (invisible, or templated)
# will not be written out.
# 
# -rt / -root
# Maya dag path which will be parented to the root of the Alembic file.
# This flag may occur more than once.  If unspecified, it defaults to '|' which
# means the entire scene will be written out.
# 
# -s / -step double (default 1.0)
# The time interval (expressed in frames) at which the frame range is sampled.
# Additional samples around each frame can be specified with -frs.
# 
# -sl / -selection
# If this flag is present, write out all all selected nodes from the active
# selection list that are descendents of the roots specified with -root.
# 
# -sn / -stripNamespaces (optional int)
# If this flag is present all namespaces will be stripped off of the node before
# being written to Alembic.  If an optional int is specified after the flag
# then that many namespaces will be stripped off of the node name. Be careful
# that the new stripped name does not collide with other sibling node names.
# 
# Examples: 
# taco:foo:bar would be written as just bar with -sn
# taco:foo:bar would be written as foo:bar with -sn 1
# 
# -u / -userAttr string
# A specific user attribute to write out.  This flag may occur more than once.
# 
# -uatp / -userAttrPrefix string
# Prefix filter for determining which user attributes to write out.
# This flag may occur more than once.
# 
# -uv / -uvWrite
# If this flag is present, uv data for PolyMesh and SubD shapes will be written to
# the Alembic file.  Only the current uv map is used.
# 
# -uvo / -uvsOnly
# If this flag is present, only uv data for PolyMesh and SubD shapes will be written
# to the Alembic file.  Only the current uv map is used.
# 
# -wcs / -writeColorSets
# Write all color sets on MFnMeshes as color 3 or color 4 indexed geometry 
# parameters with face varying scope.
# 
# -wfs / -writeFaceSets
# Write all Face sets on MFnMeshes.
# 
# -wfg / -wholeFrameGeo
# If this flag is present data for geometry will only be written out on whole
# frames.
# 
# -ws / -worldSpace
# If this flag is present, any root nodes will be stored in world space.
# 
# -wv / -writeVisibility
# If this flag is present, visibility state will be stored in the Alembic
# file.  Otherwise everything written out is treated as visible.
# 
# -wuvs / -writeUVSets
# Write all uv sets on MFnMeshes as vector 2 indexed geometry 
# parameters with face varying scope.
# 
# -mfc / -melPerFrameCallback string
# When each frame (and the static frame) is evaluated the string specified is
# evaluated as a Mel command. See below for special processing rules.
# 
# -mpc / -melPostJobCallback string
# When the translation has finished the string specified is evaluated as a Mel
# command. See below for special processing rules.
# 
# -pfc / -pythonPerFrameCallback string
# When each frame (and the static frame) is evaluated the string specified is
# evaluated as a python command. See below for special processing rules.
# 
# -ppc / -pythonPostJobCallback string
# When the translation has finished the string specified is evaluated as a
# python command. See below for special processing rules.
# 
# Special callback information:
# On the callbacks, special tokens are replaced with other data, these tokens
# and what they are replaced with are as follows:
# 
# #FRAME# replaced with the frame number being evaluated.
# #FRAME# is ignored in the post callbacks.
# 
# #BOUNDS# replaced with a string holding bounding box values in minX minY minZ
# maxX maxY maxZ space seperated order.
# 
# #BOUNDSARRAY# replaced with the bounding box values as above, but in
# array form.
# In Mel: {minX, minY, minZ, maxX, maxY, maxZ}
# In Python: [minX, minY, minZ, maxX, maxY, maxZ]
# 
# Examples:
# 
# AbcExport -j "-root |group|foo -root |test|path|bar -file /tmp/test.abc"
# Writes out everything at foo and below and bar and below to /tmp/test.abc.
# foo and bar are siblings parented to the root of the Alembic scene.
# 
# AbcExport -j "-frameRange 1 5 -step 0.5 -root |group|foo -file /tmp/test.abc"
# Writes out everything at foo and below to /tmp/test.abc sampling at frames:
# 1 1.5 2 2.5 3 3.5 4 4.5 5
# 
# AbcExport -j "-fr 0 10 -frs -0.1 -frs 0.2 -step 5 -file /tmp/test.abc"
# Writes out everything in the scene to /tmp/test.abc sampling at frames:
# -0.1 0.2 4.9 5.2 9.9 10.2
# 
# Note: The difference between your highest and lowest frameRelativeSample can
# not be greater than your step size.
# 
# AbcExport -j "-step 0.25 -frs 0.3 -frs 0.60 -fr 1 5 -root foo -file test.abc"
# 
# Is illegal because the highest and lowest frameRelativeSamples are 0.3 frames
# apart.
# 
# AbcExport -j "-sl -root |group|foo -file /tmp/test.abc"
# Writes out all selected nodes and it's ancestor nodes including up to foo.
# foo will be parented to the root of the Alembic scene.
