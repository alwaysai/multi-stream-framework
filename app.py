from edgeiq import MultiprocessFramework
from applications import DetectorApp, ClassifierApp, DashboardApp
from app_shared import AppShared
import os


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

if __name__ == "__main__":
    try:
        exit_flag = app_shared.process_exit
        app.start(exit_flag)

    finally:
        app.close()
