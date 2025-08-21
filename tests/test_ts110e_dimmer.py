import pytest
from unittest.mock import MagicMock

# Importe a classe SafeOnOffCluster do seu arquivo TS110E_dimmer.py
from zhaquirks.tuya.TS110E_dimmer import SafeOnOffCluster

# Importe as classes necessárias do zigpy
from zigpy.zcl.clusters.general import OnOff
from zigpy.endpoint import Endpoint

@pytest.fixture
def safe_on_off_cluster():
    """Fixture para criar uma instância de SafeOnOffCluster com um mock de OnOff."""
    # Crie um mock para o endpoint
    mock_endpoint = MagicMock(spec=Endpoint)
    # Crie uma instância de SafeOnOffCluster, que herda de OnOff e CustomCluster
    cluster = SafeOnOffCluster(mock_endpoint)
    # Adicione a lista para rastrear as atualizações de atributos
    cluster.attribute_updates = []

    # Faça o patch do método _update_attribute da classe pai (OnOff)
    # para que possamos rastrear as chamadas a super()._update_attribute
    original_update_attribute = OnOff._update_attribute
    def mocked_update_attribute(self, attrid, value):
        self.attribute_updates.append((attrid, value))
    
    with patch.object(OnOff, '_update_attribute', mocked_update_attribute):
        yield cluster

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

