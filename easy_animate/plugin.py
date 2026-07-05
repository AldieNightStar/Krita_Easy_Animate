from krita import Extension, Krita
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

K = Krita.instance()

class EasyAnimatePlugin(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        pass

    def trans_new_frame(self):
        doc = K.activeDocument()
        K.action('add_scalar_keyframes').trigger()
        doc.refreshProjection()
        
    def trans_rem_frame(self):
        doc = K.activeDocument()
        K.action('remove_scalar_keyframe').trigger()
        K.action('remove_frames').trigger()
        doc.refreshProjection()

    def trans_select(self):
        doc = K.activeDocument()
        transform = self._getOrCreateTransLayer()
        doc.setActiveNode(transform)

    def trans_visible_toggle(self):
        doc = K.activeDocument()
        transfrom = self._getTransLayer()
        if transfrom is None: return
        transfrom.setVisible(not transfrom.visible())
        doc.refreshProjection()

    def copy_frames(self):
        doc = K.activeDocument()
        K.action('copy_frames').trigger()

    def paste_frames(self):
        doc = K.activeDocument()
        K.action('paste_frames').trigger()

    def create_trans_interpol(self, name):
        def _method():
            doc = K.activeDocument()
            self._select_current_curves()
            K.action(name).trigger()
            doc.refreshProjection()
        return _method

    def _getTransLayer(self):
        doc = K.activeDocument()
        layer = doc.activeNode()

        # If current layer transform, then return as is
        if layer.type() == "transformmask":
            return layer

        # Try get Transform as sub-layer
        for sublayer in layer.childNodes():
            if sublayer.type() == "transformmask":
                return sublayer
        return None

    def _getOrCreateTransLayer(self):
        transform = self._getTransLayer()
        if transform is None:
            transform = self._addTransform()
        return transform

    def _addTransform(self):
        doc = K.activeDocument()
        layer = doc.activeNode()

        transform = doc.createTransformMask("Transform")
        layer.addChildNode(transform, None)
        return transform

    def _newAction(self, win, name, desc, act):
        action = win.createAction(name, desc, "tools/scripts")

    def _get_anim_docker(self):
        for docker in K.dockers():
            name = docker.objectName().lower()
            if "animation" in name and "docker" in name:
                docker.setVisible(True)
                return docker
        raise IndexError("Can't find any Animation Docker")
    
    def _select_current_curves(self):
        curves_docker = self._get_anim_docker()
        current_frame = K.activeDocument().currentTime()
        view = curves_docker.findChild(QAbstractItemView)
        if view and view.model():
            model = view.model()
            selection_model = view.selectionModel()
            selection_model.clearSelection()
            precise_selection = QItemSelection()
            total_rows = model.rowCount()
            
            for row in range(total_rows):
                cell_index = model.index(row, current_frame)
                if cell_index.isValid():
                    precise_selection.select(cell_index, cell_index)
            selection_model.select(
                precise_selection, 
                selection_model.Select
            )
            view.viewport().update()
        else:
            raise IndexError("Can't find view for Animation Curves")

pluginInstance = EasyAnimatePlugin(K)
K.addExtension(pluginInstance)