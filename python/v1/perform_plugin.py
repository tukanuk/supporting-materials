"""
Perform Host Performance Demo Extension
"""

from datetime import datetime, timedelta
import logging

import shutil
import psutil

from ruxit.api.base_plugin import BasePlugin


logger = logging.getLogger(__name__)

class PerformHostPerformancePlugin(BasePlugin):
    """
    Main class of extension
    """
    
    last_metric_report: datetime = datetime.now()
    last_event: datetime = datetime.now()

    
    def query(self, **kwargs):
        
        logger.info("Starting PerformHostPerformancePlugin")

        # Collect the metrics
        total, used, free = shutil.disk_usage(__file__)
        cpu: float = psutil.cpu_percent(percpu=False)
        ram: float = psutil.virtual_memory().percent

        # Report the metrics
        if (datetime.now() - self.last_metric_report) > timedelta(minutes=self.config.get('interval', 1)):
            self.results_builder.absolute(key='disk.used', value=used)
            self.results_builder.absolute(key='disk.free', value=free)
            self.results_builder.absolute(key='disk.total', value=total)
            self.results_builder.absolute(key='cpu.usage', value=cpu)
            self.results_builder.absolute(key='memory.usage', value=ram)
        
        # Push an event every five minutes
        if (datetime.now() - self.last_event) > timedelta(minutes=5):
            logger.info("Reporting a custom event")
            self.results_builder.report_resource_contention_event(
                title="Host Performance Resource Event (v1)",
                description="Host Performance Resource Event (v1)",
                properties= {
                    "free": str(free),
                    "cpu": str(cpu),
                    "ram": str(ram),
                }
            )
            self.last_event = datetime.now()
        
        logger.info("Ending the query")