import time
import edgeiq
from .config import DetectorAppConfig
from edgeiq._utils import empty_queue


class DetectorApp:
    # this class would be instantiated in the base process
    # this app can load the app config, parse it and intialize the variables
    def __init__(self, args):
        self._config_filepath = args[0]
        self._app_shared = args[1]

        self._app_config = DetectorAppConfig(self._config_filepath)
        self._app_fps = self._app_config.app_fps

        # variables from application configuration
        self._camera_stream = self._app_config.source_file
        self._detector_model = self._app_config.detector_model
        self._process_idx = self._app_config.process_idx

        # update time
        self._update_time = 1 / self._app_fps
        self._last_update = time.time()

    def _gen_stream_object(self):
        stream_object = edgeiq.FileVideoStream(
            self._camera_stream, play_realtime=False, fps=self._app_fps
        )
        self._stream_object = stream_object

    def _start_stream(self):
        self._stream_object.start()

    def _read_stream(self):
        try:
            frame = self._stream_object.read()
            frame = edgeiq.resize(frame, width=640, height=360)

        except Exception:
            self._stream_object.stop()
            self._stream_object.start()
            frame = self._stream_object.read()
            frame = edgeiq.resize(frame, width=640, height=360)

        return frame

    def _stop_stream(self):
        self._stream_object.stop()

    def close(self):
        empty_queue(self._app_shared.frames_to_web_mp_queues[
            self._process_idx])

    def run(self):
        self._gen_stream_object()
        self._person_detector = edgeiq.ObjectDetection(self._detector_model)
        self._person_detector.load(engine=edgeiq.Engine.DNN)
        self._start_stream()

        self._app_shared.process_barrier.wait()

        try:
            while True:
                self._current_time = time.time()
                elapsed_time = self._current_time - self._last_update

                if self._app_shared.process_exit.is_set():
                    break

                if elapsed_time >= self._update_time:
                    self._last_update = self._current_time
                    person_frame = self._read_stream()
                    person_result = self._person_detector.detect_objects(
                        person_frame, confidence_level=0.5
                    )

                    # Predict image and update the trackers
                    frame = person_result.image
                    people_predictions = edgeiq.filter_predictions_by_label(
                        person_result.predictions, ["person"]
                    )

                    # Markup frame
                    frame = edgeiq.markup_image(frame, people_predictions)

                    # Submit frames to the queue
                    self._app_shared.frames_to_web_mp_queues[1].put(frame)

                else:
                    remaining_time = self._update_time - elapsed_time
                    time.sleep(remaining_time)

        finally:
            self._stop_stream()
            self.close()
