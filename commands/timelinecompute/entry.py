import adsk.core
import adsk.fusion
import csv
import os
import secrets
import tempfile
import traceback
from pathlib import Path
from typing import Optional

# Import the fusionAddInUtils module from the parent directory.
from ...lib import fusionAddInUtils as futil
from ... import config

# Constants
SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60
MILLISECONDS_PER_SECOND = 1000
HOURS_PER_DAY = 24

# HTML template constants
HTML_CSS_TEMPLATE = """<style>
body {
    font-family: Arial, Helvetica, sans-serif;
}
.timeline-compute-report {
    overflow: auto;
    width: 100%;
}
.timeline-compute-report table {
    border: 1px solid #dededf;
    width: 100%;
    table-layout: fixed;
    border-collapse: collapse;
    border-spacing: 1px;
    text-align: left;
}
.timeline-compute-report caption {
    caption-side: top;
    text-align: left;
}
.timeline-compute-report th {
    border: 1px solid #dededf;
    background-color: #eceff1;
    color: #000000;
    padding: 5px;
}
.timeline-compute-report td {
    border: 1px solid #dededf;
    padding: 5px;
}
.timeline-compute-report tr:nth-child(even) td {
    background-color: #ffffff;
    color: #000000;
}
.timeline-compute-report tr:nth-child(odd) td {
    background-color: #ffffff;
    color: #000000;
}
</style>
"""

app = adsk.core.Application.get()
ui = app.userInterface

CMD_NAME = "Timeline Compute time to CSV"
CMD_ID = "PTPM-timelinecompute"
CMD_Description = "Dump compute time for each timeline feature to a CSV file. Features are sorted by compute time."
IS_PROMOTED = False

# Global variables by referencing values from /config.py
WORKSPACE_ID = config.design_workspace
TAB_ID = "SolidTab"
TAB_NAME = "Solid"

PANEL_ID = "InspectPanel"
PANEL_NAME = "Inspect"
CMD_AFTER = "InterferenceCheckCommand"

# Resource location for command icons, here we assume a sub folder in this directory named "resources".
ICON_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources", "")

# Local list of event handlers used to maintain a reference so
# they are not released and garbage collected.
local_handlers = []


# Executed when add-in is run.
def start():
    # ******************************** Create Command Definition ********************************
    cmd_def = ui.commandDefinitions.addButtonDefinition(
        CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER
    )

    # Add command created handler. The function passed here will be executed when the command is executed.
    futil.add_handler(cmd_def.commandCreated, command_created)

    # ******************************** Create Command Control ********************************
    # Get target workspace for the command.
    workspace = ui.workspaces.itemById(WORKSPACE_ID)

    # Get target toolbar tab for the command and create the tab if necessary.
    toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
    if toolbar_tab is None:
        toolbar_tab = workspace.toolbarTabs.add(TAB_ID, TAB_NAME)

    # Get target panel for the command and and create the panel if necessary.
    panel = toolbar_tab.toolbarPanels.itemById(PANEL_ID)
    if panel is None:
        panel = toolbar_tab.toolbarPanels.add(PANEL_ID, PANEL_NAME, "", False)

    # Create the command control, i.e. a button in the UI.
    control = panel.controls.addCommand(cmd_def, "", True)

    # Now you can set various options on the control such as promoting it to always be shown.
    control.isPromoted = IS_PROMOTED


# Executed when add-in is stopped.
def stop():
    # Get the various UI elements for this command
    workspace = ui.workspaces.itemById(WORKSPACE_ID)
    panel = workspace.toolbarPanels.itemById(PANEL_ID)
    toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
    command_control = panel.controls.itemById(CMD_ID)
    command_definition = ui.commandDefinitions.itemById(CMD_ID)

    # Delete the button command control
    if command_control:
        command_control.deleteMe()

    # Delete the command definition
    if command_definition:
        command_definition.deleteMe()

    # Delete the panel if it is empty
    if panel.controls.count == 0:
        panel.deleteMe()

    # Delete the tab if it is empty
    if toolbar_tab.toolbarPanels.count == 0:
        toolbar_tab.deleteMe()


# Function that is called when a user clicks the corresponding button in the UI.
# This defines the contents of the command dialog and connects to the command related events.
def command_created(args: adsk.core.CommandCreatedEventArgs):
    futil.log(f"{CMD_NAME} Command Created Event")

    # Connect to the events that are needed by this command.
    futil.add_handler(
        args.command.execute, command_execute, local_handlers=local_handlers
    )
    futil.add_handler(
        args.command.destroy, command_destroy, local_handlers=local_handlers
    )


