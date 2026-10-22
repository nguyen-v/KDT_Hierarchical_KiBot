#!/usr/bin/env python3
"""Run complete workflow phases on a disposable, connected four-layer test board."""
from pathlib import Path
import argparse
import json
import re
import shutil
import subprocess
import sys
import zipfile

TEMPLATE = Path(__file__).resolve().parents[2]
SOURCE = Path(__file__).with_name('validation')
# Keep maintenance tests outside the files distributed to PCB projects.
sys.path.insert(0, str(TEMPLATE / 'kibot_resources/scripts'))
import run_kibot


def install_embedded_worksheet(project):
    # A cold profile must resolve worksheets embedded in both CAD files, not
    # rely on a designer's existing cache. The payload is a synthetic worksheet.
    payload = (SOURCE / 'embedded_worksheet.txt').read_text()
    for suffix in ('kicad_pcb', 'kicad_sch'):
        path = project / f'port_validation.{suffix}'
        text = path.read_text().rstrip()
        assert text.endswith(')')
        path.write_text(text[:-1] + payload + '\n)\n')
    path = project / 'port_validation.kicad_pro'
    data = json.loads(path.read_text())
    for editor in ('pcbnew', 'schematic'):
        data.setdefault(editor, {})['page_layout_descr_file'] = 'kicad-embed://port-cache.kicad_wks'
    path.write_text(json.dumps(data, indent=2) + '\n')


def audit(project, variant, major=None):
    files = [p for p in project.rglob('*') if p.is_file() and '.git' not in p.parts]
    by_suffix = lambda suffix: [p for p in files if p.suffix.lower() == suffix]
    pdfs = by_suffix('.pdf')
    assert pdfs and all(p.read_bytes().startswith(b'%PDF') and p.stat().st_size > 1000 for p in pdfs)
    assert any('Schematic' in p.parts for p in pdfs), 'Missing schematic PDF'
    assert any('PORT-1K' in p.read_text() for p in by_suffix('.csv')), 'Missing public MPN field in BOM'
    readme = project / 'README.md'
    assert readme.stat().st_size > 1000
    manifest = json.loads((project / 'kibot_resources/project_manager/template.json').read_text())['files']
    # The generated README must refer to installed, managed logo assets.
    logos = re.findall(r'(?:src|srcset)="(Logos/[^"\s]+)"', readme.read_text())
    assert logos, 'README is missing its logo references'
    for logo in logos:
        assert logo in manifest and (project / logo).is_file(), f'Unmanaged or missing README logo: {logo}'
    if variant != 'DRAFT':
        gerbers = [p for p in files if 'Gerbers' in p.parts and p.suffix == '.gbr']
        assert len(gerbers) >= 10, 'Missing Gerber layers'
        assert by_suffix('.drl'), 'Missing drill output'
        assert any(p.stat().st_size > 1000 for p in by_suffix('.step')), 'Missing STEP model'
        pngs = list((project / 'Images').glob('*.png'))
        assert len(pngs) >= 4, 'Missing 3D renders'
        assert all(p.read_bytes().startswith(b'\x89PNG') and p.stat().st_size > 1000 for p in pngs)
        archives = by_suffix('.zip')
        assert len(archives) >= 2, 'Missing ODB++/fabrication archives'
        for archive in archives:
            with zipfile.ZipFile(archive) as stream:
                assert stream.testzip() is None and stream.namelist()
        assert any('ibom' in p.name.lower() for p in by_suffix('.html')), 'Missing interactive BOM'
        assert list((project / 'HTML').glob('*-navigate.html')), 'Missing results navigator'
        assert (project / 'index.html').is_file(), 'Missing root navigator link'
        assert (project / 'KiRI/index.html').is_file(), 'Missing KiRI history viewer'
        if major == 10:
            profile = json.loads((project / 'shadow-profile.json').read_text())['render']
            assert profile['raytrace_shadows'] is False and profile['raytrace_backfloor'] is False
            for feature in ('raytrace_anti_aliasing', 'raytrace_reflections',
                            'raytrace_refractions', 'raytrace_procedural_textures'):
                assert profile[feature] is True, f'Render quality changed: {feature}'
            assert (project / 'kibot_run.log').read_text().count('--quality user') == 4
    return {'variant': variant, 'pdfs': len(pdfs), 'pngs': len(by_suffix('.png')),
            'csvs': len(by_suffix('.csv')), 'zips': len(by_suffix('.zip')), 'status': 'PASS'}


def check_rejected_erc(workspace, major, network):
    project = workspace.resolve() / 'erc_failure'
    shutil.copytree(TEMPLATE, project, ignore=shutil.ignore_patterns('.git','__pycache__','meta'))
    for file in project.glob('*.kicad_*'):
        file.unlink()
    for file in SOURCE.glob('*.kicad_*.txt'):
        shutil.copy2(file, project / file.name.removesuffix('.txt'))
    install_embedded_worksheet(project)
    schematic = project / 'port_validation.kicad_sch'
    schematic.write_text('\n'.join(line for line in schematic.read_text().splitlines()
                                   if not line.lstrip().startswith('(wire ')) + '\n')
    prefix = run_kibot.container_prefix(project, major, network)
    with (project / 'validation.log').open('w') as log:
        result = subprocess.run(prefix + ['-c','kibot_yaml/kibot_main.yaml','-g','variant=CHECKED',
                                '-s','draw_fancy_stackup,set_text_variables,drc','netlist'],
                                cwd=project,stdout=log,stderr=subprocess.STDOUT)
    message = (project / 'validation.log').read_text()
    assert result.returncode != 0 and 'ERC' in message and 'ERROR' in message, message[-3000:]
    reports = list((project / 'Reports').glob('*erc*.rpt'))
    assert reports and 'pin_not_connected' in reports[0].read_text(), 'Expected disconnected-pin ERC report'
    return {'returncode': result.returncode, 'reason':'deliberately disconnected pins', 'status':'PASS'}


