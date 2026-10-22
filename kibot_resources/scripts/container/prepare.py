"""Build-only helpers. Verify official downloads and reuse the pinned engine."""
from pathlib import Path
import hashlib
import importlib.metadata as metadata
import importlib.util
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request

PIP_URL = 'https://files.pythonhosted.org/packages/29/a2/d40fb2460e883eca5199c62cfc2463fd261f760556ae6290f88488c362c0/pip-25.1.1-py3-none-any.whl'
PIP_SHA = '2913a38a2abf4ea6b64ab507bd9e967f3b53dc1ede74b01b0931e1ce548751af'


def download(url, dest, sha):
    with urllib.request.urlopen(url, timeout=180) as source, dest.open('wb') as target:
        shutil.copyfileobj(source, target)
    if hashlib.sha256(dest.read_bytes()).hexdigest() != sha:
        raise RuntimeError(f'SHA256 mismatch: {url}')


def extract_runtime(version, sha, work):
    archive = work / 'runtime.tar'
    name = f'kicad-{version}-x86_64.AppImage'
    download(f'https://kicad-downloads.s3.cern.ch/appimage/stable/{name}.tar', archive, sha)
    with tarfile.open(archive) as source:
        # Only extract the expected regular file, with no arbitrary paths/links.
        member = source.getmember(name)
        if not member.isfile():
            raise RuntimeError('Expected an AppImage regular file')
        with source.extractfile(member) as stream, (work / name).open('wb') as dest:
            shutil.copyfileobj(stream, dest)
    archive.unlink()
    image = work / name
    image.chmod(0o755)
    subprocess.run([str(image), '--appimage-extract'], cwd=work, check=True, stdout=subprocess.DEVNULL)
    image.unlink()
    return (work / 'squashfs-root').resolve()


def prepare(version, sha):
    if version != '10.0.7':
        raise ValueError('Unqualified KiCad version')
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        runtime = extract_runtime(version, sha, work)
        shutil.move(str(runtime), '/opt/kicad')
    download(PIP_URL, Path('/opt/port/pip-25.1.1-py3-none-any.whl'), PIP_SHA)
    engine = Path('/opt/port/engine')
    engine.mkdir()
    for module, distribution in (('kibot', 'kibot'), ('InteractiveHtmlBom', 'InteractiveHtmlBom')):
        package = Path(importlib.util.find_spec(module).origin).parent
        shutil.copytree(package, engine / package.name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        dist = metadata.distribution(distribution)._path
        shutil.copytree(dist, engine / dist.name)
    Path('/opt/port/major').write_text(version.split('.')[0])


def entrypoints():
    directory = Path('/opt/port/bin')
    directory.mkdir(exist_ok=True)
    for distribution in ('kibot', 'InteractiveHtmlBom'):
        for point in metadata.distribution(distribution).entry_points:
            if point.group != 'console_scripts':
                continue
            module, function = point.value.split(':')
            target = directory / point.name
            target.write_text(f'#!/opt/kibot-env/bin/python\nfrom {module} import {function}\nraise SystemExit({function}())\n')
            target.chmod(0o755)
    # Scripts importing pcbnew must use its bundled 3.11 interpreter too.
    for name in ('kicad-diff.py', 'kicad-diff-init.py'):
        target = directory / name
        source = Path(shutil.which(name))
        target.write_text('#!/opt/kibot-env/bin/python\n' + source.read_text().split('\n', 1)[1])
        target.chmod(0o755)



if __name__ == '__main__':
    if sys.argv[1] == 'entrypoints':
        entrypoints()
    else:
        prepare(*sys.argv[1:])
