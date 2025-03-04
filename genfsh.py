import argparse
import csv
import json
import os
import pandas as pd
import re
from typing import Dict, List, Optional, Set, Any

class FshCodeSystem:
    """Class to represent and manipulate a FHIR CodeSystem in FSH format."""
    
    def __init__(self, fsh_path: str):
        """Initialize from FSH file."""
        self.fields = ['valueSet']
        self.fsh_path = fsh_path
        self.id = ""
        self.name = ""
        self.title = ""
        self.description = ""
        self.content_mode = ""
        self.status = ""
        self.url = ""
        self.version = ""
        self.elements = {}  # self.fields -> ...
        self.codes = {}  # code -> {display, status, properties, designations}
        self.properties = {}  # name -> {description, type}
        self.extra_metadata = {}
        self.load_fsh()
    
    def load_fsh(self):
        """Load the CodeSystem from FSH file."""
        with open(self.fsh_path, 'r') as file:
            content = file.read()
        
        # Extract CodeSystem name
        name_match = re.search(r'CodeSystem:\s+(\S+)', content)
        if name_match:
            self.name = name_match.group(1)
        
        # Extract basic metadata
        self.id = self._extract_metadata(content, 'Id')
        self.title = self._extract_metadata(content, 'Title')
        self.description = self._extract_metadata(content, 'Description')
        self.content_mode = self._extract_metadata(content, 'content')
        self.status = self._extract_metadata(content, 'status')
        self.url = self._extract_metadata(content, 'url')
        self.version = self._extract_metadata(content, 'version')
        for f in self.fields:
            val = self._extract_metadata(content, f)
            if val:
                self.elements[f] = val

        # Extract properties
        property = None
        property_matches = re.finditer(r'\* \^property\[(.)\]\.(\S+)\s+=\s+(.*)', content)
        for match in property_matches:
            if '=' != match.group(1):
                if property:
                    self.properties[property['code']] = property
                property = {}
            
            property_name = match.group(2)
            property_content = match.group(3)
            
            if 'description' == property_name:
                property[property_name] = property_content
            else:
                property[property_name] = property_content[1:]
        if property:
            self.properties[property['code']] = property


        # Extract codes and their attributes
        code_blocks = re.split(r'\n\*\s+#', content)
        for block in code_blocks[1:]:
            lines = block.split('\n')
            line = block.strip()
            match = re.match(r'(\S+)\s+"([^"]+)"(?:\s+"([^"]+)")?', line)
            if match:
                code, display, definition = match.groups()
                self.codes[code] = {
                    'display': display,
                    'definition': definition if definition else None,
                    'status': 'active',
                    'properties': {},
                    'designations': []
                }
            
            # Extract properties
            prop_match = re.match(r'(\S+)\s+\^property\[(.)\]\.(\S+)\s+=\s+(.+)', line)
            if prop_match:
                prop_code, prop_idx, prop_name, prop_value = prop_match.groups()
                if '=' != prop_idx:
                    pc = None
                    pv = None
                    if not self.codes[prop_code]['properties']:
                        self.codes[prop_code]['properties'] = {}
                    p = self.codes[prop_code]['properties']
                if 'code' == prop_name:
                  pc = prop_value[1:]
                elif 'valueCode' == prop_name:
                  pv = prop_value[1:]
                else:
                  pv = prop_value.strip('"')
                if pc and pv:
                    p[pc] = pv
            
            # Extract designations
            desig_match = re.match(r'(\S+)\s+\^designation\[(.)\]\.(\S+)\s+=\s+(.+)', line)
            if desig_match:
                desig_code, desig_idx, desig_name, desig_value = desig_match.groups()
                if '=' != desig_idx:
                    if '+' == desig_idx:
                      di = di + 1
                    else:
                      di = int(desig_idx)
                    if di >= len(self.codes[desig_code]['designations']):
                        for i in range(len(self.codes[desig_code]['designations']), di+1):
                            self.codes[desig_code]['designations'].append({})
                    d = self.codes[desig_code]['designations'][di]
                if 'use' == desig_name:
                    d[desig_name] = desig_value.strip('#')
                else:
                    d[desig_name] = desig_value.strip('"')


    def _extract_metadata(self, content: str, field: str) -> str:
        """Extract metadata field from FSH content."""
        match = re.search(fr'{field}:\s+(.+)(?:\n|$)', content)
        if match:
            return match.group(1).strip('"')
        match = re.search(fr'\* {field}:\s+(.+)(?:\n|$)', content)
        if match:
            return match.group(1).strip('"')
        return ""
    
    def update_from_tabular(self, data: pd.DataFrame, config: Dict):
        """Update CodeSystem from tabular data based on provided configuration."""
        existing_codes = set(self.codes.keys())
        updated_codes = set()
        
        # Extract configuration
        code_column = config.get('codeColumn', 'code')
        display_column = config.get('displayColumn', 'display')
        definition_column = config.get('definitionColumn')
        additional_displays = config.get('additionalDisplays', [])
        property_mappings = config.get('propertyMappings', {})
        
        # Process each row in the data
        for _, row in data.iterrows():
            code = str(row[code_column])
            updated_codes.add(code)
            
            if code not in self.codes:
                # New code
                self.codes[code] = {
                    'display': row[display_column],
                    'definition': row[definition_column] if definition_column and definition_column in row and isinstance(row[definition_column], str) else None,
                    'status': 'active',
                    'properties': {},
                    'designations': []
                }
            else:
                # Update existing code
                self.codes[code]['display'] = row[display_column]
                if definition_column and definition_column in row:
                    self.codes[code]['definition'] = row[definition_column]
                self.codes[code]['status'] = 'active'
                # clear previous properties and designations
                self.codes[code]['properties'] = {}
                self.codes[code]['designations'] = []
            
            # Update properties
            for prop_name, column_name in property_mappings.items():
                if column_name in row and not pd.isna(row[column_name]):
                    self.codes[code]['properties'][prop_name] = str(row[column_name])
            
            # Add additional displays as designations
            for display_info in additional_displays:
                column_name = display_info.get('column')
                language = display_info.get('language')
                use = display_info.get('use')
                sep = display_info.get('separator')
                
                if column_name and column_name in row and not pd.isna(row[column_name]):
                    value = str(row[column_name])
                    terms = value.split(sep) if sep else [value]
                    for term in terms:
                        designation = {
                            'value': term
                        }
                        if language:
                            designation['language'] = language
                        if use:
                            designation['use'] = use
                    
