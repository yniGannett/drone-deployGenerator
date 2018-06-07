# drone-deployGenerator

## How to use

### Install

Clone this repo to anywhere of local

`pip install PyYAML`

### Prepared sample.yml
Modify sample.yml based on the requirement of the app deployment
- Modify environment variables
- Setup different values for deployment manifest

Modify prefix setting for each environment based on your change, if no change related to prefix, this step can be skipped

### Running

```
cd <path of repo>
python ./yml_generator.py
```

It will generate `deploy-all.yml` under the path, then you get deployments for different environment

### Don't forget to do last thing
deployGenerator is not perfect, we need to adjust the format for `sed commands` for each block

We need to replace `sed commands` from sample's `sed commands`
```
- "sed -i 's|name.*|name: '$DRONE_REPO_NAME'|g' .chart/Chart.yaml"
- "sed -i 's|version.*|version: '$VERSION'|g' .chart/Chart.yaml"
```



