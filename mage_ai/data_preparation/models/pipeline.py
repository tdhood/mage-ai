from mage_ai.data_cleaner.shared.utils import clean_name
from mage_ai.data_preparation.models.block import Block
import os
import shutil
import yaml

PIPELINES_FOLDER = 'pipelines'
PIPELINE_CONFIG_FILE = 'metadata.yaml'


class Pipeline:
    def __init__(self, uuid, repo_path):
        self.repo_path = repo_path
        self.uuid = uuid
        self.load_config_from_yaml()

    @property
    def config_path(self):
        return os.path.join(
            self.repo_path,
            PIPELINES_FOLDER,
            self.uuid,
            PIPELINE_CONFIG_FILE,
        )

    @property
    def dir_path(self):
        return os.path.join(self.repo_path, PIPELINES_FOLDER, self.uuid)

    @classmethod
    def create(self, name, repo_path):
        """
        1. Create a new folder for pipeline
        2. Create a new yaml file to store pipeline config
        3. Create other files: requirements.txt, __init__.py
        """
        uuid = clean_name(name)
        pipeline_path = os.path.join(repo_path, PIPELINES_FOLDER, uuid)
        if os.path.exists(pipeline_path):
            raise Exception(f'Pipeline {name} alredy exists.')
        # Copy pipeline files from template folder
        template_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'templates/pipeline',
        )
        if not os.path.exists(template_path):
            raise IOError('Could not find templates for pipeline.')
        shutil.copytree(template_path, pipeline_path)
        # Update metadata.yaml with pipeline config
        with open(os.path.join(pipeline_path, 'metadata.yaml'), 'w') as fp:
            yaml.dump(dict(name=name, uuid=uuid), fp)
        return Pipeline(uuid, repo_path)

    @classmethod
    def get_all_pipelines(self, repo_path):
        return os.listdir(os.path.join(repo_path, PIPELINES_FOLDER))

    def load_config_from_yaml(self):
        with open(self.config_path) as fp:
            config = yaml.full_load(fp) or {}
        self.name = config.get('name')
        self.block_configs = config.get('blocks', [])
        blocks = \
            [Block(c.get('name'), c.get('uuid'), c.get('type'), c.get('status'), self)
             for c in self.block_configs]
        self.blocks_by_uuid = {b.uuid: b for b in blocks}
        # breakpoint()
        for b in self.block_configs:
            block = self.blocks_by_uuid[b['uuid']]
            block.downstream_blocks = \
                [self.blocks_by_uuid[uuid] for uuid in b.get('downstream_blocks', [])]
            block.upstream_blocks = \
                [self.blocks_by_uuid[uuid] for uuid in b.get('upstream_blocks', [])]

    def to_dict(self):
        return dict(
            name=self.name,
            uuid=self.uuid,
            blocks=[b.to_dict() for b in self.blocks_by_uuid.values()],
        )

    def execute(self):
        # TODO: implement execution logic
        pass

    def add_block(self, block, upstream_block_uuids=[]):
        upstream_blocks = [self.blocks_by_uuid[uuid] for uuid in upstream_block_uuids]
        for upstream_block in upstream_blocks:
            upstream_block.downstream_blocks.append(block)
        block.upstream_blocks = upstream_blocks
        block.pipeline = self
        self.blocks_by_uuid[block.uuid] = block
        self.__save()
        return block

    def remove_block(self, block):
        if block.uuid not in self.blocks_by_uuid:
            raise Exception(f'Block {block.uuid} is not in pipeline {self.uuid}.')
        if len(block.downstream_blocks) > 0:
            downstream_block_uuids = [b.uuid for b in block.downstream_blocks]
            raise Exception(f'Blocks {downstream_block_uuids} are depending on block {block.uuid}'
                            '. Please remove the these blocks first.')
        upstream_blocks = block.upstream_blocks
        for upstream_block in upstream_blocks:
            upstream_block.downstream_blocks = \
                [b for b in upstream_block.downstream_blocks if b.uuid != block.uuid]
        del self.blocks_by_uuid[block.uuid]
        self.__save()
        return block

    def delete(self):
        pass

    def __save(self):
        with open(self.config_path, 'w') as fp:
            yaml.dump(self.to_dict(), fp)