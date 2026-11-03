#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/sensor.h>
#include <zephyr/logging/log.h>
#include <zephyr/sys/printk.h>

LOG_MODULE_REGISTER(main, LOG_LEVEL_INF);

#define SCD41_NODE DT_NODELABEL(scd41)
#define ATM_PR_MMHG 760.0 // Atmospheric pressure (standard)
#define TEMP_WARN_THRESHOLD_C 45.0
#define TEMP_HYSTERESIS_C      1.0

int main(void)
{
    struct sensor_value co2, temp, humidity;
    const struct device *scd41 = DEVICE_DT_GET(SCD41_NODE);
	bool temp_alarm = false;

	if (!device_is_ready(scd41)) {
		printk("SCD41 not ready\n");
		return -ENODEV;
	}

	printk("Sensor ready: %s\n", scd41->name);

	while (1) {
		/* Fetch sensor data */
		int rc = sensor_sample_fetch(scd41);
		if (rc != 0) {
			LOG_ERR("Failed to fetch sensor data: %d\n", rc);
			k_msleep(1000);
			continue;

		}

		sensor_channel_get(scd41, SENSOR_CHAN_CO2, &co2);
		sensor_channel_get(scd41, SENSOR_CHAN_AMBIENT_TEMP, &temp);
		sensor_channel_get(scd41, SENSOR_CHAN_HUMIDITY, &humidity);

		double co2_ppm = co2.val1 + (co2.val2 / 1000000.0);
		double co2_mmhg = (co2_ppm/1000000.0) * ATM_PR_MMHG;

		double temp_c = sensor_value_to_double(&temp);
		if (temp_c > TEMP_WARN_THRESHOLD_C) {
			LOG_WRN("High temperature: %d.%d°C (limit %d°C)",
				temp.val1, temp.val2 / 100000,
				(int)TEMP_WARN_THRESHOLD_C);
			temp_alarm = true;
		} else if (temp_alarm &&
			   temp_c < (TEMP_WARN_THRESHOLD_C - TEMP_HYSTERESIS_C)) {
			LOG_INF("Temperature back to normal: %d.%d°C",
				temp.val1, temp.val2 / 100000);
			temp_alarm = false;
		}

		int mmhg_int = (int)co2_mmhg;
		int mmhg_frac = (int)((co2_mmhg - mmhg_int) * 10000);

		LOG_INF("CO2: %d.%d ppm | Temp: %d.%d°C | Humidity: %d.%d%% | CO2: %d.%04d mmHg\n",
			co2.val1, co2.val2 / 100000,
			temp.val1, temp.val2 / 100000,
			humidity.val1, humidity.val2 / 100000,
			mmhg_int, mmhg_frac);

		k_msleep(5000);
	}

	return 0;
}
