# pragma pylint: disable=missing-docstring

from mobility_pipeline.lib.validate import validate_mobility, \
    validate_mobility_full


def test_validate_mobility_simple_full_valid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'br1', '13853'],
           ['20150201', 'br0', 'br2', '13853']]
    assert validate_mobility(csv) is None


def test_validate_mobility_simple_missing_row_valid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'br2', '13853'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is None


def test_validate_mobility_simple_malformed_ori_1_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0a', 'br2', '13853'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_simple_malformed_ori_2_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'bra0', 'br2', '13853'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_simple_malformed_dst_1_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'br2a', '13853'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_simple_malformed_dst_2_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'bra2', '13853'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_simple_malformed_count_1_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'br2', 'a13853'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_simple_malformed_count_2_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'br2', '138a53'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_simple_malformed_count_3_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'br2', '13853a'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_simple_negative_count_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'br2', '-13853'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_simple_unordered_1_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'br4', '13853'],
           ['20150201', 'br0', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_simple_unordered_2_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br2', 'br2', '13853'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_simple_unordered_3_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility(csv) is not None


def test_validate_mobility_full_simple_missing_row_invalid():
    csv = [['20150201', 'br0', 'br0', '13853'],
           ['20150201', 'br0', 'br2', '13853'],
           ['20150201', 'br1', 'br3', '13853']]
    assert validate_mobility_full(csv) is not None
