from krita import *
from .plugin import pluginInstance
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

K = Krita.instance()

class AnimationHelperDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Easy Animate")
        
        # Create the main widget and layout
        self._main_widget = QWidget(self)
        self._layout = QVBoxLayout(self._main_widget)
        
        # Create Quick Buttons
        self._button("⚒️ Select Transform", pluginInstance.trans_select)
        self._button("✨ Transform Visible", pluginInstance.trans_visible_toggle)
        self._button("🧾 Transform Key", pluginInstance.trans_new_frame)
        self._button("❌ Remove Transform Key", pluginInstance.trans_rem_frame)

        self._layout.addStretch() # Pushes buttons to the top
        self.setWidget(self._main_widget)
        
    # Required by Krita
    def canvasChanged(self, canvas):
        pass

    def _button(self, name, act):
        b = QPushButton(name, self._main_widget)
        b.clicked.connect(act)
        self._layout.addWidget(b)
        return b
