# multistream_framework
Use multistream framework to develop multiple applications on individual processes and run them in parallel.

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

## Notes
* Configuration files used for the application can be found under the config directory
* Configuration can be customed handled at the application level. Examples of that can be  found in the `config.py` scripts for each application in the applications directory.
* `app_shared.py` script contains shared resources that would be shared between applications.
* The detector application is configured to run with `test.mp4` in the `videos` directory. Please add a sample video in the directory to run or set it to appropriate path in the configuration file.

To change the computer vision model, the engine and accelerator, and add additional dependencies read [this guide](https://alwaysai.co/docs/application_development/configuration_and_packaging.html).

## Support
* [Documentation](https://alwaysai.co/docs/)
* [Community Discord](https://discord.gg/alwaysai)
* Email: support@alwaysai.co