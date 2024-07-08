"""from Packages.utils.init_pinpin import init_pinpin
init_pinpin()

from Packages.utils.logger import init_logger
logger = init_logger(__file__)"""

import sys
from Packages.apps.standalone.standalone_app import PinpinApp

app = PinpinApp(sys.argv)
app.exec_()