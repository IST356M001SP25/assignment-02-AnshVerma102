'''
This is the main program. 
You should read the packaging.txt in the data folder.
Each line contains one package description. 
You should parse the package description using parse_packaging()
print the total number of items in the package using calc_total_units()
along with the unit using get_unit()
place each package in a list and save in JSON format.

Example:

    INPUT (example data/packaging.txt file):
    
    12 eggs in 1 carton
    6 bars in 1 pack / 12 packs in 1 carton

    OUTPUT: (print to console)

    12 eggs in 1 carton => total units: 12 eggs
    6 bars in 1 pack / 12 packs in 1 carton => total units: 72 bars

    OUTPUT (example data/packaging.json file):
    [
        [{ 'eggs' : 12}, {'carton' : 1}],
        [{ 'bars' : 6}, {'packs' : 12}, {'carton' : 1}],
    ]    
'''

import json
from pathlib import Path
from packaging import parse_packaging, calc_total_units, get_unit


def main():
    data_path = Path('data/packaging.txt')
    if not data_path.exists():
        print(f"File not found: {data_path}")
        return

    packages = []
    # Read and strip lines, skip empty ones
    lines = [line.strip() for line in data_path.read_text().splitlines() if line.strip()]

    for line in lines:
        try:
            package = parse_packaging(line)
            total_units = calc_total_units(package)
            unit = get_unit(package)
            print(f"{line} => total units: {total_units} {unit}")
            packages.append(package)
        except Exception as e:
            print(f"Skipping invalid line: '{line}' ({e})")

    # Write output JSON once
    out_path = Path('data/packaging.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(packages, indent=4))
    print(f"Saved {len(packages)} package(s) to {out_path}")


if __name__ == '__main__':
    main()