def command_execute(args: adsk.core.CommandCreatedEventArgs):
    # this handles the document close and reopen
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        reportName = secrets.token_urlsafe(8)
        docName = app.activeDocument.name

        feats = app.executeTextCommand("fusion.DumpFeaturesByComputeTime /csv")
        print(feats)

        tempPath = tempfile.gettempdir()

        filepath = os.path.join(tempPath, reportName + ".csv")
        # Write the results to the file
        with open(filepath, "w") as f:
            f.write(feats)
        # ui.messageBox("CSV file saved at: " + filepath)

        totalTime = totalComputeTime(filepath)

        htmlfilepath = writeHTML(docName, filepath, totalTime)

        futil.log(
            f"CSV file saved at: {tempPath} with time {convert(totalTime)} (hour, minutes, seconds, milliseconds), QTWebBrowser.Display file:///{htmlfilepath}"
        )

        app.executeTextCommand(f"QTWebBrowser.Display file:///{htmlfilepath}")

    except:
        if ui:
            ui.messageBox("Failed:\n{}".format(traceback.format_exc()))


def convert(seconds):
    total_seconds = int(seconds)
    milliseconds = int((seconds - total_seconds) * 1000)

    total_seconds = total_seconds % (24 * 3600)
    hour = total_seconds // 3600
    total_seconds %= 3600
    minutes = total_seconds // 60
    seconds = total_seconds % 60

    return "%d:%02d:%02d.%03d" % (hour, minutes, seconds, milliseconds)


def totalComputeTime(s_csv):
    total_sum = 0

    # Replace 'your_file.csv' with the actual path to your CSV file
    with open(s_csv, "r") as file:
        reader = csv.reader(file)

        # Skip the header row if it exists
        next(reader, None)

        for row in reader:
            try:
                # Column indexing starts from 0, so the fourth column is at index 3
                # Convert the value to a float before adding to the sum
                total_sum += float(row[2])
            except (ValueError, IndexError):
                # Handle cases where the value is not a number or the row is too short
                print(f"Skipping invalid value or short row: {row}")
                continue
    # futil.log(f"{CMD_NAME} Total compute time is: {total_sum}")
    return total_sum


def HTMLCSS():

    htmlstyle = f"""<style>
body {{  font-family: Arial, Helvetica, sans-serif;
}}
.timeline-compute-report {{
    overflow: auto;
    width: 100%;
}}

.timeline-compute-report table {{
    border: 1px solid #dededf;
    width: 100%;
    table-layout: fixed;
    border-collapse: collapse;
    border-spacing: 1px;
    text-align: left;
}}

.timeline-compute-report caption {{
    caption-side: top;
    text-align: left;
}}

.timeline-compute-report th {{
    border: 1px solid #dededf;
    background-color: #eceff1;
    color: #000000;
    padding: 5px;
}}

.timeline-compute-report td {{
    border: 1px solid #dededf;
    padding: 5px;
}}

.timeline-compute-report tr:nth-child(even) td {{
    background-color: #ffffff;
    color: #000000;
}}

.timeline-compute-report tr:nth-child(odd) td {{
    background-color: #ffffff;
    color: #000000;
}}
</style>\n"""
    return htmlstyle


def HTMLHeader(d_name, time):

    header = f"""<html>\n
<h1>{d_name} Timeline Report</h1>
<body>
Total timeline compute: {convert(time)} <i>(hour, minutes, seconds, milliseconds)</i>
<br>
<br>\n"""
    return header


def TableHeader(d_name):
    theader = f"""<div class="timeline-compute-report" role="region" tabindex="0">
<table>
    <caption>Timeline Details</caption>
    <thead>
        <tr>
            <th>Component</th>
            <th>Feature</th>
            <th>Time (h:m:s:ms)</th>
            <th>Health</th>
        </tr>
    </thead>"""
    return theader


def TableContent(s_csv):
    with open(s_csv, mode="r", newline="") as file:
        # Create a csv.reader object
        reader = csv.reader(file)
        rows = f""

        # Iterate through each row in the CSV file
        for row in reader:
            # Skip the header row
            if reader.line_num == 1:
                continue

            # Ensure we have at least 4 columns, pad with empty strings if necessary
            while len(row) < 4:
                row.append("")

            # Write table row with 4 columns
            rows += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>\n"
            # Each 'row' is a list representing a line in the CSV
            # You can access individual columns by index (e.g., row[0], row[1])
    return rows


def HtmlFooter():
    footer = f"""</body>
</html>
"""
    return footer


def writeHTML(d_name, s_csv, totalTime):
    tempPath = tempfile.gettempdir()
    reportName = secrets.token_urlsafe(8)

    filepath = os.path.join(tempPath, reportName + ".html")
    # Write the results to the file
    with open(filepath, "w") as f:
        f.write(HTMLCSS())

        f.write(HTMLHeader(d_name, totalTime))

        f.write(TableHeader(d_name))

        f.write(TableContent(s_csv))

        f.write(HtmlFooter())

    # ui.messageBox("HTML file saved at: " + filepath)
    # futil.log(f"HTML file saved at: {tempPath}")

    path_with_backslashes = filepath
    path_object = Path(path_with_backslashes)
    reportpath = path_object.as_posix()  # Converts to a POSIX-style path string

    return reportpath


# This function will be called when the user completes the command.
def command_destroy(args: adsk.core.CommandEventArgs):
    global local_handlers
    local_handlers = []
    futil.log(f"{CMD_NAME} Command Destroy Event")
