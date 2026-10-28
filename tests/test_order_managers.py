from unittest.mock import MagicMock, patch

import pytest
from binance.exceptions import BinanceAPIException

from src.limit_orders import LimitOrderManager
from src.market_orders import MarketOrderManager


@pytest.fixture
def market_manager():
    with patch('src.market_orders.Client') as client_cls:
        client_cls.return_value.futures_create_order.return_value = {'orderId': 42}
        yield MarketOrderManager()


@pytest.fixture
def limit_manager():
    with patch('src.limit_orders.Client') as client_cls:
        client_cls.return_value.futures_create_order.return_value = {'orderId': 7}
        yield LimitOrderManager()


def test_market_order_success(market_manager):
    result = market_manager.place_market_order('btcusdt', 'buy', 0.002)

    assert result['success'] is True
    assert result['order']['orderId'] == 42
    market_manager.client.futures_create_order.assert_called_once_with(
        symbol='BTCUSDT', side='BUY', type='MARKET', quantity=0.002
    )


def test_market_order_invalid_input_never_hits_api(market_manager):
    result = market_manager.place_market_order('BTCUSDT', 'HOLD', 0.002)

    assert result['success'] is False
    assert 'Invalid side' in result['error']
    market_manager.client.futures_create_order.assert_not_called()


def test_market_order_api_error_is_reported(market_manager):
    response = MagicMock(status_code=400, text='{"code": -2019, "msg": "Margin is insufficient."}')
    market_manager.client.futures_create_order.side_effect = BinanceAPIException(response, 400, response.text)

    result = market_manager.place_market_order('BTCUSDT', 'BUY', 0.002)

    assert result['success'] is False
    assert 'Margin is insufficient' in result['error']


def test_get_market_price(market_manager):
    market_manager.client.futures_symbol_ticker.return_value = {'price': '60000.5'}
    assert market_manager.get_market_price('btcusdt') == 60000.5


def test_limit_order_success(limit_manager):
    result = limit_manager.place_limit_order('ETHUSDT', 'SELL', 0.1, 4000.0, 'ioc')

    assert result['success'] is True
    limit_manager.client.futures_create_order.assert_called_once_with(
        symbol='ETHUSDT', side='SELL', type='LIMIT', timeInForce='IOC', quantity=0.1, price=4000.0
    )


def test_limit_order_rejects_invalid_price(limit_manager):
    result = limit_manager.place_limit_order('ETHUSDT', 'SELL', 0.1, 0)

    assert result['success'] is False
    limit_manager.client.futures_create_order.assert_not_called()


def test_cancel_order(limit_manager):
    result = limit_manager.cancel_order('btcusdt', 12345)

    assert result['success'] is True
    limit_manager.client.futures_cancel_order.assert_called_once_with(symbol='BTCUSDT', orderId=12345)
