"""Tests for the Flask warehouse interface."""

import importlib
import os
import unittest
from unittest.mock import patch

import app


class TestWarehouseWebInterface(unittest.TestCase):
    """Test warehouse creation and stock operations."""

    def setUp(self):
        app.app.config.update(TESTING=True)
        app.warehouses.clear()
        self.client = app.app.test_client()

    def create_warehouse(self, name="Main", capacity="100"):
        """Create a warehouse through the web interface."""
        return self.client.post(
            "/warehouses",
            data={"name": name, "capacity": capacity},
            follow_redirects=True,
        )

    def test_create_multiple_warehouses(self):
        """Multiple named warehouses can be created."""
        self.create_warehouse("Main", "100")
        response = self.create_warehouse("Cold storage", "50")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(app.warehouses), 2)
        self.assertIn(b"Main", response.data)
        self.assertIn(b"Cold storage", response.data)

    def test_create_requires_name_and_positive_capacity(self):
        """Invalid warehouse details show clear errors."""
        response = self.create_warehouse("", "100")
        self.assertIn(b"Warehouse name is required", response.data)

        response = self.create_warehouse("Main", "-1")
        self.assertIn(
            b"Maximum capacity must be a positive number",
            response.data,
        )

    def test_secret_key_comes_from_environment(self):
        """Configured secret keys override the generated development key."""
        with patch.dict(os.environ, {"SECRET_KEY": "test-secret"}):
            importlib.reload(app)
            self.assertEqual(app.app.config["SECRET_KEY"], "test-secret")
        importlib.reload(app)

    def test_add_items_updates_stock(self):
        """Items can be added to an existing warehouse."""
        self.create_warehouse()

        response = self.client.post(
            "/warehouses/1/add",
            data={"amount": "30"},
            follow_redirects=True,
        )

        self.assertEqual(app.warehouses[1]["stock"].saldo, 30)
        self.assertIn(b"Current stock: 30", response.data)

    def test_add_cannot_exceed_capacity(self):
        """Adding beyond capacity shows an error and does not change stock."""
        self.create_warehouse("Small", "10")

        response = self.client.post(
            "/warehouses/1/add",
            data={"amount": "11"},
            follow_redirects=True,
        )

        self.assertEqual(app.warehouses[1]["stock"].saldo, 0)
        self.assertIn(
            b"Cannot add items beyond the warehouse&#39;s maximum capacity",
            response.data,
        )

    def test_remove_items_updates_stock(self):
        """Items can be removed from an existing warehouse."""
        self.create_warehouse()
        self.client.post("/warehouses/1/add", data={"amount": "30"})

        response = self.client.post(
            "/warehouses/1/remove",
            data={"amount": "12"},
            follow_redirects=True,
        )

        self.assertEqual(app.warehouses[1]["stock"].saldo, 18)
        self.assertIn(b"Current stock: 18", response.data)

    def test_remove_cannot_exceed_stock(self):
        """Removing more stock than exists shows an error."""
        self.create_warehouse()
        self.client.post("/warehouses/1/add", data={"amount": "5"})

        response = self.client.post(
            "/warehouses/1/remove",
            data={"amount": "6"},
            follow_redirects=True,
        )

        self.assertEqual(app.warehouses[1]["stock"].saldo, 5)
        self.assertIn(
            b"Cannot remove more items than are currently in stock",
            response.data,
        )


if __name__ == "__main__":
    unittest.main()
