# Multi-Stream Framework
This application demonstrates using the multi-stream framework to process multiple camera streams using multi-processing.

## Requirements
* [alwaysAI account](https://alwaysai.co/auth?register=true)
* [alwaysAI Development Tools](https://alwaysai.co/docs/get_started/development_computer_setup.html)

## Usage
Once the alwaysAI tools are installed on your development machine (or edge device if developing directly on it) you can install and run the app with the following CLI commands:

To perform initial configuration of the app:
```
aai app configure
```

To prepare the runtime environment and install app dependencies:
```
aai app install
```

To start the app:
```
aai app start
```

This application runs two different models on two camera streams, and can be stopped by pressing the "stop" button on the Streamer.

### Configuration

The configuration for this application is in `config.json`:

```json
{
  "streams": [
    {
      "stream_source": 0,
      "model_id": "alwaysai/yolo_v3"
    },
    {
      "stream_source": 2,
      "model_id": "alwaysai/yolo_v4"
    }
  ]
}
```

You can modify this config to have as many camera streams and models as your hardware can support. Additionally, you can change `WebcamVideoStream` to `IPVideoStream` or `FileVideoStream` in `DetectorApp` depending on your use case, and then modify the contents of the config file to provide the desired inputs. See the [VideoStream API docs](https://alwaysai.co/docs/edgeiq_api/video_stream.html) for more details.


To change the computer vision model, the engine and accelerator, and add additional dependencies read [this guide](https://docs.alwaysai.co/application_development/application_configuration.html).

## Support
* [Documentation](https://alwaysai.co/docs/)
* [Community Discord](https://discord.gg/alwaysai)
* Email: support@alwaysai.co