#                        # Check if this designation already exists
#                        self.codes[code]['designations'] = [d for d in self.codes[code]['designations'] 
#                                                          if not (d.get('language') == designation.get('language') and 
#                                                                  d.get('use') == designation.get('use'))]
                    
                        # Add the new designation
                        self.codes[code]['designations'].append(designation)
        
        # Mark codes as inactive if they're not in the updated data
        for code in existing_codes - updated_codes:
            self.codes[code]['properties']['inactive'] = "true"

    def save_fsh(self, output_path: Optional[str] = None):
        """Save the updated CodeSystem to FSH file."""
        if output_path is None:
            output_path = self.fsh_path
        
        content = []
        
        # Write header
        content.append(f"CodeSystem: {self.name}")
        content.append(f"Id: {self.id}")
        content.append(f"Title: \"{self.title}\"")
        content.append(f"Description: \"{self.description}\"")
        content.append(f"* ^content: {self.content_mode}")
        content.append(f"* ^status: {self.status}")
        content.append(f"* ^url: \"{self.url}\"")
        content.append(f"* ^version: \"{self.version}\"")
        for f, v in self.elements:
            if v:
                content.append(f"* ^{f}: \"{v}\"")
        
        # Write property definitions
        prop_type = {}
        idx = '0'
        for prop_name, prop_info in self.properties.items():
            content.append(f"* ^property[{idx}].code = #{prop_name}")
            content.append(f"* ^property[=].description = {prop_info['description']}")
            content.append(f"* ^property[=].type = #{prop_info['type']}")
            prop_type[prop_name] = prop_info['type']
            idx = '+'
        
        content.append("")
        
        # Write codes
        for code, code_info in sorted(self.codes.items()):
            display = code_info['display']
            definition = code_info['definition']
            
            if definition:
                code_line = f"* #{code} \"{display}\" \"{definition}\""
            else:
                code_line = f"* #{code} \"{display}\""
            
            content.append(code_line)
            
            # Add properties
            idx = '0'
            for prop_name, prop_value in sorted(code_info['properties'].items()):
                type = prop_type[prop_name] if prop_name in prop_type else "string"
                content.append(f"* #{code} ^property[{idx}].code = #{prop_name}")
                content.append(f"* #{code} ^property[=].value{type[:1].upper() + type[1:]} = {self.format_value(prop_value, type)}")
                idx = '+'
            
            # Add designations
            idx = '0'
            for designation in code_info['designations']:
                content.append(f"* #{code} ^designation[{idx}].value = \"{designation['value']}\"")
                if 'language' in designation:
                    content.append(f"* #{code} ^designation[=].language = \"{designation['language']}\"")
                if 'use' in designation:
                    content.append(f"* #{code} ^designation[=].use = {self.format_value(designation['use'], 'Coding')}")
                idx = '+'
        
        # Write to file
        with open(output_path, 'w') as file:
            file.write('\n'.join(content))
            file.write('\n')

    def format_value(self, value, type):
        cases = {
          ('code'): lambda x: f"#{x}",
          ('Coding'): lambda x: x if '#' in x else f"#{x}",
          ('string', 'uri'): lambda x: f"\"{x}\""
        }
        for keys, func in cases.items():
            if type in keys:
                return func(value)

        return value

def load_tabular_data(file_path: str) -> pd.DataFrame:
    """Load tabular data from CSV, TSV, or Excel file."""
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.csv':
        return pd.read_csv(file_path)
    elif file_ext == '.tsv':
        return pd.read_csv(file_path, sep='\t')
    elif file_ext in ['.xls', '.xlsx']:
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_ext}")


def main():
    parser = argparse.ArgumentParser(description='Update FHIR CodeSystem from tabular data')
    parser.add_argument('--fsh', required=True, help='Path to FSH file containing CodeSystem')
    parser.add_argument('--data', required=True, help='Path to tabular data file (CSV, TSV, or Excel)')
    parser.add_argument('--config', required=True, help='Path to JSON config file')
    parser.add_argument('--output', help='Path to output FSH file (defaults to overwriting input)')
    
    args = parser.parse_args()
    
    # Load FSH file
    code_system = FshCodeSystem(args.fsh)
    
    # Load tabular data
    data = load_tabular_data(args.data)
    
    # Load config
    with open(args.config, 'r') as file:
        config = json.load(file)
    
    # Update CodeSystem with tabular data
    code_system.update_from_tabular(data, config)
    
    # Save updated CodeSystem
    code_system.save_fsh(args.output)
    
    print(f"Updated CodeSystem saved to {args.output or args.fsh}")


if __name__ == "__main__":
    main()

