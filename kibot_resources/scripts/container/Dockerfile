# Exact desktop KiCad + immutable KiBot engine; built locally, never published.
ARG BASE_IMAGE=ghcr.io/inti-cmnb/kicad10_auto_full@sha256:7b720dc99b2775e4f4133f06887cf9a53c85a8403438d6684ecf0916d124f52a
FROM ${BASE_IMAGE}
ARG KICAD_VERSION
ARG KICAD_SHA256
COPY scripts/container/prepare.py /opt/port/
RUN /usr/bin/python3 /opt/port/prepare.py "$KICAD_VERSION" "$KICAD_SHA256"
COPY scripts/container/requirements.txt /opt/port/
COPY fonts/ /usr/local/share/fonts/port/
RUN /opt/kicad/AppRun python3.11 -m venv --without-pip --system-site-packages /opt/kibot-env \
 && /opt/kibot-env/bin/python -c "import sys; sys.path.insert(0, '/opt/port/pip-25.1.1-py3-none-any.whl'); from pip._internal.cli.main import main; sys.exit(main(['install','--no-cache-dir','/opt/port/pip-25.1.1-py3-none-any.whl']))" \
 && /opt/kibot-env/bin/python -m pip install --no-compile --no-cache-dir setuptools==78.1.0 wheel==0.45.1 \
 && /opt/kibot-env/bin/python -m pip install --no-build-isolation --no-compile --no-cache-dir -r /opt/port/requirements.txt \
 && cp -a /opt/port/engine/. /opt/kibot-env/lib/python3.11/site-packages/ \
 && printf 'import os; os.environ["PATH"] = "/opt/port/bin:/opt/kibot-env/bin:" + os.environ["PATH"]; os.environ["SHARUN_ALLOW_LD_PRELOAD"] = "1"\n' > /opt/kibot-env/lib/python3.11/site-packages/port_paths.pth \
 && /opt/kibot-env/bin/python /opt/port/prepare.py entrypoints \
 && rm -rf /opt/port/engine /opt/port/pip-25.1.1-py3-none-any.whl \
 && /opt/kicad/bin/kicad-cli version
COPY scripts/container/entrypoint.sh /opt/port/entrypoint.sh
COPY scripts/container/patch_kibot.py /opt/port/patch_kibot.py
RUN chmod +x /opt/port/entrypoint.sh && /opt/kibot-env/bin/python /opt/port/patch_kibot.py
ENV SHARUN_ALLOW_LD_PRELOAD=1
ENV PATH="/opt/port/bin:/opt/kibot-env/bin:/opt/kicad/bin:${PATH}" PYTHONDONTWRITEBYTECODE=1
ENV KICAD9_SYMBOL_DIR=/opt/kicad/share/kicad/symbols KICAD10_SYMBOL_DIR=/opt/kicad/share/kicad/symbols
ENV KICAD9_FOOTPRINT_DIR=/opt/kicad/share/kicad/footprints KICAD10_FOOTPRINT_DIR=/opt/kicad/share/kicad/footprints
ENV KICAD9_3DMODEL_DIR=/opt/kicad/share/kicad/3dmodels KICAD10_3DMODEL_DIR=/opt/kicad/share/kicad/3dmodels
ENTRYPOINT ["/opt/port/entrypoint.sh"]
CMD ["kibot", "--version"]
