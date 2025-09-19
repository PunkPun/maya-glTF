To hot reload the plugin in maya, type this into the maya console

```python
import maya.mel as mel
import maya.cmds as cmds

def update():
    mel.eval('rehash; source "glTFTranslatorOpts.mel";')
    cmds.unloadPlugin("glTFTranslator.py")
    cmds.loadPlugin("glTFTranslator.py")
```

and now you can just call update()

Or just for the mel changes in the mel console:

```mel
rehash;
source "glTFTranslatorOpts.mel";
```