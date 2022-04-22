#!/bin/bash
/usr/local/Cellar/mosquitto/2.0.11/bin/mosquitto_sub \
-h nam1.cloud.thethings.network:1883 -t '+/devices/+/up' \
-u 'iot-food-mgmt@ttn' \
-P 'NNSXS.3SKSOMT667KG4JY4IUALXJPJNNRPWEME3I7Q3FI.OWWDZHAP5PLF7NOW7AGIBPBBSMDDN3LE5L2J46PFJCPIDUOLYKMQ' -v
