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

out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

out.writerow([
    'Designator',
    'Value',
    'Q',
    'Package',
    'Category',
    'Stock',
    'Manufacturer',
    'MPN',
    'Datasheet',
    'Vendor',
    'Link',
    'Unit',
    'Total',
    'MOQ',
    'Description'
])

grand_total_cost = 0.0
total_items = 0
uniq_items = 0

def total_cost(unit_cost, quantity):
    if not unit_cost:
        return 0

    return float(unit_cost) * int(quantity)

grouped = net.groupComponents()
for group in grouped:
    refs = ""

    for component in group:
        refs += component.getRef() + ", "
        c = component

    out.writerow([
        refs,
        c.getValue(),
        len(group),
        c.getField("Package"),
        c.getField("Category"),
        c.getField("Stock"),
        c.getField("Manufacturer"),
        c.getField("Part No."),
        c.getDatasheet(),
        c.getField("Vendor"),
        c.getField("Vendor link"),
        c.getField("Unit cost"),
        total_cost(c.getField("Unit cost"), len(group)),
        c.getField("Minimum Order"),
        c.getPartName() + ": " + c.getDescription()
    ])

with open('_data/bom.json', 'w') as outfile:
    json.dump(data, outfile, indent=2)
