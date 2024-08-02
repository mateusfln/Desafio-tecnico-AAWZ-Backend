import pytest
import pandas as pd
from app.planilha_handler import PlanilhaHandler

@pytest.fixture
def handler():
    return PlanilhaHandler()

def test_converter_valor(handler):
    assert handler.converter_valor("R$ 1.234,56") == 1234.56
    assert handler.converter_valor("R$ 0,00") == 0.0
    assert handler.converter_valor("1234") == 1234.0
    assert handler.converter_valor("") == 0.0


