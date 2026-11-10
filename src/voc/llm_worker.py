"""Processo isolado: evita manter pesos/buffers de geração entre perguntas."""
import json
import os
import sys
from .rag import Generator

def main():
    os.environ['VOC_LLM_WORKER']='1'
    request=json.load(sys.stdin)
    generator=Generator('llamacpp')
    try:
        result=generator.complete(request['messages'],request['schema'],request['max_tokens'])
        print(json.dumps(result,ensure_ascii=False))
    finally:
        generator.close()

if __name__=='__main__': main()
