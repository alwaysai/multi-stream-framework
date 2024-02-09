import edgeiq
from edgeiq._utils import MultiprocessingCircularQueue

from app_shared import AppShared
from edgeiq._utils import empty_queue


class DetectorApp(edgeiq.MultiprocessAppInterface):
    def __init__(
        self,
        model_id: str,
        stream_source: str,
        frames_to_web_queue: MultiprocessingCircularQueue,
        app_shared: AppShared
    ):
        self._model_id = model_id
        self._stream_source = stream_source
        self._frames_to_web_mp_queue = frames_to_web_queue
        self._app_shared = app_shared

    def close(self):
        empty_queue(self._frames_to_web_mp_queue)

    def run(self):
        stream = edgeiq.WebcamVideoStream(self._stream_source).start()
        detector = edgeiq.ObjectDetection(self._model_id)
        detector.load(engine=edgeiq.Engine.DNN)

        # Wait for all processes to initialize
        self._app_shared.process_barrier.wait()

        try:
            while True:
                if self._app_shared.process_exit.is_set():
                    break

                frame = stream.read()
                result = detector.detect_objects(
                    frame, confidence_level=0.5
                )

                # Markup frame
                frame = edgeiq.markup_image(frame, result.predictions)

                # Submit frames to the dashboard
                self._frames_to_web_mp_queue.put(frame)

        finally:
            stream.stop()
