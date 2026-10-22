#!/usr/bin/env python3
"""Run the same KiBot phases locally and in CI, using pinned optional containers."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys


def phases(major: int, variant: str, revision: str, config: str, costs=False):
    if major not in (9, 10):
        raise ValueError('Choose KiCad 9 or 10')
    common = ['-c', config, '-g', f'variant={variant}', '-E', f'REVISION={revision}']
    if variant not in ('DRAFT', 'PRELIMINARY', 'CHECKED', 'RELEASED'):
        common += ['-d', 'Variants']
    if costs:
        return [common + ['-s', 'erc,drc,draw_fancy_stackup', '-E',
                          'KICOST_CONFIG=kibot_yaml/kicost_config_local.yaml', 'xlsx_bom']]
    if variant == 'DRAFT':
        return [common + ['-s', 'draw_fancy_stackup,erc,drc', '--log', 'kibot_run.log', 'draft_group'],
                common + ['-s', 'set_text_variables,draw_fancy_stackup,erc,drc', '--log',
                          'kibot_run_readme.log', 'md_readme']]
    skip = ['-s', 'erc,drc'] if variant == 'PRELIMINARY' else []
    return [common + ['-s', 'all', '--log', 'kibot_run_notes.log', 'notes'],
            common + skip + ['--log', 'kibot_run.log', f'all_group_k{major}']]


def container_image(major: int, build=True):
    tools = json.loads(Path(__file__).with_name('toolchains.json').read_text())
    config = tools[str(major)]
    if 'image' in config:
        image = config['image']
        if not re.fullmatch(r'ghcr.io/inti-cmnb/kicad9_auto_full@sha256:[0-9a-f]{64}', image):
            raise ValueError('Container image must be pinned by SHA256 digest')
        return image
    base = config['base_image']
    if not re.fullmatch(r'ghcr.io/inti-cmnb/kicad(?:9|10)_auto_full@sha256:[0-9a-f]{64}', base):
        raise ValueError('Container image must be pinned by SHA256 digest')
    directory = Path(__file__).with_name('container')
    fingerprint = hashlib.sha256(json.dumps(config, sort_keys=True).encode())
    for file in sorted([*directory.iterdir(), *(directory.parent.parent / 'fonts').glob('*')]):
        if file.is_file():
            fingerprint.update(file.name.encode() + b'\0' + file.read_bytes())
    image = f'kicad-port/kibot:{config["kicad"]}-{fingerprint.hexdigest()[:16]}'
    if build and subprocess.run(['docker', 'image', 'inspect', image], stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL).returncode:
        subprocess.run(['docker', 'build', '--platform', 'linux/amd64',
                        '--build-arg', f'BASE_IMAGE={base}',
                        '--build-arg', f'KICAD_VERSION={config["kicad"]}',
                        '--build-arg', f'KICAD_SHA256={config["sha256"]}',
                        '-t', image, '-f', str(directory / 'Dockerfile'), str(directory.parent.parent)], check=True)
    return image


def container_prefix(root: Path, major: int, network: str, build=True):
    image = container_image(major, build=build)
    command = ['docker', 'run', '--rm', '--platform', 'linux/amd64', '--network', network]
    if hasattr(os, 'getuid'):
        command += ['--user', f'{os.getuid()}:{os.getgid()}']
    command += ['-e', 'HOME=/tmp/kibot-user', '-e', 'XDG_CONFIG_HOME=/tmp/config',
                # KiCad honours XDG_CACHE_HOME; KiBot 1.9.2 resolves embedded
                # worksheets through ~/.cache. Both must address the same cache.
                '-e', 'XDG_CACHE_HOME=/tmp/kibot-user/.cache', '-e', 'XDG_DATA_HOME=/tmp/data',
                '-e', 'KICAD_CONFIG_HOME=/tmp/config/kicad',
                '--mount', f'type=bind,source={root},target=/work', '-w', '/work', image]
    if major == 9:
        setup = Path(__file__).with_name('container').joinpath('entrypoint.sh').read_text()
        command += ['sh', '-c', setup, 'port-container', 'kibot']
    else:
        command += ['kibot']
    return command


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--major', type=int, choices=(9, 10))
    parser.add_argument('-v', '--variant', default='DRAFT')
    parser.add_argument('--version', dest='revision', default='')
    parser.add_argument('--config', default='kibot_yaml/kibot_main.yaml')
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--container', action='store_true')
    parser.add_argument('--network', choices=('none', 'bridge'), default='none',
                        help='Enable bridge only when an output must download external assets')
    parser.add_argument('--costs', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    root = args.project.resolve(strict=True)
    major = args.major
    if not args.container:
        cli = os.environ.get('KICAD_CLI', 'kicad-cli')
        version = subprocess.check_output([cli, 'version'], text=True).strip()
        actual = int(version.split('.')[0])
        if major and major != actual:
            parser.error(f'Selected KiCad {major}, but kicad-cli is {version}')
        major = actual
    elif not major:
        parser.error('--container requires --major 9 or 10')
    revision = args.revision
    if not revision:
        helper = root / 'kibot_resources/scripts/get_changelog_version.py'
        revision = subprocess.check_output([sys.executable, str(helper), '-f', str(root / 'CHANGELOG.md')], text=True).strip()
    prefix = container_prefix(root, major, args.network, build=not args.dry_run) if args.container else ['kibot']
    for phase in phases(major, args.variant, revision, args.config, args.costs):
        command = prefix + phase
        print(shlex.join(command), flush=True)
        if not args.dry_run:
            subprocess.run(command, cwd=root, check=True)


if __name__ == '__main__':
    main()
