"""Integração real do Streamlit: carregamento, validação de formulário e recusa."""
import json
from pathlib import Path
from streamlit.testing.v1 import AppTest
at=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=120).run()
assert not at.exception, str(at.exception)
assert at.metric[0].value=='42.687'
at.text_area[0].set_value('Qual é a capital da França?')
at.button[0].click().run()
assert not at.exception
assert any('fora do escopo' in x.value for x in at.warning)
at.multiselect[0].set_value([])
at.button[0].click().run()
assert any('pelo menos uma nota' in x.value for x in at.warning)
Path('evidence/interface_test.json').write_text(json.dumps({'method':'Streamlit AppTest com base real e configuração local; sem inferência generativa neste teste',
 'checks':{'initial_load':True,'document_count':True,'out_of_scope_message':True,'empty_scores_validation':True},
 'visual_browser_check':False,'note':'Renderização em navegador não validada neste ambiente; revisar no Windows antes de gravar.'},indent=2,ensure_ascii=False))
print('4 verificações da interface passaram.')
