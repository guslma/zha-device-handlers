"""Quirk for Tuya TS110E Dimmer."""

from zigpy.profiles import zgp, zha
from zigpy.quirks import CustomCluster, CustomDevice
from zigpy.zcl.clusters.general import (
    Basic,
    GreenPowerProxy,
    Groups,
    Identify,
    LevelControl,
    OnOff,
    Ota,
    Scenes,
    Time,
)

from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.tuya import TuyaManufCluster


class SafeOnOffCluster(OnOff, CustomCluster):
    """Safe OnOff cluster for Tuya TS110E Dimmer that blocks automatic OFF."""

    def _update_attribute(self, attrid, value):
        if attrid == 0x0000 and value == 0:
            self.debug("Ignorando OFF automático")
            return  # Bloqueia o OFF
        super()._update_attribute(attrid, value)


class DimmerSwitch(CustomDevice):
    """Quirk for Tuya TS110E Dimmer."""

    signature = {
        MODELS_INFO: [("_TZ3210_ysfo0wla", "TS110E")],
        ENDPOINTS: {
            #  <SimpleDescriptor endpoint=1 profile=260 device_type=257
            #  input_clusters=[0, 3, 4, 5, 6, 8, 61184]
            #  output_clusters=[10, 25]>
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.DIMMABLE_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    TuyaManufCluster.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
            #  <SimpleDescriptor endpoint=242 profile=41376 device_type=97
            #  input_clusters=[]
            #  output_clusters=[33]>
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.DIMMABLE_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    SafeOnOffCluster,
                    LevelControl.cluster_id,
                    TuyaManufCluster,
                ],
                OUTPUT_CLUSTERS: [
                    Time.cluster_id,
                    Ota.cluster_id,
                ],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        }
    }
