# video_stitch_py
Stitch videos together in Python


## Setup

```bash
conda create --name video-stitch python=3.13
conda activate video-stitch
pip install moviepy==2.1.2
pip install boto3==1.38.2
pip install PyYAML==6.0.2

brew install awscli
aws configure
```

Create a yaml file based on the example_config.yaml file.

## Run

Places videos you want to stitch in _input_ folder.
Run 

```bash
python main.py
```
