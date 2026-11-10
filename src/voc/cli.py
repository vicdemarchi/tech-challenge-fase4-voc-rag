import argparse
import json
import urllib.request
import zipfile
from pathlib import Path
from .data import FILES,prepare

def main():
    parser=argparse.ArgumentParser(description='Olist Voice of Customer')
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ['download','prepare','index']: sub.add_parser(name)
    ask=sub.add_parser('ask'); ask.add_argument('question'); ask.add_argument('--output'); ask.add_argument('--score',type=int,action='append',choices=range(1,6))
    args=parser.parse_args()
    if args.command=='download':
        raw=Path('data/raw'); raw.mkdir(parents=True,exist_ok=True)
        archive=raw/'olist.zip'
        urllib.request.urlretrieve('https://www.kaggle.com/api/v1/datasets/download/olistbr/brazilian-ecommerce',archive)
        with zipfile.ZipFile(archive) as z:
            for name in FILES:
                with z.open(name) as src, (raw/name).open('wb') as dst:
                    import shutil
                    shutil.copyfileobj(src,dst)
        archive.unlink(); print('Quatro CSVs oficiais baixados.')
    elif args.command=='prepare': print(json.dumps(prepare(Path('data/raw'),Path('data/processed'),Path('evidence')),indent=2,ensure_ascii=False))
    elif args.command=='index':
        from .retrieval import build
        print(json.dumps(build(Path('data/processed'),Path('artifacts')),indent=2))
    else:
        from .retrieval import Retriever
        from .rag import Pipeline,Generator
        result=Pipeline(Retriever(),Generator()).answer(args.question,scores=args.score)
        output=json.dumps(result,indent=2,ensure_ascii=False); print(output)
        if args.output: Path(args.output).write_text(output,encoding='utf-8')

if __name__=='__main__': main()
