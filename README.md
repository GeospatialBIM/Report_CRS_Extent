# BIM Georeferencing Audit Script (ArcPy)

## Overview

This repository contains a Python (ArcPy) script that audits georeferencing metadata for BIM files stored in a folder structure.  
The script recursively scans Revit (`.rvt`) and IFC (`.ifc`) files, extracts recorded spatial reference (CRS) information and exterior model extents, evaluates georeferencing readiness, and generates a timestamped, human‑readable text report.

The output is intended to support **BIM intake validation**, **BIM‑to‑GIS workflows**, and **vendor quality assurance** prior to integrating BIM data into GIS environments such as ArcGIS Pro.

---

## What the Script Reports

For each BIM file, the report includes:

- File name
- BIM data type (Revit / IFC)
- Georeferencing status (Georeferenced vs. Un‑Georeferenced)
- Recorded spatial reference (CRS)
- ExteriorShell model extents (X, Y, Z)
- A summary section highlighting un‑georeferenced models
- A timestamp and disclaimer clarifying data responsibility
- Display units (model)

> **Important**  
> The report reflects only the spatial reference and extent information recorded in the BIM file.  
> Vendors are responsible for ensuring that georeferenced data is correct for the project location.

---

## Requirements

- **ArcGIS Pro** (3.6 recommended)
- **Python 3.x** (installed with ArcGIS Pro)
- **ArcPy** (comes with ArcGIS Pro)
- Read access to the folder containing BIM files (`.rvt`, `.ifc`)

No third‑party Python packages are required.

---

## Usage

### Option 1: Run as a Python Script

1. Open an ArcGIS Pro Python environment or ArcGIS Pro Notebook
2. Update the `workspace` variable in the script to point to your BIM folder
3. Run the script
4. When prompted, choose whether to save the report to a text file

A timestamped `.txt` report will be generated in the workspace folder by default.

---

### Option 2: Run as an ArcGIS Pro Script Tool

The script can be added to a custom toolbox in ArcGIS Pro and configured to accept:
- Input folder
- Output report path

This option is recommended for repeated use or distribution to non‑developers.

---

## Typical Use Cases

- BIM georeferencing QA checks
- BIM delivery validation from vendors
- Pre‑processing checks before BIM‑to‑GIS integration
- Identifying BIM files missing CRS or exterior geometry
- Supporting infrastructure and AEC GIS workflows

---

## Disclaimer

The report only displays the spatial reference and extent information recorded in the BIM file.  
It does **not** validate whether the georeferenced data aligns correctly with the intended real‑world project location.  
Ensuring correct georeferencing remains the responsibility of the data provider or vendor.
``