def check_public_starter(workspace, major, network):
    """Exercise the real hierarchical starter and its public reviewer worksheet."""
    project = workspace.resolve() / 'public_starter'
    shutil.copytree(TEMPLATE, project, ignore=shutil.ignore_patterns('.git','__pycache__','meta'))
    config = project / 'kibot_yaml/kibot_main.yaml'
    config.write_text(config.read_text().replace("  REVIEWER: ''", '  REVIEWER: Validation Reviewer'))
    for command in (['init','-q','-b','dev_k10'],['add','-A'],
                    ['-c','user.name=Workflow Test','-c','user.email=workflow@invalid','commit','-qm','Public template test']):
        subprocess.run(['git','-C',str(project),*command],check=True)
    prefix = run_kibot.container_prefix(project, major, network)
    with (project / 'validation.log').open('w') as log:
        for phase in run_kibot.phases(major, 'DRAFT', 'starter-trial', 'kibot_yaml/kibot_main.yaml'):
            subprocess.run(prefix + phase,cwd=project,stdout=log,stderr=subprocess.STDOUT,check=True)
    return audit_public_starter(project, major, network)


def audit_public_starter(project, major, network):
    prefix = run_kibot.container_prefix(project, major, network)
    data = json.loads((project / 'KDT_Hierarchical_KiBot.kicad_pro').read_text())
    assert data['text_variables']['REVIEWER'] == 'Validation Reviewer'
    pdf = next((project / 'Schematic').glob('*.pdf'))
    text = subprocess.check_output(prefix[:-1] + ['pdftotext', str(pdf.relative_to(project)), '-'], text=True)
    # PDF font metrics can omit word spaces during text extraction.
    normalized = re.sub(r'\s+', '', text)
    assert 'ValidationReviewer' in normalized, 'Reviewer missing from public schematic PDF'
    assert 'BlockDiagram' in normalized and 'RevisionHistory' in normalized, 'Missing hierarchical template sheets'
    return {'status': 'PASS', 'reviewer_in_project_and_pdf': True, 'hierarchical_sheets': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--major', type=int, choices=(9,10), required=True)
    parser.add_argument('--workspace', type=Path, required=True)
    parser.add_argument('--variants', nargs='+', default=['DRAFT','PRELIMINARY','CHECKED','RELEASED'])
    parser.add_argument('--network', choices=('none','bridge'), default='bridge')
    args = parser.parse_args()
    args.workspace.mkdir(parents=True, exist_ok=True)
    image = run_kibot.container_image(args.major)
    reports = []
    for variant in args.variants:
        project = args.workspace.resolve() / variant.lower()
        if project.exists():
            parser.error(f'Use a fresh test workspace: {project} already exists')
        shutil.copytree(TEMPLATE, project, ignore=shutil.ignore_patterns('.git','__pycache__','meta'))
        for file in project.glob('*.kicad_*'):
            file.unlink()
        for file in SOURCE.glob('*.kicad_*.txt'):
            shutil.copy2(file, project / file.name.removesuffix('.txt'))
        install_embedded_worksheet(project)
        for command in (['init','-q','-b','port/kicad10'],['add','-A'],
                        ['-c','user.name=Workflow Test','-c','user.email=workflow@invalid','commit','-qm','Connected workflow test']):
            subprocess.run(['git','-C',str(project),*command],check=True)
        prefix = run_kibot.container_prefix(project, args.major, args.network)
        with (project / 'validation.log').open('w') as log:
            subprocess.run(prefix + ['--version'], stdout=log, stderr=subprocess.STDOUT, check=True)
            for phase in run_kibot.phases(args.major, variant, 'port-trial', 'kibot_yaml/kibot_main.yaml'):
                # Exercise all production outputs with smaller test images.
                command = prefix + ['-E','HEIGHT=480','-E','WIDTH=480',*phase]
                if args.major == 10 and phase[-1] == 'all_group_k10':
                    # Inspect the live profile from the same isolated container
                    # that produced all four images. Keep production runs simple.
                    command = prefix[:-1] + ['sh', '-c',
                        'set -e\nkibot "$@"\ncp /tmp/config/kicad/10.0/3d_viewer.json /work/shadow-profile.json\n',
                        'profile-audit', *command[len(prefix):]]
                print(f'KiCad {args.major}: {variant}: {phase[-1]}',flush=True)
                subprocess.run(command,cwd=project,stdout=log,stderr=subprocess.STDOUT,check=True)
        reports.append(audit(project, variant, args.major))
        (args.workspace / 'summary.json').write_text(json.dumps({'major':args.major,'image':image,'checks':reports},indent=2)+'\n')
    rejected = check_rejected_erc(args.workspace, args.major, args.network)
    starter = check_public_starter(args.workspace, args.major, args.network)
    (args.workspace / 'summary.json').write_text(json.dumps({'major':args.major,'image':image,
        'checks':reports,'erc_failure_rejected':rejected,'public_starter':starter},indent=2)+'\n')
    print(json.dumps(reports),flush=True)


if __name__ == '__main__':
    main()
