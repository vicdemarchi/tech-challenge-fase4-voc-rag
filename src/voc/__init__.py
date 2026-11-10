"""Execução local com telemetria opcional desativada."""
import os
os.environ.setdefault('HF_HUB_DISABLE_TELEMETRY','1')
os.environ.setdefault('DO_NOT_TRACK','1')
os.environ.setdefault('HF_HUB_DISABLE_UPDATE_CHECK','1')

