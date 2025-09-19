import os
import sys
import maya.OpenMayaMPx as OpenMayaMPx
import glTFExport
import traceback

PLUGIN_NAME = "glTF Export"
PLUGIN_COMPANY = "Matias Codesal"
FILE_EXT = 'glb'

# Node definition
class GLTFTranslator(OpenMayaMPx.MPxFileTranslator):
    def __init__(self):
        OpenMayaMPx.MPxFileTranslator.__init__(self)
        self.kwargs = {}
    def haveWriteMethod(self):
        return True
    def haveReadMethod(self):
        return False
    def filter(self):
        return "*.glb;*.gltf"
    def defaultExtension(self):
        return FILE_EXT
    def writer( self, file_obj, opt_string, access_mode ): 
        fullName = file_obj.fullName()
        try:
            if access_mode == OpenMayaMPx.MPxFileTranslator.kExportAccessMode:
                self._parse_args(opt_string)
                self.kwargs['file_path'] = fullName
                self.kwargs['selected_nodes'] = False
                glTFExport.export(**self.kwargs)
            elif access_mode == OpenMayaMPx.MPxFileTranslator.kExportActiveAccessMode:
                self._parse_args(opt_string)
                self.kwargs['file_path'] = fullName
                self.kwargs['selected_nodes'] = True
                glTFExport.export(**self.kwargs)
        except Exception as e:
            sys.stderr.write("Failed to write file information: {}\n".format(e))
            traceback.print_exc(file=sys.stderr)
            raise
    
    def _parse_args(self, opt_string):
        # TODO: why does opt_string have default values and current values in it?
        opts = opt_string.split(';')
        for opt in opts:
            if opt:
                key, value = opt.split('=')
                if key == 'resFormat':
                    if value in ['bin', 'source', 'embedded']:
                        self.kwargs['resource_format'] = value
                    else:
                        raise ValueError("resFormat option is not valid: {}".format(value))
                elif key == 'anim':
                    if value in ['none', 'keyed', 'frames']:
                        self.kwargs['anim'] = value
                    else:
                        raise ValueError("anim option is not valid: {}".format(value))
                elif key == 'vFlip':
                    if value == "1":
                        self.kwargs['vflip'] = True
                    elif value == "0":
                        self.kwargs['vflip'] = False
                    else:
                        raise ValueError("vFlip option is not valid: {}".format(value))
                elif key == 'includeMaterials':
                    if value == "1":
                        self.kwargs['include_materials'] = True
                    elif value == "0":
                        self.kwargs['include_materials'] = False
                    else:
                        raise ValueError("includeMaterials option is not valid: {}".format(value))
                elif key == 'includeNormals':
                    if value == "1":
                        self.kwargs['include_normals'] = True
                    elif value == "0":
                        self.kwargs['include_normals'] = False
                    else:
                        raise ValueError("includeNormals option is not valid: {}".format(value))
                elif key == 'transformsApplied':
                    if value == "1":
                        self.kwargs['transforms_applied'] = True
                    elif value == "0":
                        self.kwargs['transforms_applied'] = False
                    else:
                        raise ValueError("transformsApplied option is not valid: {}".format(value))
                elif key == 'joinMeshes':
                    if value == "1":
                        self.kwargs['join_meshes'] = True
                    elif value == "0":
                        self.kwargs['join_meshes'] = False
                    else:
                        raise ValueError("joinMeshes option is not valid: {}".format(value))


    def reader( self, fileObject, optionString, accessMode ):
        raise NotImplementedError()

    def identifyFile (file_obj, buffer, size):
        basename, ext = os.path.splitext(file_obj.fullName())
        if ext not in ['.glb', '.gltf']:
            return OpenMayaMPx.MPxFileTranslator.kNotMyFileType
        
        return OpenMayaMPx.MPxFileTranslator.kIsMyFileType
        

# creator
def translator_creator():
    return OpenMayaMPx.asMPxPtr( GLTFTranslator() )

# initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, PLUGIN_COMPANY, '1.0', "Any")
    try:
        mplugin.registerFileTranslator( PLUGIN_NAME, None, translator_creator,
                                        "glTFTranslatorOpts",
                                        "resFormat=embedded;anim=keyed;vFlip=1;includeMaterials=1;includeNormals=1;transformsApplied=0;joinMeshes=0",)
        '''
        status =  plugin.registerFileTranslator( "Lep",
                                        "lepTranslator.rgb",
                                        LepTranslator::creator,
                                        "lepTranslatorOpts",
                                        "showPositions=1",
                                        true );
        '''
    except:
        sys.stderr.write( "Failed to register translator: %s" % PLUGIN_NAME )
        raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        mplugin.deregisterFileTranslator( PLUGIN_NAME )
    except:
        sys.stderr.write( "Failed to deregister translator: %s" % PLUGIN_NAME )
        raise