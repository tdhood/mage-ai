from mage_ai.data_preparation.repo_manager import RepoConfig
from mage_ai.services.aws.emr.emr import create_a_new_cluster
from mage_ai.services.aws.emr.resource_manager import EmrResourceManager


def create_cluster(project_path, done_status='WAITING', tags=dict()):
    print(f'Creating EMR cluster for project: {project_path}')
    repo_config = RepoConfig(project_path)
    # Upload bootstrap script
    resource_manager = EmrResourceManager(
        repo_config.s3_bucket,
        repo_config.s3_path_prefix,
    )
    resource_manager.upload_bootstrap_script()

    # Create EMR cluster
    cluster_id = create_a_new_cluster(
        'mage-data-preparation',
        [],
        repo_config.emr_config,
        bootstrap_script_path=resource_manager.bootstrap_script_path,
        done_status=done_status,
        keep_alive=True,
        log_uri=resource_manager.log_uri,
        tags=tags,
    )
    print(f'Cluster {cluster_id} is created')
