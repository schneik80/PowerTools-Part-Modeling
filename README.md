# PowerTools: Part Modeling Tools for Autodesk Fusion

Power Tools for Part Modeling is an Autodesk Fusion add-in that provides productivity, utility, and analysis commands to support mechanical part design workflows. It includes commands for sketch repair, constraint analysis, model timeline performance reporting, and bulk visibility management.

## Prerequisites

Before you install and run this add-in, confirm that you have the following:

- **Autodesk Fusion** (any current subscription tier) with Python add-in support enabled
- **Windows 10/11** or **macOS**

## Installation

1. Download or clone this repository to your local machine.
2. In Autodesk Fusion, open the **Add-Ins** dialog by selecting **Utilities** > **Add-Ins**, or press **Shift+S**.
3. On the **Add-Ins** tab, click the green **+** icon.
4. Navigate to the folder where you placed the add-in files and select the `PowerTools-Part-Modeling` folder.
5. Click **Open**.
6. Select **Power Tools for Part Modeling** in the list, then click **Run**.

To have the add-in load automatically each time Fusion starts, select **Run on Startup** before clicking **Run**.

## Commands

The following commands are included in this add-in:

| Command | Category | Location | Description |
| --- | --- | --- | --- |
| [Sketch Repair](./docs/SketchFix.md) | Productivity | Sketch &rsaquo; Modify | Repairs small gaps and disconnected endpoints in the active sketch. |
| [Sketch Under-Constrained](./docs/SketchUnder.md) | Productivity | Sketch &rsaquo; Modify | Highlights sketch entities that lack sufficient constraints or dimensions. |
| [Radial Hole Circle](./docs/RadialHoleCircle.md) | Productivity | Sketch &rsaquo; Create | Places a construction circle anchored to an existing sketch point, with a diameter dimension and vertically constrained top point. |
| [Timeline Compute Report](./docs/Timeline%20Compute%20Times.md) | Analysis | Solid &rsaquo; Inspect | Generates a sortable HTML report of feature compute times across the model timeline. |
| [Create Mirrored Design](./docs/MirrorDerive.md) | Productivity | Solid &rsaquo; Create | Derives all model bodies into a new document, saves as `<active-name>-mirror`, applies scale `-1`, and saves again. |
| [Hide Objects](./docs/HideObjects.md) | Utility | Tools &rsaquo; Utility | Hides selected categories of reference and construction geometry across all components in the active design. |

---

## Productivity tools

### Sketch Repair

The **Sketch Repair** command attempts to fix common sketch profile issues automatically. It performs two repair passes: the first removes tiny segments at or below the geometry tolerance threshold, and the second closes small gaps by merging disconnected endpoints.

**Requirements:** A design document must be open and a sketch must be in active edit mode.

For full usage details, see [Sketch Repair](./docs/SketchFix.md).

### Sketch Under-Constrained

The **Sketch Under-Constrained** command highlights all sketch entities that are not fully constrained. Use this command to quickly locate lines, curves, or points that still need dimensions or geometric constraints in complex sketches.

**Requirements:** A design document must be open and a sketch must be in active edit mode.

For full usage details, see [Sketch Under-Constrained](./docs/SketchUnder.md).

### Radial Hole Circle

The **Radial Hole Circle** command places a construction circle in the active sketch. Select an existing sketch point or vertex as the center, drag the mouse to preview the diameter in real time, then click to commit. A diameter dimension and a vertically constrained sketch point are automatically added at the top of the circle.

**Requirements:** A design document must be open and a sketch must be in active edit mode.

For full usage details, see [Radial Hole Circle](./docs/RadialHoleCircle.md).

### Create Mirrored Design

The **Create Mirrored Design** command creates a new design based on the currently active saved 3D design. It derives the model content into a new document, saves the new file using the active document name with `-mirror` appended, scales all derived geometry by `-1`, and saves the result.

**Requirements:**

- The active product must be a Fusion design.
- The active design must already be saved to Fusion (must have a Data File).
- The command must be run from the Design workspace.

---

## Utility tools

### Hide Objects

The **Hide Objects** command hides selected categories of reference and construction geometry across every component in the active design in a single operation. Use it to quickly declutter the viewport before sharing, rendering, or reviewing a model.

All eight object categories are enabled by default: Origin, Construction Points, Construction Axes, Construction Planes, Joint Origins, Joints, Sketches, and Canvas. Uncheck any category you want to leave visible before clicking **OK**.

**Requirements:** A design document must be open in the Design workspace.

For full usage details, see [Hide Objects](./docs/HideObjects.md).

---

## Analysis tools

### Timeline Compute Report

The **Timeline Compute Report** command generates an interactive HTML report showing the compute time for each feature in the model timeline, sorted from shortest to longest. A visual percentage bar column makes it easy to identify features that disproportionately extend model rebuild times.

The command also exports the underlying raw data as a CSV file to your system's temporary directory.

**Requirements:** The active design must use the parametric timeline. This command is not available for designs in Direct Design mode.

For full usage details, see [Timeline Compute Report](./docs/Timeline%20Compute%20Times.md).

---

## Support

This add-in is developed and maintained by IMA LLC.

---

## License

This project is released under the [GNU General Public License v3.0 or later](LICENSE).

Copyright (C) 2022-2026 IMA LLC.

The vendored library at `lib/fusionAddInUtils` is Autodesk sample code and is distributed under its own license terms; see its source headers for details.

---

*Copyright © 2026 IMA LLC. All rights reserved.*
