"""
Main exension file
"""
from datetime import datetime, timedelta

import shutil
from dynatrace_extension import Extension, Status, StatusValue, DtEventType
import psutil

# pylint: disable=W1203, W0201, C0301

METRIC_PREFIX = "custom.perform_host_performance"

class ExtensionImpl(Extension):
    """
    Main extension class
    """

    def initialize(self):
        self.extension_name = "python_perform_host_performance"
        self.last_event = datetime.now()

        self.logger.info(self.activation_config)

    def query(self):
        """
        The query method is automatically scheduled to run every minute
        """
        self.logger.info(f"query method started for {self.extension_name}.")

        for endpoint in self.activation_config["endpoints"]:

            self.logger.info(f"Endpoint: {endpoint}")

            # Collect the metrics
            total, used, free = shutil.disk_usage(__file__)
            cpu: float = psutil.cpu_percent(percpu=False)
            ram: float = psutil.virtual_memory().percent


            self.logger.debug("A debug message")
            self.logger.info(f"CPU -> {cpu:2.2f}%")

            # Report metrics with
            self.report_metric(f"{METRIC_PREFIX}.disk.total", total, dimensions={"my_dimension": "dimension1"})
            self.report_metric(f"{METRIC_PREFIX}.disk.used", used, dimensions={"my_dimension": "dimension1"})
            self.report_metric(f"{METRIC_PREFIX}.disk.free", free, dimensions={"my_dimension": "dimension1"})
            self.report_metric(f"{METRIC_PREFIX}.cpu.usage", cpu, dimensions={"my_dimension": "dimension1"})
            self.report_metric(f"{METRIC_PREFIX}.memory.usage", ram, dimensions={"my_dimension": "dimension1"})

            self.logger.info(f"Last event was at {self.last_event}")

            if (datetime.now() - self.last_event) > timedelta(minutes=5):
                self.logger.info("Reporting a resource contention event (v2)")
                self.report_dt_event(
                    event_type=DtEventType.RESOURCE_CONTENTION_EVENT,
                    title="Reporting a resource contention event (v2)",
                    properties= {
                        "free": str(free),
                        "cpu": str(cpu),
                        "ram": str(ram),
                    },
                )
                self.last_event: datetime = datetime.now()

        self.logger.info("query method ended for python_perform_host_performance.")

    def fastcheck(self) -> Status:
        """
        This is called when the extension runs for the first time.
        If this AG cannot run this extension, raise an Exception or return StatusValue.ERROR!
        """
        return Status(StatusValue.OK)


def main():
    ExtensionImpl().run()



if __name__ == '__main__':
    main()
