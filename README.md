# Power Tools for Part Modeling

Power Tools for Part Modeling is an Autodesk Fusion add-in that provides productivity and analysis utilities to support mechanical part design workflows. It includes commands for sketch repair, constraint analysis, and model timeline performance reporting.

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
|---|---|---|---|
| [Sketch Repair](./docs/SketchFix.md) | Productivity | Sketch &rsaquo; Modify | Repairs small gaps and disconnected endpoints in the active sketch. |
| [Sketch Under-Constrained](./docs/SketchUnder.md) | Productivity | Sketch &rsaquo; Modify | Highlights sketch entities that lack sufficient constraints or dimensions. |
| [Timeline Compute Report](./docs/Timeline%20Compute%20Times.md) | Analysis | Solid &rsaquo; Inspect | Generates a sortable HTML report of feature compute times across the model timeline. |

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

This project is released under the [MIT License](LICENSE).

---

*Copyright © 2026 IMA LLC. All rights reserved.*
