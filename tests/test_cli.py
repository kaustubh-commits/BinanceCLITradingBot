from unittest.mock import patch

import pytest
from click.testing import CliRunner

from src import cli as cli_module

OK = {'success': True, 'message': 'ok'}


@pytest.fixture
def runner():
    return CliRunner()


def test_market_buy_parses_arguments(runner):
    with patch.object(cli_module, 'MarketOrderManager') as manager_cls:
        manager_cls.return_value.place_market_order.return_value = OK
        result = runner.invoke(cli_module.cli, ['market', 'buy', 'BTCUSDT', '0.002'])

    assert result.exit_code == 0
    manager_cls.return_value.place_market_order.assert_called_once_with('BTCUSDT', 'BUY', 0.002)
    assert 'ok' in result.output


def test_market_sell_reports_error(runner):
    with patch.object(cli_module, 'MarketOrderManager') as manager_cls:
        manager_cls.return_value.place_market_order.return_value = {'success': False, 'error': 'boom'}
        result = runner.invoke(cli_module.cli, ['market', 'sell', 'ETHUSDT', '0.1'])

    assert result.exit_code == 0
    manager_cls.return_value.place_market_order.assert_called_once_with('ETHUSDT', 'SELL', 0.1)
    assert 'boom' in result.output


def test_market_rejects_non_numeric_quantity(runner):
    with patch.object(cli_module, 'MarketOrderManager') as manager_cls:
        result = runner.invoke(cli_module.cli, ['market', 'buy', 'BTCUSDT', 'lots'])

    assert result.exit_code == 2
    manager_cls.assert_not_called()


def test_market_requires_quantity(runner):
    result = runner.invoke(cli_module.cli, ['market', 'buy', 'BTCUSDT'])
    assert result.exit_code == 2


def test_limit_buy_defaults_to_gtc(runner):
    with patch.object(cli_module, 'LimitOrderManager') as manager_cls:
        manager_cls.return_value.place_limit_order.return_value = OK
        result = runner.invoke(cli_module.cli, ['limit', 'buy', 'BTCUSDT', '0.002', '55000'])

    assert result.exit_code == 0
    manager_cls.return_value.place_limit_order.assert_called_once_with('BTCUSDT', 'BUY', 0.002, 55000.0, 'GTC')


def test_limit_sell_accepts_tif_option(runner):
    with patch.object(cli_module, 'LimitOrderManager') as manager_cls:
        manager_cls.return_value.place_limit_order.return_value = OK
        result = runner.invoke(cli_module.cli, ['limit', 'sell', 'ETHUSDT', '0.1', '4000', '--tif', 'IOC'])

    assert result.exit_code == 0
    manager_cls.return_value.place_limit_order.assert_called_once_with('ETHUSDT', 'SELL', 0.1, 4000.0, 'IOC')


def test_limit_cancel_parses_order_id_as_int(runner):
    with patch.object(cli_module, 'LimitOrderManager') as manager_cls:
        manager_cls.return_value.cancel_order.return_value = OK
        result = runner.invoke(cli_module.cli, ['limit', 'cancel', 'BTCUSDT', '12345'])

    assert result.exit_code == 0
    manager_cls.return_value.cancel_order.assert_called_once_with('BTCUSDT', 12345)


def test_oco_prints_both_order_ids(runner):
    with patch.object(cli_module, 'OCOOrderManager') as manager_cls:
        manager_cls.return_value.place_oco_order.return_value = {
            'success': True, 'message': 'ok',
            'tp_order': {'orderId': 111}, 'sl_order': {'orderId': 222},
        }
        result = runner.invoke(cli_module.cli, ['advanced', 'oco', 'BTCUSDT', 'BUY', '0.002', '70000', '55000'])

    assert result.exit_code == 0
    manager_cls.return_value.place_oco_order.assert_called_once_with('BTCUSDT', 'BUY', 0.002, 70000.0, 55000.0)
    assert '111' in result.output and '222' in result.output


def test_twap_parses_interval_option(runner):
    with patch.object(cli_module, 'TWAPOrderManager') as manager_cls:
        manager_cls.return_value.place_twap_order.return_value = {
            'success': True, 'message': 'ok', 'total_intervals': 30, 'quantity_per_order': 0.0003,
        }
        result = runner.invoke(cli_module.cli, ['advanced', 'twap', 'BTCUSDT', 'BUY', '0.01', '30', '--interval', '60'])

    assert result.exit_code == 0
    manager_cls.return_value.place_twap_order.assert_called_once_with('BTCUSDT', 'BUY', 0.01, 30, 60)


def test_grid_parses_arguments(runner):
    with patch.object(cli_module, 'GridOrderManager') as manager_cls:
        manager_cls.return_value.create_grid_orders.return_value = {
            'success': True, 'message': 'ok', 'buy_orders_count': 2, 'sell_orders_count': 3,
        }
        result = runner.invoke(cli_module.cli, ['advanced', 'grid', 'BTCUSDT', '58000', '62000', '5', '0.002'])

    assert result.exit_code == 0
    manager_cls.return_value.create_grid_orders.assert_called_once_with('BTCUSDT', 58000.0, 62000.0, 5, 0.002)
    assert 'Created 2 buy orders and 3 sell orders' in result.output


def test_grid_rejects_non_integer_levels(runner):
    result = runner.invoke(cli_module.cli, ['advanced', 'grid', 'BTCUSDT', '58000', '62000', 'five', '0.002'])
    assert result.exit_code == 2
