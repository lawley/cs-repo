# Maintain a FHIR CodeSystem based on Tabular Data

### Overview
This program allows you to update an existing FHIR CodeSystem (in FSH format) using tabular data.
FSH is used because it is more firendly for source control (Git) than JSON or XML.

Here's how it works:
1. It reads an existing FSH file containing a CodeSystem
2. Loads your tabular data (CSV, TSV, or Excel spreadsheet)
3. Uses a JSON configuration to map columns to FHIR CodeSystem elements
4. Updates the CodeSystem, marking missing codes as inactive
Saves the updated CodeSystem to a new or existing FSH file

### Usage
```bash
python genfsh.py --fsh initial_codesystem.fsh --data codes.csv --config config.json --output codesystem.fsh
```
### Configuration Format
Your JSON configuration file should look something like this:

```json
{
  "codeColumn": "code",
  "displayColumn": "display",
  "definitionColumn": "definition",
  "additionalDisplays": [
    {
      "column": "display_es",
      "language": "es",
      "use": "display",
      "separator": ";"
    },
    {
      "column": "display_fr",
      "language": "fr",
      "use": "http://example.com/Uses#translation"
    }
  ],
  "propertyMappings": {
    "cs_property": "csv_property_column",
    "normalizedCode": "normalized_code",
    "category": "category_column"
  }
}
```
### Features
The program handles:

* Multiple column-to-property mappings
* Additional displays as properties
* Maintaining existing codes (marking them inactive if not in the new data)
* Preserving metadata from the original CodeSystem
* Handles updating the input file (same input and output:
  `--fsh cs.fsh --output cs.fsh`)

### FSH
The program uses the [FSH](https://fshschool.org/) format for FHIR resources.

If you don't have your initial CodeSystem in FSH format, you can use [GoFSH](https://github.com/FHIR/GoFSH) to convert it.
