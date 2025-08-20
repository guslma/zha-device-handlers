"""Device handler for Yale."""

from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.closures import DoorLock
from zigpy.zcl.clusters.general import (
    Alarms,
    Basic,
    Groups,
    Identify,
    PowerConfiguration,
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

from zigpy.quirks import CustomCluster

class YaleCluster(CustomCluster):
    """Proprietary Yale cluster (0x100F)."""

    cluster_id = 0x100F  # 4111
    name = "Yale Proprietary Cluster"
    ep_attribute = "yale_cluster"

class YaleLock(CustomDevice):
    """Yale YDM60 / YMC 420 D Locks."""

    signature = {
        #  <SimpleDescriptor endpoint=1 profile=260 device_type=10
        #  device_version=0
        #  input_clusters=[0, 3, 4, 257, 4111]
        #  output_clusters=[0, 3, 4, 257, 4111]>
        MODELS_INFO: [("Yale", "YDM60"), ("Yale", "YMC 420 D")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.DOOR_LOCK,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    DoorLock.cluster_id,
                    YaleCluster.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    DoorLock.cluster_id,
                    YaleCluster.cluster_id,
                ],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.DOOR_LOCK,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Alarms.cluster_id,
                    Time.cluster_id,
                    DoorLock.cluster_id,
                    PowerConfiguration.cluster_id,
                    YaleCluster.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Alarms.cluster_id,
                    Time.cluster_id,
                    DoorLock.cluster_id,
                    PowerConfiguration.cluster_id,
                    YaleCluster.cluster_id,
                ],

            }
        }
    }
