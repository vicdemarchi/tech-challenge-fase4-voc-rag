"""Modelo GGUF oficial opcional para backend llama.cpp (sem Ollama)."""
import hashlib
from pathlib import Path
import urllib.request
p=Path('models/qwen2.5-3b-instruct-q4_k_m.gguf');p.parent.mkdir(exist_ok=True)
url='https://huggingface.co/Qwen/Qwen2.5-3B-Instruct-GGUF/resolve/main/qwen2.5-3b-instruct-q4_k_m.gguf'
expected='626b4a6678b86442240e33df819e00132d3ba7dddfe1cdc4fbb18e0a9615c62d'
temporary=p.with_suffix('.download')
print('Baixando modelo oficial (~2 GB)...')
urllib.request.urlretrieve(url,temporary)
with temporary.open('rb') as f: checksum=hashlib.file_digest(f,'sha256').hexdigest()
if checksum!=expected:
    raise ValueError('Hash diferente do modelo validado. Verifique a versão da origem antes de usar o arquivo .download.')
temporary.replace(p)
print('Modelo validado:',p,'SHA-256:',checksum)
