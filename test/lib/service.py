import subprocess
import time


class Service:
    LOG = open("/logs/service.log", "w")
    service = None

    def start(self):
        self.service = subprocess.Popen(
            ["/usr/local/bin/python", "-m" "app"],
            cwd="/",
            stdout=self.LOG,
            stderr=self.LOG,
        )
        time.sleep(1)

    def stop(self):
        if self.service is not None:
            self.service.terminate()
            self.service.wait()
