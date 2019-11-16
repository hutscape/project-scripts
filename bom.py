import kicad_netlist_reader
import csv
import sys
import json

net = kicad_netlist_reader.netlist(sys.argv[1])

try:
    f = open(sys.argv[2], 'w')
except IOError:
    e = "Can't open output file for writing: " + sys.argv[2]
    print(__file__, ":", e, sys.stderr)
    f = sys.stdout

out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)

grand_total_cost = 0.0
total_items = 0
total_items_populate = 0
uniq_items = 0
vendor_names = []

def total_cost(unit_cost, quantity):
    if not unit_cost:
        return 0

    return float("{0:.2f}".format(float(unit_cost) * int(quantity)))

def is_valid_vendor_name(vendor_name):
    if "stock" not in vendor_name.lower():
        if "dnp" not in vendor_name.lower():
            return True

    return False

def get_uniq_vendor_names(vendors):
    uniq_vendors = []

    for each_vendor in vendors:
        if is_valid_vendor_name(each_vendor):
            if each_vendor not in uniq_vendors and each_vendor:
                uniq_vendors.append(each_vendor)

    return uniq_vendors

def get_datasheet(datasheet):
    if datasheet == "~":
        return None

    return datasheet

# Write CSV
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
    'Description',
    'DNP'
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

    uniq_items += 1
    total_items += len(group)
    grand_total_cost += total_cost(c.getField("Unit cost"), len(group))
    vendor_names.append(c.getField("Vendor"))

    if not c.getField("DNP"):
        total_items_populate += len(group)

    out.writerow([
        refs,
        c.getValue(),
        len(group),
        c.getField("Package"),
        c.getField("Category"),
        c.getField("Stock No."),
        c.getField("Manufacturer"),
        c.getField("Part No."),
        get_datasheet(c.getDatasheet()),
        c.getField("Vendor"),
        c.getField("Vendor link"),
        c.getField("Unit cost"),
        total_cost(c.getField("Unit cost"), len(group)),
        c.getField("Minimum Order"),
        c.getPartName() + ": " + c.getDescription(),
        dnp,
    ])

# Calculate BOM analytics
data = {}
data['bom-uniq'] = uniq_items
data['bom-total'] = total_items
data['bom-total-populate'] = total_items_populate
data['bom-cost'] = grand_total_cost
data['vendors'] = len(get_uniq_vendor_names(vendor_names))
data['vendor-names'] = get_uniq_vendor_names(vendor_names)

with open('_data/bom.json', 'w') as outfile:
    json.dump(data, outfile, indent=2)
