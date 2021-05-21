import csv
import sys
import json

filename = sys.argv[1]
uniq_items = 0
total_items = 0
total_items_dnp = 0
grand_total_cost = 0.0
vendor_list = []
uniq_vendor_list = []
total_vendors = 0


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


with open(filename, 'r') as csv_file:
  reader = csv.reader(csv_file)
  next(reader, None)  # skip the headers

  for row in reader:
    uniq_items += 1
    total_items = int(row[2], base=10) + total_items

    if row[15] != "":  # if DNP is valid
      total_items_dnp += row[15].count(",") + 1

    grand_total_cost += float(row[12])

    if row[9] != "":
      vendor_list.append(str(row[9]))

    uniq_vendor_list = get_uniq_vendor_names(vendor_list)
    total_vendors = len(uniq_vendor_list)

print("\nUniq Items:")
print(uniq_items)
print("Total Items:")
print(total_items)
print("Total Items to populate:")
print(total_items - total_items_dnp)
print("Total cost: $")
print(round(grand_total_cost, 2))
print("Vendor list:")
print(vendor_list)
print("Uniq vendor list:")
print(uniq_vendor_list)
print("Unique vendors:")
print(total_vendors)

# Calculate BOM analytics
data = {}
data['bom-uniq'] = uniq_items
data['bom-total'] = total_items
data['bom-total-populate'] = total_items - total_items_dnp
data['bom-cost'] = round(grand_total_cost, 2)
data['vendor-names'] = uniq_vendor_list
data['vendors'] = total_vendors

with open('_data/bom.json', 'w') as outfile:
    json.dump(data, outfile, indent=2)
