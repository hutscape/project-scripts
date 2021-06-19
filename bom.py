# run from parent folder:
# $ python scripts/bom.py hardware/*.xml _data/bill_of_materials.csv
import kicad_netlist_reader
import csv
import sys

net = kicad_netlist_reader.netlist(sys.argv[1])

try:
    f = open(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

out = csv.writer(f, lineterminator='\n', delimiter=',',
                 quotechar='\"', quoting=csv.QUOTE_ALL)


def get_datasheet(datasheet):
    if datasheet == "~":
        return None

    return datasheet


# Write CSV
out.writerow([
    'Designator',  # E.g. U1, R1
    'Value',  # E.g. 10k, 0.1uF
    'Qty',  # Quantity of each part
    'Package',  # E.g. SMD, 0805, SOT-23-5
    'Category',  # E.g. Electronics, Connector, Mechanical, PCB
    'Stock',  # Internal stock location
    'Manufacturer',  # E.g. Vishay, Muticomp
    'MPN',  # Manufacturer part number
    'Datasheet',  # URL for Datasheet
    'Vendor',  # Name of vendor E.g. Element14, Digikey, RS Components, Mouser
    'Link',  # Vendor link to the exact part
    'Unit',  # Unit price
    'Total',  # Total price
    'MOQ',  # Minimum Order Quantity
    'Description',  # Auto-populated by KiCad
    'DNP'  # Do not populate comma, seperate designators
])

grouped = net.groupComponents()
for group in grouped:
    refs = ""
    dnp = ""

    for component in group:
        refs += component.getRef() + ", "
        c = component

        if c.getField("DNP") == "Yes":
            dnp += c.getRef() + ", "

    out.writerow([
        refs,
        c.getValue(),
        len(group),
        c.getField("Package"),
        c.getField("Category"),
        c.getField("Stock"),
        c.getField("Manufacturer"),
        c.getField("MPN"),
        get_datasheet(c.getDatasheet()),
        c.getField("Vendor"),
        c.getField("Link"),
        c.getField("Unit"),
        c.getField("MOQ"),
        c.getPartName() + ": " + c.getDescription(),
        dnp,
    ])
