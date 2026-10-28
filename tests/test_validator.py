import pytest

from src.validator import OrderValidator


@pytest.mark.parametrize("symbol", ["BTCUSDT", "ethusdt", "1000PEPEUSDT"])
def test_valid_symbols(symbol):
    assert OrderValidator.validate_symbol(symbol)


@pytest.mark.parametrize("symbol", ["", None, "BTCBUSD", "BTC-USDT", "USDTBTC", 123])
def test_invalid_symbols(symbol):
    assert not OrderValidator.validate_symbol(symbol)


@pytest.mark.parametrize("quantity", [0.002, 1, "0.5", "100"])
def test_valid_quantities(quantity):
    assert OrderValidator.validate_quantity(quantity)


@pytest.mark.parametrize("quantity", [0, -1, "-0.1", "abc", None, ""])
def test_invalid_quantities(quantity):
    assert not OrderValidator.validate_quantity(quantity)


@pytest.mark.parametrize("price", [55000.0, 1, "0.0001"])
def test_valid_prices(price):
    assert OrderValidator.validate_price(price)


@pytest.mark.parametrize("price", [0, -100, "nan-price", None])
def test_invalid_prices(price):
    assert not OrderValidator.validate_price(price)


@pytest.mark.parametrize("side", ["BUY", "SELL", "buy", "Sell"])
def test_valid_sides(side):
    assert OrderValidator.validate_side(side)


@pytest.mark.parametrize("side", ["HOLD", "", "LONG"])
def test_invalid_sides(side):
    assert not OrderValidator.validate_side(side)


@pytest.mark.parametrize("tif", ["GTC", "IOC", "FOK", "gtc"])
def test_valid_time_in_force(tif):
    assert OrderValidator.validate_time_in_force(tif)


@pytest.mark.parametrize("tif", ["GTX", "DAY", ""])
def test_invalid_time_in_force(tif):
    assert not OrderValidator.validate_time_in_force(tif)


@pytest.mark.parametrize("order_type", ["MARKET", "limit", "STOP_MARKET"])
def test_valid_order_types(order_type):
    assert OrderValidator.validate_order_type(order_type)


def test_invalid_order_type():
    assert not OrderValidator.validate_order_type("ICEBERG")
