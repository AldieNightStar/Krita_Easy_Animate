from krita import *

# Panel will import plugin and all its setup
from .panel import *

# Create dock panel
factory = DockWidgetFactory(
    "easy_animate_dock",
    DockWidgetFactoryBase.DockRight,
    AnimationHelperDocker
)
Krita.instance().addDockWidgetFactory(factory)
