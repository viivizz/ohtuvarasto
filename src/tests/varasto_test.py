
"""Varaston testit."""

import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    """Varaston testit."""

    def setUp(self):
        """Luo uuden varaston jokaista testiä varten."""
        self.varasto = Varasto(10)

    def test_virheellinen_tilavuus_nollataan(self):
        """Testaa virheellisen tilavuuden ja nollaa sen."""
        varasto = Varasto(0)
        self.assertEqual(varasto.tilavuus, 0)

    def test_negatiivinen_alkusaldo_nollataan(self):
        """Testaa negatiivisen alkusaldon ja nollaa sen."""
        varasto = Varasto(10, -1)
        self.assertEqual(varasto.saldo, 0)

    def test_liian_suuri_alkusaldo_tayttaa_varaston(self):
        """Testaa liian suuren alkusaldon."""
        varasto = Varasto(10, 12)
        self.assertEqual(varasto.saldo, 10)

    def test_liian_suuri_lisays_tayttaa_varaston(self):
        """Testaa liian suuren lisayksen."""
        self.varasto.lisaa_varastoon(15)
        self.assertEqual(self.varasto.saldo, 10)

    def test_negatiivista_maaraa_ei_lisata(self):
        """Testaa, ettei negatiivista maaraa lisata."""
        self.varasto.lisaa_varastoon(-2)
        self.assertEqual(self.varasto.saldo, 0)

    def test_negatiivinen_otto_palauttaa_nollan(self):
        """Testaa, etta negatiivinen otto palauttaa nollan."""
        saatu = self.varasto.ota_varastosta(-2)
        self.assertEqual(saatu, 0)
        self.assertEqual(self.varasto.saldo, 0)

    def test_merkkijonoesitys(self):
        """Testaa varaston merkkijonoesityksen."""
        self.assertEqual(str(self.varasto), "saldo = 0, vielä tilaa 10")

    def test_liian_suuri_otto_tyhjentaa_varaston(self):
        """Testaa, etta liian suuri otto tyhjentaa varaston."""
        self.varasto.lisaa_varastoon(5)
        saatu = self.varasto.ota_varastosta(8)
        self.assertEqual(saatu, 5)
        self.assertEqual(self.varasto.saldo, 0)

    def test_konstruktori_luo_tyhjan_varaston(self):
        """Testaa, etta konstruktori luo tyhjan varaston."""
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        """Testaa uuden varaston tilavuuden."""
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        """Testaa, etta lisays kasvattaa saldoa."""
        self.varasto.lisaa_varastoon(8)
        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        """Testaa, etta lisays pienentää vapaata tilaa."""
        self.varasto.lisaa_varastoon(8)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        """Testaa, etta otto palauttaa oikean maaran."""
        self.varasto.lisaa_varastoon(8)
        saatu_maara = self.varasto.ota_varastosta(2)
        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        """Testaa, etta ottaminen lisaa tilaa."""
        self.varasto.lisaa_varastoon(8)
        self.varasto.ota_varastosta(2)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)
