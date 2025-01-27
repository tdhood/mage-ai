# 📚 Documentation

## Table of contents

### Development experience
- [Setup and install](tutorials/quick_start/setup.md)
- [Tutorials](tutorials/README.md)
- Concepts
    - [Core design principles](core/design_principles.md)
    - [Core abstractions](core/abstractions.md)
    - [Blocks](blocks/README.md)
- Data pipeline management
    - [UI overview](features/orchestration/README.md)
- [Kernels](kernels/README.md)
    - [Spark and PySpark](spark/setup/README.md)
- Testing
    - [Data validation](testing/README.md#data-validation)
- [Templates](#templates)

### Production
- Deploying to cloud
    - [Using Terraform](deploy/terraform/README.md)
    - [AWS](deploy/aws/README.md)
- Configuring production settings
    - [Compute resource](production/compute_resource.md)
    - [Runtime variables](production/runtime_variables.md)
- Triggering pipelines
    - [Schedule pipelines to run periodically](tutorials/triggers/schedule.md)
    - [Trigger pipeline from AWS Event (WIP)](tutorials/triggers/events/aws.md)
- Monitoring and alerting
    - [Status updates in Slack](monitoring/alerting/slack.md)
- Integrating with other tools
    - [Airflow](tutorials/airflow/integrate_into_existing_project/README.md)
    - [Prefect](production/prefect.md)

<br />

## Templates

### `io_config.yaml`

This YAML file contains the information and credentials required to access
databases, data warehouses, and data lakes.

[Example](https://github.com/mage-ai/mage-ai/blob/master/mage_ai/data_preparation/templates/repo/io_config.yaml)

<br />
