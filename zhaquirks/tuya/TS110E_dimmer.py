from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import (
    Basic,
    Groups,
    Identify,
    LevelControl,
    OnOff,
    Ota,
    Scenes,
    Time,
)
from zigpy.zcl.clusters.manufacturer_specific import ManufacturerSpecificCluster


class SafeOnOffCluster(OnOff):
    def _update_attribute(self, attrid, value):
        if attrid == 0x0000 and value == 0:
            self.debug("Ignorando OFF automático")
            return  # Bloqueia o OFF
        super()._update_attribute(attrid, value)


class TuyaManufCluster(ManufacturerSpecificCluster):
    cluster_id = 0xEF00
    name = "tuya_manufacturer"
    ep_attribute = "tuya_manufacturer"


class TS110E(CustomDevice):
    """Quirk for Tuya TS110E Dimmer."""

    signature = {
        "models_info": [("_TZ3210_ysfo0wla", "TS110E")],
        "endpoints": {
            1: {
                "profile_id": zha.PROFILE_ID,
                "device_type": 0x0101,
                "input_clusters": [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    0xEF00,
                ],
                "output_clusters": [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
            242: {
                "profile_id": 0xA1E0,
                "device_type": 0x0061,
                "input_clusters": [],
                "output_clusters": [0x0021],
            },
        },
    }

    replacement = {
        "endpoints": {
            1: {
                "profile_id": zha.PROFILE_ID,
                "device_type": 0x0101,
                "input_clusters": [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    SafeOnOffCluster,  # substitui OnOff padrão
                    LevelControl.cluster_id,
                    TuyaManufCluster,
                ],
                "output_clusters": [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
            242: {
                "profile_id": 0xA1E0,
                "device_type": 0x0061,
                "input_clusters": [],
                "output_clusters": [0x0021],
            },
        }
    }
