import arcpy
import os
from datetime import datetime

# Path to the folder containing BIM files
workspace = r"\Downloads\ARENA"
arcpy.env.workspace = workspace
results = []

# Output text file path (saved in the workspace folder)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_txt = os.path.join(workspace, f"BIM_Report_{timestamp}.txt")

# Iterate through the folder
for dirpath, dirnames, filenames in os.walk(workspace):
    for filename in filenames:

        # Check RVT or IFC
        if not filename.lower().endswith((".rvt", ".ifc")):
            continue

        full_path = os.path.join(dirpath, filename)

        # Describe the BIM file
        desc = arcpy.Describe(full_path)
        exterior_extent = None

        # Look for ExteriorShell feature class
        if hasattr(desc, "children"):
            for child in desc.children:
                for fc in getattr(child, "children", []):
                    fc_name = getattr(fc, "name", "").lower()

                    if "exteriorshell" in fc_name:
                        fc_path = getattr(fc, "catalogPath", None)
                        if fc_path:
                            fc_desc = arcpy.Describe(fc_path)
                            ext = fc_desc.extent

                            exterior_extent = {
                                "XMin": ext.XMin,
                                "YMin": ext.YMin,
                                "XMax": ext.XMax,
                                "YMax": ext.YMax,
                                "ZMin": ext.ZMin,
                                "ZMax": ext.ZMax,
                                "SpatialReference": (
                                    ext.spatialReference.name
                                    if ext.spatialReference else None
                                )
                            }
                        break  # stop once ExteriorShell is found

        # ---- GEOREFERENCE STATUS (MUST BE PER FILE) ----
        spatial_ref = (
            exterior_extent.get("SpatialReference")
            if exterior_extent else None
        )

        if not exterior_extent:
            geo_status = "UN-GEOREFERENCED (No ExteriorShell)"
        elif not spatial_ref or spatial_ref.lower() in ("unknown", "unnamed"):
            geo_status = "UN-GEOREFERENCED (No Spatial Reference)"
        else:
            geo_status = "GEOREFERENCED"

        # ---- APPEND RESULT (PER FILE) ----
        results.append({
            "Name": desc.name,
            "DataType": desc.dataType,
            "ExteriorShellExtent": exterior_extent,
            "GeoreferenceStatus": geo_status
        })

def build_summary(results):
    total = len(results)
    georef = sum(
        1 for r in results
        if r.get("GeoreferenceStatus") == "GEOREFERENCED"
    )
    ungeoref = total - georef

    ungeoref_files = [
        r.get("Name") for r in results
        if r.get("GeoreferenceStatus", "").startswith("UN-GEOREFERENCED")
    ]

    return {
        "Total": total,
        "Georeferenced": georef,
        "UnGeoreferenced": ungeoref,
        "UnGeoreferencedFiles": ungeoref_files
    }


def format_results(results):
    lines = []

  # ---- Timestamp ---- 
    report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines.append("=" * 80)
    lines.append("BIM GEOREFERENCING REPORT")
    lines.append(f"Report Generated : {report_time}")
    lines.append(f"Workspace        : {workspace}")
    lines.append("=" * 80)
    lines.append("")
  

    # ---- SUMMARY SECTION ----
    summary = build_summary(results)

    lines.append("=" * 80)
    lines.append("BIM GEOREFERENCING SUMMARY")
    lines.append("=" * 80)
    lines.append(f"Total BIM Files          : {summary['Total']}")
    lines.append(f"Georeferenced Models     : {summary['Georeferenced']}")
    lines.append(f"Un-Georeferenced Models  : {summary['UnGeoreferenced']}")


 # ---- DISCLAIMER ----
    lines.append("")
    lines.append("=" * 80)
    lines.append("DISCLAIMER")
    lines.append("=" * 80)
    lines.append(
        "The report just shows the Spatial Reference (CRS) and extent "
        "that is recorded in the file."
    )
    lines.append(
        "The vendor needs to ensure, however, that the georeferenced data "
        "is correct for the project location."
    )
    lines.append("=" * 80)
    lines.append("")



    if summary["UnGeoreferencedFiles"]:
        lines.append("")
        lines.append("WARNING: UN-GEOREFERENCED FILES:")
        for name in summary["UnGeoreferencedFiles"]:
            lines.append(f"  - {name}")

    lines.append("=" * 80)
    lines.append("")

    # ---- PER-FILE VERTICAL TABLE ----
    headers = [
        "BIM File",
        "DataType",
        "Georeference Status",
        "SpatialReference",
        "ExteriorShell Extent (XMin)",
        "ExteriorShell Extent (YMin)",
        "ExteriorShell Extent (XMax)",
        "ExteriorShell Extent (YMax)",
        "ExteriorShell Extent (ZMin)",
        "ExteriorShell Extent (ZMax)",
    ]

    for item in results:
        extent = item.get("ExteriorShellExtent") or {}

        values = {
            "BIM File": item.get("Name"),
            "DataType": item.get("DataType"),
            "Georeference Status": item.get("GeoreferenceStatus"),
            "SpatialReference": extent.get("SpatialReference"),
            "ExteriorShell Extent (XMin)": extent.get("XMin"),
            "ExteriorShell Extent (YMin)": extent.get("YMin"),
            "ExteriorShell Extent (XMax)": extent.get("XMax"),
            "ExteriorShell Extent (YMax)": extent.get("YMax"),
            "ExteriorShell Extent (ZMin)": extent.get("ZMin"),
            "ExteriorShell Extent (ZMax)": extent.get("ZMax"),
        }

        lines.append("-" * 80)
        for h in headers:
            lines.append(f"{h:<35}: {values.get(h, 'N/A')}")
        lines.append("-" * 80)
        lines.append("")

    return lines


# Print results to console
# Ensure something is always written even if no BIM files are found
if not results:
    output_lines = [
        "=" * 40,
        "BIM FILES REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Workspace: {workspace}",
        "No BIM (.rvt / .ifc) files found.",
        "=" * 40,
    ]
else:
    output_lines = format_results(results)


# Ask user whether to save a text file
save_choice = input("\nWould you like to save the results to a text file? (yes/no): ").strip().lower()

if save_choice in ("yes", "y"):
    # Optionally let user choose a custom path
    custom_path = input(f"Enter output path (or press Enter to use default):\n  [{output_txt}]: ").strip()
    if custom_path:
        output_txt = custom_path

try:
    os.makedirs(os.path.dirname(output_txt), exist_ok=True)

    with open(output_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"\n✅ Report saved to: {output_txt}")

except PermissionError:
    print("\n❌ Permission denied. Try saving to Documents or Desktop.")
except Exception as e:
    print(f"\n❌ Failed to save file: {e}")
