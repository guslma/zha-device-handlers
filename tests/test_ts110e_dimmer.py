"""Testes para o módulo TS110E_dimmer, focando na cobertura do SafeOnOffCluster."""

from unittest.mock import MagicMock, patch

import pytest
from zigpy.endpoint import Endpoint
from zigpy.zcl.clusters.general import OnOff

from zhaquirks.tuya.TS110E_dimmer import SafeOnOffCluster


@pytest.fixture
def safe_on_off_cluster():
    """Fixture para criar uma instância de SafeOnOffCluster com um mock de OnOff."""
    mock_endpoint = MagicMock(spec=Endpoint)
    cluster = SafeOnOffCluster(mock_endpoint)
    cluster.attribute_updates = []

    def mocked_update_attribute(self, attrid, value):
        self.attribute_updates.append((attrid, value))

    with patch.object(OnOff, "_update_attribute", mocked_update_attribute):
        yield cluster


def test_safe_on_off_cluster_blocks_off_command(safe_on_off_cluster):
    """Testa se o OFF (attrid=0x0000, value=0) é bloqueado."""
    safe_on_off_cluster._update_attribute(0x0000, 0)
    assert len(safe_on_off_cluster.attribute_updates) == 0


def test_safe_on_off_cluster_allows_on_command(safe_on_off_cluster):
    """Testa se o ON (attrid=0x0000, value=1) é permitido."""
    safe_on_off_cluster._update_attribute(0x0000, 1)
    assert len(safe_on_off_cluster.attribute_updates) == 1
    assert safe_on_off_cluster.attribute_updates[0] == (0x0000, 1)


def test_safe_on_off_cluster_allows_other_attributes(safe_on_off_cluster):
    """Testa se outros atributos são permitidos e passados."""
    safe_on_off_cluster._update_attribute(0x0001, 100)
    assert len(safe_on_off_cluster.attribute_updates) == 1
    assert safe_on_off_cluster.attribute_updates[0] == (0x0001, 100)
