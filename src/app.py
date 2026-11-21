"""Simple Flask web interface for managing warehouses."""

from importlib import import_module

from flask import Flask, flash, redirect, render_template, request, url_for

try:
    Varasto = import_module("src.varasto").Varasto
except ModuleNotFoundError:
    Varasto = import_module("varasto").Varasto

# pylint: disable=too-many-statements


app = Flask(__name__)
app.config["SECRET_KEY"] = "development-only"

warehouses = {}


def parse_positive_amount(value):
    """Parse a positive numeric amount, or return None for invalid input."""
    try:
        amount = float(value)
    except (TypeError, ValueError):
        return None
    if amount <= 0:
        return None
    return amount


@app.route("/", methods=["GET"])
def index():
    """Show warehouse creation form and all warehouses."""
    return render_template("index.html", warehouses=warehouses)


@app.route("/warehouses", methods=["POST"])
def create_warehouse():
    """Create a new warehouse."""
    name = request.form.get("name", "").strip()
    capacity = parse_positive_amount(request.form.get("capacity"))

    if not name:
        flash("Warehouse name is required.")
        return redirect(url_for("index"))
    if capacity is None:
        flash("Maximum capacity must be a positive number.")
        return redirect(url_for("index"))

    warehouse_id = max(warehouses, default=0) + 1
    warehouses[warehouse_id] = {
        "name": name,
        "stock": Varasto(capacity),
    }
    flash(f'Warehouse "{name}" created.')
    return redirect(url_for("index"))


@app.route("/warehouses/<int:warehouse_id>/add", methods=["POST"])
def add_items(warehouse_id):
    """Add items to a selected warehouse."""
    warehouse = warehouses.get(warehouse_id)
    if warehouse is None:
        return "Warehouse not found.", 404

    amount = parse_positive_amount(request.form.get("amount"))
    if amount is None:
        flash("Amount to add must be a positive number.")
        return redirect(url_for("index"))

    stock = warehouse["stock"]
    if amount > stock.paljonko_mahtuu():
        flash("Cannot add items beyond the warehouse's maximum capacity.")
        return redirect(url_for("index"))

    stock.lisaa_varastoon(amount)
    flash(f'Added {amount:g} items to "{warehouse["name"]}".')
    return redirect(url_for("index"))


@app.route("/warehouses/<int:warehouse_id>/remove", methods=["POST"])
def remove_items(warehouse_id):
    """Remove items from a selected warehouse."""
    warehouse = warehouses.get(warehouse_id)
    if warehouse is None:
        return "Warehouse not found.", 404

    amount = parse_positive_amount(request.form.get("amount"))
    if amount is None:
        flash("Amount to remove must be a positive number.")
        return redirect(url_for("index"))

    stock = warehouse["stock"]
    if amount > stock.saldo:
        flash("Cannot remove more items than are currently in stock.")
        return redirect(url_for("index"))

    stock.ota_varastosta(amount)
    flash(f'Removed {amount:g} items from "{warehouse["name"]}".')
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
