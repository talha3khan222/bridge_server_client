import os
from typing import List, Dict, Any


# Declarations
class BaseConfig:
    _config_file_path = os.path.join(os.getcwd(), '.config')
    _server_ip = "3.231.203.30"
    _server_address = f"http://{_server_ip}/config"
    _key_value_delimiter = "="
    _block_delimiter = "---"

    def _assert_configuration_block(self, block: Dict[str, Any], block_level: int):
        needed_fields = ["IDENTIFIER", "STREAM_ADDRESS"]
        for field in needed_fields:
            assert block.get(field), f"'Config File Error: Block {block_level}: {field}' is required"

    def _process_line_text(self, text: str):
        return text.strip("\n").strip(" ")

    def _process_configuration_blocks(self, line_items: List[str]):
        config_blocks = []
        block_items = {}
        for item in line_items:
            item = self._process_line_text(item)
            if item == self._block_delimiter:
                self._assert_configuration_block(block_items, len(config_blocks) + 1)
                config_blocks.append(block_items.copy())
                block_items.clear()
                continue
            key, value = (i.strip() for i in item.split(self._key_value_delimiter, 1))
            block_items[key] = value
        if block_items:
            config_blocks.append(block_items.copy())
        return config_blocks
