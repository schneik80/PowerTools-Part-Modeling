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

CMD_NAME = "Timeline Compute Report"
CMD_ID = "PTPM-timelinecompute"
CMD_Description = "Display a timeline compute report. Also exports a CSF as source data. Features are sorted by compute time."
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
def start() -> None:
    """Initialize and start the timeline compute command."""
    try:
        # Create Command Definition
        cmd_def = ui.commandDefinitions.addButtonDefinition(
            CMD_ID, CMD_NAME, CMD_Description, ICON_FOLDER
        )

        # Add command created handler
        futil.add_handler(cmd_def.commandCreated, command_created)

        # Create Command Control
        workspace = ui.workspaces.itemById(WORKSPACE_ID)
        if not workspace:
            futil.log(f"Warning: Workspace {WORKSPACE_ID} not found")
            return

        # Get or create toolbar tab
        toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
        if toolbar_tab is None:
            toolbar_tab = workspace.toolbarTabs.add(TAB_ID, TAB_NAME)

        # Get or create panel
        panel = toolbar_tab.toolbarPanels.itemById(PANEL_ID)
        if panel is None:
            panel = toolbar_tab.toolbarPanels.add(PANEL_ID, PANEL_NAME, "", False)

        # Create the command control
        control = panel.controls.addCommand(cmd_def, "", True)
        control.isPromoted = IS_PROMOTED

        futil.log(f"{CMD_NAME} command started successfully")

    except Exception as e:
        futil.log(f"Error starting {CMD_NAME}: {e}")


# Executed when add-in is stopped.
def stop() -> None:
    """Clean up and stop the timeline compute command."""
    try:
        # Get the various UI elements for this command
        workspace = ui.workspaces.itemById(WORKSPACE_ID)
        if not workspace:
            return

        panel = workspace.toolbarPanels.itemById(PANEL_ID)
        toolbar_tab = workspace.toolbarTabs.itemById(TAB_ID)
        command_control = panel.controls.itemById(CMD_ID) if panel else None
        command_definition = ui.commandDefinitions.itemById(CMD_ID)

        # Delete the button command control
        if command_control:
            command_control.deleteMe()

        # Delete the command definition
        if command_definition:
            command_definition.deleteMe()

        # Delete the panel if it is empty
        if panel and panel.controls.count == 0:
            panel.deleteMe()

        # Delete the tab if it is empty
        if toolbar_tab and toolbar_tab.toolbarPanels.count == 0:
            toolbar_tab.deleteMe()

        futil.log(f"{CMD_NAME} command stopped successfully")

    except Exception as e:
        futil.log(f"Error stopping {CMD_NAME}: {e}")


def command_created(args: adsk.core.CommandCreatedEventArgs) -> None:
    """
    Handle command creation event.

    Args:
        args: Command creation event arguments
    """
    futil.log(f"{CMD_NAME} Command Created Event")

    try:
        # Connect to the events that are needed by this command
        futil.add_handler(
            args.command.execute, command_execute, local_handlers=local_handlers
        )
        futil.add_handler(
            args.command.destroy, command_destroy, local_handlers=local_handlers
        )
    except Exception as e:
        futil.log(f"Error in command_created: {e}")


def command_execute(args: adsk.core.CommandCreatedEventArgs) -> None:
    """
    Execute the timeline compute command.

    Args:
        args: Command execution arguments
    """
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        doc_name = app.activeDocument.name

        # Generate timeline features data
        features_data = app.executeTextCommand("fusion.DumpFeaturesByComputeTime /csv")
        futil.log(f"Generated features data for document: {doc_name}")

        # Create temporary CSV file
        csv_filepath = _create_temp_csv_file(features_data)

        # Calculate total compute time
        total_time = _calculate_total_compute_time(csv_filepath)

        # Generate HTML report
        html_filepath = _generate_html_report(doc_name, csv_filepath, total_time)

        # Debug log the report generation
        futil.log(
            f"Report generated - CSV: {csv_filepath}, "
            f"Total time: {format_time_duration(total_time)}, "
            f"HTML: {html_filepath}"
        )

        # Display the HTML report using Fusion built in QTWebBrowser
        app.executeTextCommand(f"QTWebBrowser.Display file:///{html_filepath}")

    except Exception as e:
        error_msg = (
            f"Timeline compute command failed: {str(e)}\n{traceback.format_exc()}"
        )
        futil.log(error_msg)
        if ui:
            ui.messageBox(f"Failed to generate timeline report:\n{str(e)}")


def _create_temp_csv_file(data: str) -> str:
    """
    Create a temporary CSV file with the provided data.

    Args:
        data: CSV data as string

    Returns:
        Path to the created CSV file
    """
    temp_path = tempfile.gettempdir()
    report_name = secrets.token_urlsafe(8)
    filepath = os.path.join(temp_path, f"{report_name}.csv")

    with open(filepath, "w", encoding="utf-8", newline="") as f:
        f.write(data)

    return filepath


