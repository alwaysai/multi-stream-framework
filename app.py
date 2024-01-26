from edgeiq import MultiprocessFramework
from applications import DetectorApp, ClassifierApp, DashboardApp
from app_shared import AppShared
import os
import threading

# Load configuration paths
capacity_appconfig = os.path.abspath(os.path.join("config",
                                                  "detector_app.yml"))
ppe_appconfig = os.path.abspath(os.path.join("config", "classifier_app.yml"))
app_shared = AppShared()


# app shared to be passed in along with config in the args
app = MultiprocessFramework(
    apps=[DetectorApp, ClassifierApp, DashboardApp],
    args=[(capacity_appconfig, app_shared),
          (ppe_appconfig, app_shared),
          (app_shared,)],)


class MonitorThread(threading.Thread):
    def __init__(self, app, exit_flag):
        self._app = app
        self._exit_flag = exit_flag
        super().__init__()

    def run(self):
        self._exit_flag.wait()
        self._app.stop()


if __name__ == "__main__":
    exit_flag = app_shared.process_exit
    monitor_thread = MonitorThread(app, exit_flag)
    monitor_thread.start()
    app.start()
    exit_flag.set()
