"""Regression tests for the existing mixture-classification behavior."""

import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

import pandas as pd
import yaml


if importlib.util.find_spec("streamlit") is None:
    sys.modules["streamlit"] = SimpleNamespace()

from calculations import (  # noqa: E402
    calculate_carc,
    calculate_masses,
    calculate_masses_with_hazards,
    calculate_oral_acute_toxicity,
    cas_verifier,
    get_H_statements,
    h_statements,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
with (PROJECT_ROOT / "data" / "limits.yaml").open(encoding="utf-8") as file:
    LIMITS = yaml.safe_load(file)


class MassCalculationTests(unittest.TestCase):
    def test_percentage_is_filled_with_water(self):
        result = calculate_masses([{"name": "Ingredient", "percentage": 25.0}])

        self.assertAlmostEqual(result[0]["mass"], 250.0)
        self.assertAlmostEqual(result[0]["percentage"], 25.0)
        self.assertEqual(result[-1]["name"], "water")
        self.assertAlmostEqual(result[-1]["percentage"], 75.0)

    def test_concentrations_are_converted_to_mass(self):
        cases = [
            ({"M": 1.0, "molarmass": 40.0}, 40.0),
            ({"mM": 100.0, "molarmass": 40.0}, 4.0),
        ]
        for amount, expected_mass in cases:
            with self.subTest(amount=amount):
                result = calculate_masses([{"name": "Ingredient", **amount}])
                self.assertAlmostEqual(result[0]["mass"], expected_mass)

    def test_current_component_can_fill_remaining_mass(self):
        result = calculate_masses_with_hazards(
            [
                {"name": "Ingredient", "percentage": 20.0},
                {"name": "Filler"},
            ]
        )

        self.assertAlmostEqual(result[-1]["percentage"], 80.0)
        self.assertAlmostEqual(
            sum(component["percentage"] for component in result), 100.0
        )


class ClassificationTests(unittest.TestCase):
    def test_valid_and_invalid_cas_numbers(self):
        self.assertTrue(cas_verifier("64-17-5"))
        self.assertTrue(cas_verifier("7732-18-5"))
        self.assertFalse(cas_verifier("64-17-6"))

    def test_carcinogenicity_cutoff_boundary(self):
        cutoff = LIMITS["carc_limits"]["1A"]

        self.assertEqual(
            calculate_carc(
                [{"Carcinogenicity": "1A", "percentage": cutoff}], LIMITS
            ),
            "1A",
        )
        self.assertIsNone(
            calculate_carc(
                [{"Carcinogenicity": "1A", "percentage": cutoff - 0.001}],
                LIMITS,
            )
        )

    def test_oral_acute_toxicity_category(self):
        component = {"Acute Toxicity (Oral)": "3", "percentage": 100.0}

        self.assertEqual(calculate_oral_acute_toxicity([component], LIMITS), 3)

    def test_h_statement_data_matches_calculated_code(self):
        hazard_data = pd.read_csv(
            PROJECT_ROOT / "data" / "hazard_data.csv", delimiter=";"
        )
        hazards = [
            None,
            None,
            None,
            None,
            None,
            3,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        codes = h_statements(hazards)
        hazard_numbers, statements, _, signal_words = get_H_statements(
            codes, [], {}, hazard_data
        )

        self.assertEqual(hazard_numbers, ["H301"])
        self.assertEqual(statements, ["Toxic if swallowed"])
        self.assertEqual(signal_words, ["Danger"])


if __name__ == "__main__":
    unittest.main()
