from datetime import date, timedelta
import pytest
from domain.models import allocate, OrderLine, Batch, OutOfStock

today = date.today()
tomorrow = date.today() + timedelta(days=1)
later = date.today() + timedelta(days=10)


def test_prefers_current_stock_batches_to_shipment():
    in_stock_batch = Batch('in-stock-batch', 'ANGULAR', 100, eta=None)
    shipment_batch = Batch('shipment-batch', 'ANGULAR', 100, eta=tomorrow)
    line = OrderLine('oder-123', 'ANGULAR', 10)
    allocate(line, [in_stock_batch, shipment_batch])
    assert in_stock_batch.available_quantity == 90
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("speedy-batch", "MINIMALIST-SPOON", 100, eta=today)
    medium = Batch("normal-batch", "MINIMALIST-SPOON", 100, eta=tomorrow)
    latest = Batch("slow-batch", "MINIMALIST-SPOON", 100, eta=later)
    line = OrderLine("order1", "MINIMALIST-SPOON", 10)
    allocate(line, [medium, earliest, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch('in-stock-batch', 'ANGULAR', 200, eta=None)
    shipment_batch = Batch('shipment-batch', 'ANGULAR', 200, eta=tomorrow)
    line = OrderLine('oder-123', 'ANGULAR', 10)
    allocation = allocate(line, [in_stock_batch, shipment_batch])
    assert allocation == in_stock_batch.reference


def test_raise_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL', 10, eta=today)
    line = OrderLine('order-1', 'SMALL', 10)
    allocate(line, [batch])
    with pytest.raises(OutOfStock, match="SMALL"):
        allocate(OrderLine('order-2', 'SMALL', 1), [batch])
