import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def to_whole_number(text):
    try:
        return int(text.strip())
    except ValueError:
        return None


def check_columns(reader, needed, file_name):
    if reader.fieldnames is None or not set(needed).issubset(reader.fieldnames):
        raise ValueError(file_name + " must have the columns: " + ", ".join(needed))


def load_inventory(path):
    stock = {}
    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        check_columns(reader, ["sku", "name", "quantity"], "Inventory file")

        for row_number, row in enumerate(reader, start=2):
            sku = (row.get("sku") or "").strip()
            name = (row.get("name") or "").strip()
            quantity = to_whole_number(row.get("quantity") or "")

            if sku == "":
                raise ValueError("Inventory row " + str(row_number) + ": missing SKU")
            if sku in stock:
                raise ValueError("Inventory row " + str(row_number) + ": duplicate SKU " + sku)
            if quantity is None or quantity < 0:
                raise ValueError("Inventory row " + str(row_number) + ": quantity must be zero or more")

            stock[sku] = {"name": name, "quantity": quantity}

    return stock


def apply_movements(stock, path):
    rejected = []

    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        check_columns(reader, ["sku", "type", "units"], "Movements file")

        for row_number, row in enumerate(reader, start=2):
            sku = (row.get("sku") or "").strip()
            raw_type = (row.get("type") or "").strip()
            raw_units = (row.get("units") or "").strip()
            movement_type = raw_type.upper()
            units = to_whole_number(raw_units)

            reason = None
            if sku not in stock:
                reason = "unknown SKU"
            elif movement_type not in ("IN", "OUT"):
                reason = "invalid movement type"
            elif units is None:
                reason = "units is not a whole number"
            elif units <= 0:
                reason = "units must be greater than zero"
            elif movement_type == "OUT" and units > stock[sku]["quantity"]:
                reason = "not enough stock for this OUT movement"

            if reason is not None:
                rejected.append({
                    "row": row_number,
                    "sku": sku,
                    "type": raw_type,
                    "units": raw_units,
                    "reason": reason,
                })
            elif movement_type == "IN":
                stock[sku]["quantity"] += units
            else:
                stock[sku]["quantity"] -= units

    return rejected


def write_inventory(path, stock):
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["sku", "name", "quantity"])
        for sku, item in stock.items():
            writer.writerow([sku, item["name"], item["quantity"]])


def write_rejected(path, rejected):
    with open(path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["row", "sku", "type", "units", "reason"])
        for item in rejected:
            writer.writerow([item["row"], item["sku"], item["type"], item["units"], item["reason"]])


def reconcile(inventory_path, movements_path, updated_path, rejected_path):
    stock = load_inventory(inventory_path)
    rejected = apply_movements(stock, movements_path)
    write_inventory(updated_path, stock)
    write_rejected(rejected_path, rejected)
    return stock, rejected


def create_sample_files(folder):
    inventory_rows = [
        ["sku", "name", "quantity"],
        ["P01", "Widget", 10],
        ["P02", "Gadget", 5],
        ["P03", "Bolt", 0],
    ]
    movement_rows = [
        ["sku", "type", "units"],
        ["P01", "OUT", 4],
        ["P01", "OUT", 9],
        ["P01", "IN", 2],
        ["P02", "IN", 3],
        ["X99", "IN", 5],
        ["P02", "OUT", 0],
        ["P03", "IN", -2],
        ["P02", "SELL", 1],
        ["P03", "IN", "many"],
        ["P03", "in", 6],
    ]
    for file_name, rows in (("inventory.csv", inventory_rows), ("movements.csv", movement_rows)):
        with open(os.path.join(folder, file_name), "w", newline="", encoding="utf-8") as csv_file:
            csv.writer(csv_file).writerows(rows)


if __name__ == "__main__":
    create_sample_files(HERE)

    stock, rejected = reconcile(
        os.path.join(HERE, "inventory.csv"),
        os.path.join(HERE, "movements.csv"),
        os.path.join(HERE, "updated_inventory.csv"),
        os.path.join(HERE, "rejected_movements.csv"),
    )

    print("Updated inventory:")
    for sku, item in stock.items():
        print(" ", sku, item["name"], item["quantity"])

    print()
    print("Rejected movements:")
    for item in rejected:
        print("  row", item["row"], "|", item["sku"], item["type"], item["units"], "->", item["reason"])

    print()
    print("Files written: updated_inventory.csv, rejected_movements.csv")
