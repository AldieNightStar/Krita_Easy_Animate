from krita import *
from .plugin import pluginInstance
from PyQt5.QtWidgets import *

K = Krita.instance()

class AnimationHelperDocker(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Easy Animate")
        
        # Create the main widget and layout
        self._main_widget = QWidget(self)
        vbox = QVBoxLayout(self._main_widget)
        hbox1 = QHBoxLayout(self._main_widget)
        hbox2 = QHBoxLayout(self._main_widget)
        
        # Create Quick Buttons
        self._button(vbox, "⚒️ Select Transform", pluginInstance.trans_select)
        self._button(vbox, "✨ Transform Visible", pluginInstance.trans_visible_toggle)

        # Add hbox panel
        self._button(hbox1, "♦️", pluginInstance.trans_new_frame)
        self._button(hbox1, "❌", pluginInstance.trans_rem_frame)
        self._button(hbox1, "📚", pluginInstance.copy_frames)
        self._button(hbox1, "📋", pluginInstance.paste_frames)

        self._button(hbox2, "📈const", pluginInstance.create_trans_interpol('interpolation_constant'))
        self._button(hbox2, "📈lin", pluginInstance.create_trans_interpol('interpolation_linear'))
        self._button(hbox2, "📈bez", pluginInstance.create_trans_interpol('interpolation_bezier'))

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        hbox1.addStretch()
        hbox2.addStretch()
        vbox.addStretch()
        self.setWidget(self._main_widget)
        
    # Required by Krita
    def canvasChanged(self, canvas):
        pass

    def _button(self, parent, name, act):
        b = QPushButton(name, self._main_widget)
        b.clicked.connect(act)
        parent.addWidget(b)
        return b