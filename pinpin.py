from Packages.utils.init_pinpin import init_pinpin
init_pinpin()

from Packages.utils.logger import init_logger
logger = init_logger(__file__)

import sys
from Packages.apps.standalone.standalone_app import PinpinApp

app = PinpinApp(sys.argv)
logger.info('Launch Pinpin standalone application.')
app.exec_()
logger.info('Close Pinpin standalone application.')

"""
- asset
    - petru
    - bob
    
- prop
    - rien
    - rerien
"""