def format_time_duration(seconds: float) -> str:
    """
    Convert seconds to formatted time string (h:mm:ss.mmm).

    Args:
        seconds: Time duration in seconds

    Returns:
        Formatted time string
    """
    total_seconds = int(seconds)
    milliseconds = int((seconds - total_seconds) * MILLISECONDS_PER_SECOND)

    total_seconds = total_seconds % (HOURS_PER_DAY * SECONDS_PER_HOUR)
    hours = total_seconds // SECONDS_PER_HOUR
    total_seconds %= SECONDS_PER_HOUR
    minutes = total_seconds // SECONDS_PER_MINUTE
    remaining_seconds = total_seconds % SECONDS_PER_MINUTE

    return f"{hours}:{minutes:02d}:{remaining_seconds:02d}.{milliseconds:03d}"


def _calculate_total_compute_time(csv_filepath: str) -> float:
    """
    Calculate the total compute time from the CSV file. Assumes the third column contains time in seconds.

    Args:
        csv_filepath: Path to the CSV file

    Returns:
        Total compute time in seconds
    """
    total_sum = 0.0

    try:
        with open(csv_filepath, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            # Skip the header row
            next(reader, None)

            for row_num, row in enumerate(
                reader, start=2
            ):  # Start from 2 since we skipped header
                try:
                    if len(row) >= 3:  # Ensure we have at least 3 columns
                        total_sum += float(row[2])  # Third column contains the time
                except (ValueError, IndexError) as e:
                    futil.log(f"Skipping invalid row {row_num}: {row} - Error: {e}")
                    continue

    except (FileNotFoundError, IOError) as e:
        futil.log(f"Error reading CSV file {csv_filepath}: {e}")
        raise

    return total_sum


def _get_html_css() -> str:
    """
    Get the CSS styles for the HTML report.

    Returns:
        CSS styles as string
    """
    return HTML_CSS_TEMPLATE


def _get_html_header(document_name: str, total_time: float) -> str:
    """
    Generate the HTML header section.

    Args:
        document_name: Name of the Fusion 360 document
        total_time: Total compute time in seconds

    Returns:
        HTML header as string
    """
    return f"""<html>
<head>
    <title>{document_name} Timeline Report</title>
</head>
<body>
<h1>{document_name} Timeline Report</h1>
<p>Total timeline compute: {format_time_duration(total_time)} <i>(hour:minutes:seconds.milliseconds)</i><br>
Table sorted from shortest to longest feature compute.</p>
<br>
"""


def _get_table_header() -> str:
    """
    Generate the HTML table header.

    Returns:
        HTML table header as string
    """
    return """<div class="timeline-compute-report" role="region" tabindex="0">
<table>
    <caption>Timeline Details</caption>
    <thead>
        <tr>
            <th>Component</th>
            <th>Feature</th>
            <th>Time (seconds)</th>
            <th>Health</th>
        </tr>
    </thead>
    <tbody>"""


def _generate_table_content(csv_filepath: str) -> str:
    """
    Generate HTML table content from CSV data.

    Args:
        csv_filepath: Path to the CSV file

    Returns:
        HTML table rows as string
    """
    rows = []

    try:
        with open(csv_filepath, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)

            # Skip the header row
            next(reader, None)

            for row in reader:
                # Ensure we have at least 4 columns, pad with empty strings if necessary
                padded_row = row + [""] * (4 - len(row))

                # Escape HTML characters in cell content
                escaped_cells = [_escape_html(str(cell)) for cell in padded_row[:4]]

                row_html = f"<tr><td>{escaped_cells[0]}</td><td>{escaped_cells[1]}</td><td>{escaped_cells[2]}</td><td>{escaped_cells[3]}</td></tr>"
                rows.append(row_html)

    except (FileNotFoundError, IOError) as e:
        futil.log(f"Error reading CSV file for table content: {e}")
        rows.append("<tr><td colspan='4'>Error reading data</td></tr>")

    return "\n".join(rows)


def _escape_html(text: str) -> str:
    """
    Escape HTML special characters.

    Args:
        text: Text to escape

    Returns:
        HTML-escaped text
    """
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def _get_html_footer() -> str:
    """
    Generate the HTML footer.

    Returns:
        HTML footer as string
    """
    return """    </tbody>
</table>
</div>
</body>
</html>"""


def _generate_html_report(
    document_name: str, csv_filepath: str, total_time: float
) -> str:
    """
    Generate a complete HTML report from CSV data.

    Args:
        document_name: Name of the Fusion 360 document
        csv_filepath: Path to the CSV file containing timeline data
        total_time: Total compute time in seconds

    Returns:
        Path to the generated HTML file
    """
    temp_path = tempfile.gettempdir()
    report_name = secrets.token_urlsafe(8)
    html_filepath = os.path.join(temp_path, f"{report_name}.html")

    try:
        with open(html_filepath, "w", encoding="utf-8") as f:
            f.write(_get_html_css())
            f.write(_get_html_header(document_name, total_time))
            f.write(_get_table_header())
            f.write(_generate_table_content(csv_filepath))
            f.write(_get_html_footer())

        # Convert to POSIX-style path for cross-platform compatibility
        return Path(html_filepath).as_posix()

    except IOError as e:
        futil.log(f"Error writing HTML file: {e}")
        raise


def command_destroy(args: adsk.core.CommandEventArgs) -> None:
    """
    Handle command destruction event.

    Args:
        args: Command event arguments
    """
    global local_handlers
    local_handlers = []
    futil.log(f"{CMD_NAME} Command Destroy Event")
