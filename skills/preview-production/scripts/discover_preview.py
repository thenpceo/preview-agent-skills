#!/usr/bin/env python3
"""Capture public CLI help/catalog/schemas locally; no production mutations."""
import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

CORE = [
    'getCanvasContext', 'getStoryContext', 'getSceneContext', 'getShotContext',
    'listCanvasGroups', 'getTakeContext', 'getTakeProvenance', 'listTakeComments',
    'createCanvas', 'renameCanvas', 'createScene', 'updateScene',
    'batchCreateShots', 'batchUpdateShots', 'updateShot', 'assignTakeToShot',
    'getLibraryItemContext', 'createLibraryItem', 'updateLibraryItem',
    'addVariant', 'renameVariant', 'attachImageToLibraryItem',
    'attachUploadedImageToLibraryItem', 'copyLibraryItemAttachment', 'updateShotStatus',
    'linkLibraryItemToShot', 'listScripts', 'getScriptContext', 'writeScript',
    'batchGenerateImages', 'batchGenerateVideos', 'estimateGenerationCost',
    'waitForGeneration', 'saveTakeToAssets', 'createAssetFolder',
    'moveAssetsToFolder', 'updateAsset',
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', default='preview', help='Executable name or full path')
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--all-schemas', action='store_true')
    parser.add_argument('--schemas', nargs='+', help='Specific tool names instead of the core set')
    args = parser.parse_args()
    executable = shutil.which(args.cli)
    if not executable:
        parser.error('Preview CLI not found; install it or pass --cli /path/to/preview')
    args.out.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, PREVIEW_CLI_SKIP_UPDATE='1')

    def run(*arguments, as_json=True):
        command = [executable, *arguments]
        if as_json:
            command.append('--json')
        result = subprocess.run(command, capture_output=True, text=True, env=env, timeout=60)
        if result.returncode:
            raise RuntimeError('CLI command failed: ' + ' '.join(arguments) + '; ' + result.stderr.strip()[:500])
        if not as_json:
            return result.stdout
        payload = json.loads(result.stdout)
        if isinstance(payload, dict) and payload.get('ok') is False:
            raise RuntimeError('CLI returned an error for ' + ' '.join(arguments))
        return payload

    version = run('--version', as_json=False)
    (args.out / 'version.txt').write_text(version)
    (args.out / 'help.txt').write_text(run('--help', as_json=False))
    catalog = run('tools', 'list')
    (args.out / 'catalog.json').write_text(json.dumps(catalog, indent=2) + '\n')
    data = catalog.get('data', catalog)
    tools = data['tools']
    names = {tool['name'] for tool in tools}
    wanted = sorted(names) if args.all_schemas else (args.schemas or CORE)
    missing = [name for name in wanted if name not in names]
    if missing:
        parser.error('Not present in the current catalog: ' + ', '.join(missing))
    schema_dir = args.out / 'schemas'
    schema_dir.mkdir(exist_ok=True)
    for name in wanted:
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', name):
            raise ValueError('Unexpected tool name')
        schema = run('tools', 'schema', name)
        (schema_dir / (name + '.json')).write_text(json.dumps(schema, indent=2) + '\n')
    print(json.dumps(dict(tool_count=len(tools), schema_count=len(wanted), output=str(args.out.resolve()))))


if __name__ == '__main__':
    main()
