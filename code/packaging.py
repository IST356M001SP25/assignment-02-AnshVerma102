'''
Module for parsing packaging data
'''

def parse_packaging(packaging_data: str) -> list[dict]:
    '''
    This function parses a string of packaging data and returns a list of dictionaries.
    The order of the list implies the order of the packaging data (inner to outer units).

    Examples:

    input: "12 eggs in 1 carton"
    output: [{ 'eggs': 12}, { 'carton': 1}]

    input: "6 bars in 1 pack / 12 packs in 1 carton"
    output: [{ 'bars': 6}, { 'packs': 12}, { 'carton': 1}]

    input: "20 pieces in 1 pack / 10 packs in 1 carton / 4 cartons in 1 box"
    output: [{ 'pieces': 20}, { 'packs': 10}, { 'cartons': 4}, { 'box': 1}]
    '''
    package = []
    # split into segments and strip whitespace
    segments = [seg.strip() for seg in packaging_data.split('/') if seg.strip()]

    # parse each segment for inner quantity/unit and keep track of outermost
    outer_qty = None
    outer_unit = None
    for seg in segments:
        parts = seg.split()
        if len(parts) < 5 or parts[2].lower() != 'in':
            raise ValueError(f"Invalid packaging segment: '{seg}'")
        # unpack: qty, unit, 'in', parent_qty, parent_unit
        qty, unit, _, parent_qty, parent_unit = parts[:5]
        package.append({unit: int(qty)})
        outer_qty = int(parent_qty)
        outer_unit = parent_unit

    # append the outermost packaging level
    if outer_unit is not None:
        package.append({outer_unit: outer_qty})

    return package


def calc_total_units(package: list[dict]) -> int:
    '''
    This function calculates the total number of items in a package.

    Example:

    input: [{ 'bars': 6}, {'packs': 12}, {'carton': 1}]
    output: 72 (6 * 12 * 1)

    input: [{ 'pieces': 20}, {'packs': 10}, {'cartons': 4}, {'box': 1}]
    output: 800 (20 * 10 * 4 * 1)
    '''
    total = 1
    for item in package:
        total *= list(item.values())[0]
    return total


def get_unit(package: list[dict]) -> str:
    '''
    This function returns the base item in the packaging (first element in the list).

    Examples:

    input: [{ 'bars': 6}, {'packs': 12}, {'carton': 1}]
    output: 'bars'

    input: [{ 'pieces': 20}, {'packs': 10}, {'cartons': 4}, {'box': 1}]
    output: 'pieces'
    '''
    if not package:
        raise ValueError("Package list is empty")
    return next(iter(package[0].keys()))


if __name__ == '__main__':
    text = "25 balls in 1 bucket / 4 buckets in 1 bin"
    package = parse_packaging(text)
    print(package)

    package_total = calc_total_units(package)
    unit = get_unit(package)
    print(f"{package_total} {unit} total")
