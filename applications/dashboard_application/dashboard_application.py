import edgeiq
import multiprocessing
import queue
import time
import cv2
import numpy as np


class DashboardApp(multiprocessing.Process):
    def __init__(self, args):
        self._app_shared = args[0]
        self._frame_queues = self._app_shared.frames_to_web_mp_queues
        super().__init__()

    def _run(self):
        self._app_shared.process_barrier.wait()

        with edgeiq.Streamer() as streamer:
            while True:
                while True:
                    try:
                        frame1 = self._frame_queues[0].get(block=False)
                        frame2 = self._frame_queues[1].get(block=False)
                        break

                    except queue.Empty:
                        time.sleep(0.01)

                frame1 = cv2.resize(frame1, (640, 480))
                frame2 = cv2.resize(frame2, (640, 480))
                final_image = np.vstack((frame1, frame2))

                streamer.send_data(final_image, "")

                if streamer.check_exit():
                    break

    def run(self):
        try:
            self._run()
        except Exception as e:
            print("exception occured :", e)
            pass
        finally:
            self._app_shared.process_exit.set()

    def close(self):
        pass
