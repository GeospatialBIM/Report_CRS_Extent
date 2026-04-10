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
- EPSG Code
- Version of the File
- ExteriorShell model extents (X, Y, Z)
- A summary section highlighting un‑georeferenced models
- A timestamp and disclaimer clarifying data responsibility
- Display Unit System
- Length Display Unit
- Model Length Unit 

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
## 🚀 Key Features

- ✅ Recursively scans a workspace folder for:
  - Autodesk Revit files (`.rvt`)
  - IFC files (`.ifc`)
- ✅ Reports **per BIM file**:
  - CRS name
  - EPSG code (when available)
  - Spatial extent:
    - XMin
    - YMin
    - XMax
    - YMax
  - Georeferencing status
  - **IFC length unit** (IFC only)
- ✅ Output options:
  - Console report
  - Optional text (`.txt`) report
- ✅ Separate reports:
  - **FULL BIM Report** (all files)
  - **UN‑GEOREFERENCED ONLY Report**
- ✅ Designed for **ArcGIS Pro Notebook** execution
- ✅ Vendor‑neutral and standards‑focused

---

## 📂 Supported File Types

| File Type | Supported | Notes |
|----------|----------|------|
| `.rvt` | ✅ | CRS & spatial extent only |
| `.ifc` | ✅ | CRS, extent, **length unit extracted** |
| Other | ❌ | Ignored |

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

## 📑 Generated Reports

This script can generate **two separate text files**:

### 1️⃣ Full BIM Report  
Includes **all detected BIM files**.

Default:
```
BIM_Report_.txt
```

### 2️⃣ Un‑Georeferenced BIM Report  
Includes **only files flagged as UN‑GEOREFERENCED**.

Default:
```
BIM_UnGeoreferenced_Report_.txt
```

The un‑georeferenced report is offered **only if applicable files exist**.
****

## 📝 Text Output Behavior

- Default output filename:
  ```
  BIM_Report_.txt
  ```
- The user may:
  - Accept the default location
  - Specify a custom path
- The script will:
  - Attempt to create directories if missing
  - Warn the user if file permissions prevent saving

---

## 📏 IFC Length Unit Reporting

- Length units are extracted **only for IFC files**
- Detection is based on parsing readable IFC text
- Typical reported values:
  - `METERS`
  - `MILLIMETERS`
  - `FEET`
- For Revit models:
  ```
  Length Unit: N/A
  ```

---

## ⚠️ Important Disclaimer

The report only displays the spatial reference and extent information recorded in the BIM file.  
It does **not** validate whether the georeferenced data aligns correctly with the intended real‑world project location.  
Ensuring correct georeferencing remains the responsibility of the data provider or vendor.

> **This tool performs metadata‑level validation only.**

- It does **not** verify real‑world spatial accuracy
- CRS values may exist but be incorrectly assigned
- Spatial extents may fall outside valid CRS bounds
- IFC parsing depends on accessible text content

⚠️ **Results should always be validated against project control, survey data, and authoritative GIS references.**

This script must **not** be used as a substitute for professional surveying or engineering review.
