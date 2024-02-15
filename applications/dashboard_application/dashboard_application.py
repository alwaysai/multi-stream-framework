import edgeiq
import cv2
import numpy as np

from app_shared import AppShared


class DashboardApp(edgeiq.MultiStreamAppInterface):
    def __init__(self, app_shared: AppShared):
        self._app_shared = app_shared
        self._frame_queues = self._app_shared.frames_to_web_mp_queues

    def _run(self):
        self._app_shared.process_barrier.wait()
        print('Running DashboardApp')

        with edgeiq.Streamer() as streamer:
            while True:
                frames = []
                for frame_queue in self._frame_queues:
                    frames.append(frame_queue.get())

                for frame in frames:
                    frame = cv2.resize(frame, (640, 480))
                final_image = np.vstack(frames)

                streamer.send_data(final_image)

                if streamer.check_exit():
                    break

                if self._app_shared.process_exit.is_set():
                    break

    def run(self):
        try:
            self._run()
        finally:
            print('DashboardApp closing...')
            self._app_shared.process_exit.set()
