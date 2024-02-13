import json
from multiprocessing.synchronize import Event as EventClass
import os
from typing import List, Type
import edgeiq
from applications import DetectorApp, DashboardApp
from app_shared import AppShared
import threading


def wait_for_exit_cmd(app: edgeiq.MultiStreamFramework, exit_flag: EventClass):
    exit_flag.wait()
    app.stop()


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

    apps: List[Type[edgeiq.MultiStreamAppInterface]] = []
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

    app = edgeiq.MultiStreamFramework(apps=apps, args=args)
    monitor_thread = threading.Thread(target=wait_for_exit_cmd, args=(app, app_shared.process_exit))

    # Run application
    monitor_thread.start()
    try:
        app.start()
    finally:
        # Ensure monitor thread closes
        app_shared.process_exit.set()
        monitor_thread.join(timeout=1)
