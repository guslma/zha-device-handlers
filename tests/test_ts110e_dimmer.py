import pytest

# Importe as classes necessárias do zigpy, se elas não forem mockadas
from zigpy.zcl.clusters.general import OnOff

# Importe a classe SafeOnOffCluster do seu arquivo TS110E_dimmer.py
# Certifique-se de que o caminho de importação esteja correto para o seu ambiente
from zhaquirks.tuya.TS110E_dimmer import SafeOnOffCluster


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
    # Simula o comando OFF
    safe_on_off_cluster._update_attribute(0x0000, 0)
    # Verifica se nenhuma atualização foi passada para o cluster pai
    assert len(safe_on_off_cluster.attribute_updates) == 0


def test_safe_on_off_cluster_allows_on_command(safe_on_off_cluster):
    """Testa se o comando ON (attrid=0x0000, value=1) é permitido."""
    # Simula o comando ON
    safe_on_off_cluster._update_attribute(0x0000, 1)
    # Verifica se a atualização foi passada para o cluster pai
    assert len(safe_on_off_cluster.attribute_updates) == 1
    assert safe_on_off_cluster.attribute_updates[0] == (0x0000, 1)


def test_safe_on_off_cluster_allows_other_attributes(safe_on_off_cluster):
    """Testa se outros atributos são permitidos e passados."""
    # Simula uma atualização de outro atributo
    safe_on_off_cluster._update_attribute(0x0001, 100)
    # Verifica se a atualização foi passada para o cluster pai
    assert len(safe_on_off_cluster.attribute_updates) == 1
    assert safe_on_off_cluster.attribute_updates[0] == (0x0001, 100)


# Se houver outras classes ou métodos no TS110E_dimmer.py que precisam de cobertura,
# você precisaria adicionar testes para eles aqui.
# Por exemplo, para a classe DimmerSwitch, você precisaria simular a inicialização
# e a interação com seus atributos e métodos.

# Exemplo de teste para a classe DimmerSwitch (simplificado)
# from zhaquirks.tuya.TS110E_dimmer import DimmerSwitch
# from zigpy.profiles import zha
# from zigpy.quirks import CustomDevice

# def test_dimmer_switch_signature():
#     device = DimmerSwitch()
#     assert device.signature["MODELS_INFO"][0] == ("_TZ3210_ysfo0wla", "TS110E")
#     assert device.signature["ENDPOINTS"][1]["PROFILE_ID"] == zha.PROFILE_ID
