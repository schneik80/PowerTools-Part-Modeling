import adsk.core
import os
import os.path
import json
from .lib import fusionAddInUtils as futil

DEBUG = True
ADDIN_NAME = os.path.basename(os.path.dirname(__file__))
COMPANY_NAME = "IMA LLC"
COMPANY_HUB =""

#COMPANY_HUB = "a.YnVzaW5lc3M6aW1hbGxj"

def loadHub(__file__):

    app = adsk.core.Application.get()
    ui = app.userInterface
    my_addin_path = os.path.dirname(os.path.realpath(__file__))
    my_hub_path = os.path.join(my_addin_path, "hub.json")

    docsExist = os.path.isfile(my_hub_path)

    if docsExist == False:
        global COMPANY_HUB

        ui.messageBox(
            "Hub Configuration file is missing.\nPlease read the documentation and configure your hub",
            "No Hub Configured",
            0,
            3,
        )
    else:
        with open(my_hub_path) as json_file:
            my_hub = json.load(json_file)
            COMPANY_HUB = my_hub.get('HUB_ID')
data = loadHub(__file__)


# Palettes
sample_palette_id = f"{COMPANY_NAME}_{ADDIN_NAME}_palette_id"

design_workspace = "FusionSolidEnvironment"
tools_tab_id = "ToolsTab"
my_tab_name = "Power Tools"

my_panel_id = f"{ADDIN_NAME}_panel_2"
my_panel_name = "Tools"
my_panel_after = ""