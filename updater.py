from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import time
import shutil
import os
import signal
import sys

dev_folder = os.path.expanduser("~/Documents/GitHub/maya-glTF")
maya_plugins = os.path.expanduser("~/Library/Preferences/Autodesk/maya/2026/plug-ins")
maya_scripts = os.path.expanduser("~/Library/Preferences/Autodesk/maya/2026/scripts")

def safe_copy(src, dst):
    if os.path.abspath(src) == os.path.abspath(dst):
        return
    try:
        shutil.copy2(src, dst)
        print(f"Updated: {os.path.basename(src)}")
    except shutil.SameFileError:
        pass
    except Exception as e:
        print(f"Error copying {src} -> {dst}: {e}")

# Sync all files on script start
src_plugin = os.path.join(dev_folder, "plug-ins", "glTFTranslator.py")
dst_plugin = os.path.join(maya_plugins, "glTFTranslator.py")
safe_copy(src_plugin, dst_plugin)

src_opts = os.path.join(dev_folder, "scripts", "glTFTranslatorOpts.mel")
dst_opts = os.path.join(maya_scripts, "glTFTranslatorOpts.mel")
safe_copy(src_opts, dst_opts)

src_export = os.path.join(dev_folder, "scripts", "glTFExport.py")
dst_export = os.path.join(maya_scripts, "glTFExport.py")
safe_copy(src_export, dst_export)

class PluginHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        fname = os.path.basename(event.src_path)
        if fname == "glTFTranslator.py":
            safe_copy(event.src_path, os.path.join(maya_plugins, fname))
        elif fname == "glTFTranslatorOpts.mel":
            safe_copy(event.src_path, os.path.join(maya_scripts, fname))
        elif fname == "glTFExport.py":
            safe_copy(event.src_path, os.path.join(maya_scripts, fname))

observer = Observer()
observer.schedule(PluginHandler(), path=dev_folder, recursive=True)
observer.start()

def signal_handler(sig, frame):
    print("Stopping watcher...")
    observer.stop()
    observer.join()
    print("Watcher stopped")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("Watching for file changes. Press Ctrl+C to stop.")
while True:
    time.sleep(1)