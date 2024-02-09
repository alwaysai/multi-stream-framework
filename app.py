import json
import multiprocessing
import os
from typing import List, Type
import edgeiq
from applications import DetectorApp, DashboardApp
from app_shared import AppShared
import threading


class MonitorThread(threading.Thread):
    def __init__(
        self,
        app: edgeiq.MultiprocessFramework,
        exit_flag: multiprocessing.Event
    ):
        self._app = app
        self._exit_flag = exit_flag
        super().__init__()

    def run(self):
        self._exit_flag.wait()
        self._app.stop()


if __name__ == "__main__":
    # Load configuration
    cfg_path = 'config.json'
    if not os.path.exists(cfg_path):
        raise FileNotFoundError('{} not found!'.format(cfg_path))

    with open(cfg_path) as f:
        cfg: dict = json.load(f)

    # Build app configuration
    stream_count = len(cfg['streams'])
    app_shared = AppShared(stream_count)

    apps: List[Type[edgeiq.MultiprocessAppInterface]] = []
    args: List[tuple] = []

    for i, stream in enumerate(cfg['streams']):
        apps.append(DetectorApp)
        args.append((
            stream['model_id'],
            stream['stream_source'],
            app_shared.frames_to_web_mp_queues[i],
            app_shared,
        ))

    apps.append(DashboardApp)
    args.append((
        app_shared,
    ))

    app = edgeiq.MultiprocessFramework(apps=apps, args=args)
    monitor_thread = MonitorThread(app, app_shared.process_exit)

    # Run application
    monitor_thread.start()
    try:
        app.start()
    finally:
        # Ensure monitor thread closes
        app_shared.process_exit.set()
        monitor_thread.join(timeout=1)
