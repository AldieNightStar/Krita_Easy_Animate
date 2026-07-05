from krita import Extension, Krita
from PyQt5.QtWidgets import QMessageBox

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
        transform = self._getOrCreateTransLayer()

        oldActive = doc.activeNode()
        doc.setActiveNode(transform)
        K.action('add_scalar_keyframes').trigger()
        doc.setActiveNode(oldActive)
        
    def trans_rem_frame(self):
        doc = K.activeDocument()
        transform = self._getOrCreateTransLayer()
        if transform is None: return

        oldActive = doc.activeNode()
        doc.setActiveNode(transform)
        K.action('remove_scalar_keyframe').trigger()
        K.action('remove_frames').trigger()
        doc.setActiveNode(oldActive)
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

    def create_interpol(self, name):
        def _method():
            doc = K.activeDocument()
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

pluginInstance = EasyAnimatePlugin(K)
K.addExtension(pluginInstance)