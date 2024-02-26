import numpy as np
import polars as pl
import pytest

from syn_data_fidelity.counting import _is_not_none_or_nan
from syn_data_fidelity.counting import normalize_count
from syn_data_fidelity.counting import normalize_count_bivariate
from syn_data_fidelity.counting import harmonize_categorical_probabilities
from syn_data_fidelity.counting import _probabilities_safe_as_denominator
from syn_data_fidelity.counting import contingency_table

import sys


@pytest.mark.parametrize("value", [None, np.nan])
def test_is_not_none_or_nan_with_null(value):
    assert not _is_not_none_or_nan(value)


@pytest.mark.parametrize("value", ["x", 0, 1, "abc"])
def test_is_not_none_or_nan_with_value(value):
    assert _is_not_none_or_nan(value)


list_items_single = ["a"]


@pytest.mark.parametrize(
    "column",
    [list_items_single, np.array(list_items_single), pl.Series(list_items_single)],
)
def test_normalize_count_single_str(column):
    assert normalize_count(column) == {list_items_single[0]: 1.0}


@pytest.mark.parametrize(
    "column",
    [
        [],
        np.array([]),
        pl.Series([]),
        [None],
        np.array([None]),
        pl.Series([None]),
        [np.nan],
        np.array([np.nan]),
        pl.Series([np.nan]),
    ],
)
def test_normalize_count_empty(column):
    with pytest.raises(AssertionError) as exc_info:
        normalize_count(column)
    assert exc_info.type == AssertionError


list_items_numbers = [1]


@pytest.mark.parametrize(
    "column",
    [list_items_numbers, np.array(list_items_numbers), pl.Series(list_items_numbers)],
)
def test_normalize_count_single_number(column):
    assert normalize_count(column) == {list_items_numbers[0]: 1.0}


list_two_items = ["a", "b"]


@pytest.mark.parametrize(
    "column",
    [
        list_two_items,
        np.array(list_two_items),
        pl.Series(list_two_items),
        list_two_items + list_two_items,
        np.array(list_two_items + list_two_items),
        pl.Series(list_two_items + list_two_items),
    ],
)
def test_normalize_count_balanced_categories(column):
    assert normalize_count(column) == {k: 0.5 for k in list_two_items}


list_items_inbalanced = ["a", "b", "b", "b"]


@pytest.mark.parametrize(
    "column",
    [
        list_items_inbalanced,
        np.array(list_items_inbalanced),
        pl.Series(list_items_inbalanced),
    ],
)
def test_normalize_count_inbalanced_categories(column):
    assert normalize_count(column) == {"a": 0.25, "b": 0.75}


list_items_nan = ["a", np.nan, "b", "b", "b", None]


@pytest.mark.parametrize(
    "column", [list_items_nan, np.array(list_items_nan), pl.Series(list_items_nan)]
)
def test_normalize_count_with_nan(column):
    assert normalize_count(column) == {"a": 0.25, "b": 0.75}


def test_normalize_count_bivariate_single_entry():
    assert normalize_count_bivariate(["a"], ["b"]) == {
        (
            "a",
            "b",
        ): 1.0
    }


@pytest.mark.parametrize(
    "column",
    [
        [],
        np.array([]),
        pl.Series([]),
        [None],
        np.array([None]),
        pl.Series([None]),
        [np.nan],
        np.array([np.nan]),
        pl.Series([np.nan]),
    ],
)
def test_normalize_count_empty(column):
    with pytest.raises(AssertionError) as exc_info:
        normalize_count(column)
    assert exc_info.type == AssertionError


list_items_without_nan_1 = ["a", "b", "b", "b"]
list_items_without_nan_2 = ["x", "y", "y", "y"]


@pytest.mark.parametrize(
    "column_1, column_2",
    [
        (
            list_items_without_nan_1,
            list_items_without_nan_2,
        ),
        (
            np.array(list_items_without_nan_1),
            np.array(list_items_without_nan_2),
        ),
        (pl.Series(list_items_without_nan_1), pl.Series(list_items_without_nan_2)),
        (
            np.array(list_items_without_nan_1),
            list_items_without_nan_2,
        ),
        (
            list_items_without_nan_1,
            np.array(list_items_without_nan_2),
        ),
        (list_items_without_nan_1, pl.Series(list_items_without_nan_2)),
    ],
)
def test_normalize_count_bivariate_without_nan(column_1, column_2):
    assert normalize_count_bivariate(column_1, column_2) == {
        (
            "a",
            "x",
        ): 0.25,
        (
            "b",
            "y",
        ): 0.75,
    }


def test_normalize_count_bivariate_one_empty():
    col = ["a", "b", "c"]
    with pytest.raises(AssertionError) as exc_info:
        normalize_count_bivariate(col, [])
    assert exc_info.type == AssertionError
    with pytest.raises(AssertionError) as exc_info:
        normalize_count_bivariate([], col)
    assert exc_info.type == AssertionError


list_items_nan_1 = ["a", np.nan, "b", "b", "b", None]
list_items_nan_2 = ["x", np.nan, "y", "y", "y", "y"]


@pytest.mark.parametrize(
    "column_1, column_2",
    [
        (
            list_items_nan_1,
            list_items_nan_2,
        ),
        (
            np.array(list_items_nan_1),
            np.array(list_items_nan_2),
        ),
        (pl.Series(list_items_nan_1), pl.Series(list_items_nan_2)),
        (
            np.array(list_items_nan_1),
            list_items_nan_2,
        ),
        (
            list_items_nan_1,
            np.array(list_items_nan_2),
        ),
        (list_items_nan_1, pl.Series(list_items_nan_2)),
    ],
)
def test_normalize_count_bivariate_with_nan(column_1, column_2):
    assert normalize_count_bivariate(column_1, column_2) == {
        (
            "a",
            "x",
        ): 0.25,
        (
            "b",
            "y",
        ): 0.75,
    }


@pytest.mark.parametrize(
    "ps",
    [
        {"a": 1.0},
        {"a": 1.0, "b": 0.0},
        {"a": 0.5, "b": 0.5},
    ],
)
def test_harmonize_categorical_probabilities_one_empty(ps):
    assert harmonize_categorical_probabilities(ps, {}) == (
        ps,
        {k: 0.0 for k in ps.keys()},
    )
    assert harmonize_categorical_probabilities({}, ps) == (
        {k: 0.0 for k in ps.keys()},
        ps,
    )


@pytest.mark.parametrize(
    "ps",
    [
        {"a": 1.0},
        {"a": 1.0, "b": 0.0},
        {"a": 0.5, "b": 0.5},
    ],
)
def test_harmonize_categorical_probabilities_identicial(ps):
    assert harmonize_categorical_probabilities(ps, ps) == (
        ps,
        ps,
    )


def test_probabilities_safe_as_denominator():
    assert _probabilities_safe_as_denominator(
        {"a": 0, "b": 1.0}, constant=sys.float_info.min
    ) == {"a": sys.float_info.min, "b": 1.0}


def test_probabilities_safe_as_denominator_idenity():
    assert _probabilities_safe_as_denominator({"a": 0.3, "b": 0.7}) == {
        "a": 0.3,
        "b": 0.7,
    }


def test_contingency_table_2x1():
    assert (
        contingency_table(["a", "b"], ["a", "a"]).tolist()
        == np.asarray([[1, 2], [1, 0]]).tolist()
    )


def test_contingency_table_2x2():
    assert (
        contingency_table(["a", "b"], ["x", "y"]).tolist()
        == np.asarray([[1, 0], [1, 0], [0, 1], [0, 1]]).tolist()
    )
