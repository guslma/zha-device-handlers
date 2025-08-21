import pytest
from unittest.mock import MagicMock, patch

from zhaquirks.tuya.TS110E_dimmer import SafeOnOffCluster

from zigpy.zcl.clusters.general import OnOff

class MockOnOffCluster(OnOff):
    """Um mock simplificado para a classe OnOff para capturar chamadas a _update_attribute."""
    def __init__(self):
        super().__init__()
        self.attribute_updates = []

    def _update_attribute(self, attrid, value):
        self.attribute_updates.append((attrid, value))

@pytest.fixture
def safe_on_off_cluster():
    """Fixture para criar uma instância de SafeOnOffCluster com um mock de OnOff."""
    mock_parent_cluster = MockOnOffCluster()
    return SafeOnOffCluster(mock_parent_cluster)

def test_safe_on_off_cluster_blocks_off_command(safe_on_off_cluster):
    """Testa se o comando OFF (attrid=0x0000, value=0) é bloqueado."""
    safe_on_off_cluster._update_attribute(0x0000, 0)
    assert len(safe_on_off_cluster.attribute_updates) == 0

def test_safe_on_off_cluster_allows_on_command(safe_on_off_cluster):
    """Testa se o comando ON (attrid=0x0000, value=1) é permitido."""
    safe_on_off_cluster._update_attribute(0x0000, 1)
    assert len(safe_on_off_cluster.attribute_updates) == 1
    assert safe_on_off_cluster.attribute_updates[0] == (0x0000, 1)

def test_safe_on_off_cluster_allows_other_attributes(safe_on_off_cluster):
    """Testa se outros atributos são permitidos e passados."""
    safe_on_off_cluster._update_attribute(0x0001, 100)
    assert len(safe_on_off_cluster.attribute_updates) == 1
    assert safe_on_off_cluster.attribute_updates[0] == (0x0001, 100)


# def test_dimmer_switch_signature():
#     device = DimmerSwitch()
#     assert device.signature["MODELS_INFO"][0] == ("_TZ3210_ysfo0wla", "TS110E")
#     assert device.signature["ENDPOINTS"][1]["PROFILE_ID"] == zha.PROFILE_ID

