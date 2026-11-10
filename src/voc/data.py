"""Preparação auditável: uma avaliação por documento, sem multiplicar por itens."""
import hashlib
import html
import json
import re
from pathlib import Path
import pandas as pd

FILES = ['olist_order_reviews_dataset.csv', 'olist_orders_dataset.csv',
         'olist_order_items_dataset.csv', 'olist_products_dataset.csv']

def clean(value):
    if pd.isna(value):
        return ''
    text = html.unescape(str(value))
    text = re.sub(r'<[^>]*>', ' ', text)
    text = re.sub(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}', '[EMAIL]', text)
    text = re.sub(r'(?<!\d)(?:\+?55\s*)?\(?\d{2}\)?[\s.-]*\d{4,5}[\s.-]*\d{4}(?!\d)', '[TELEFONE]', text)
    text = re.sub(r'\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b', '[CPF]', text)
    return re.sub(r'\s+', ' ', text).strip()

def prepare(raw: Path, out: Path, evidence: Path):
    reviews = pd.read_csv(raw / FILES[0])
    audit = {'input_reviews': len(reviews), 'source_sha256': {
        f: hashlib.sha256((raw / f).read_bytes()).hexdigest() for f in FILES}}
    n = len(reviews)
    reviews = reviews.drop_duplicates().copy()
    audit['exact_duplicate_rows_removed'] = n - len(reviews)
    reviews['source_row'] = reviews.index + 2  # CSV header = line 1; logical record index
    reviews['text'] = [clean(t) + (' — ' if clean(t) and clean(c) else '') + clean(c)
                       for t,c in zip(reviews.review_comment_title, reviews.review_comment_message)]
    audit['without_text'] = int(reviews.text.eq('').sum())
    valid = reviews.review_score.isin([1,2,3,4,5]) & reviews.review_id.notna() & reviews.order_id.notna()
    audit['invalid_key_or_score'] = int((~valid).sum())
    reviews = reviews[valid & reviews.text.ne('')].copy()
    reviews['doc_id'] = ['D' + hashlib.sha256(f'{r.review_id}|{r.order_id}|{r.source_row}'.encode()).hexdigest()[:16]
                         for r in reviews.itertuples()]
    orders = pd.read_csv(raw / FILES[1], usecols=['order_id','order_status','order_purchase_timestamp',
                       'order_delivered_customer_date','order_estimated_delivery_date'])
    if orders.order_id.duplicated().any():
        raise ValueError('Chave order_id duplicada em orders; integração interrompida.')
    items = pd.read_csv(raw / FILES[2], usecols=['order_id','product_id'])
    products = pd.read_csv(raw / FILES[3], usecols=['product_id','product_category_name'])
    if products.product_id.duplicated().any():
        raise ValueError('Chave product_id duplicada em products.')
    joined = items.merge(products, on='product_id', how='left', validate='many_to_one')
    categories = joined.groupby('order_id').product_category_name.agg(
        lambda x: sorted(set(x.fillna('nao_informada')))).rename('categories')
    docs = reviews.merge(orders,on='order_id',how='left',validate='many_to_one',indicator=True)
    audit['reviews_without_order_match'] = int(docs['_merge'].eq('left_only').sum())
    docs = docs.merge(categories, on='order_id',how='left',validate='many_to_one')
    docs['categories'] = docs.categories.map(lambda x: x if isinstance(x,list) else ['nao_informada'])
    purchase = pd.to_datetime(docs.order_purchase_timestamp,errors='coerce')
    delivered = pd.to_datetime(docs.order_delivered_customer_date,errors='coerce')
    estimate = pd.to_datetime(docs.order_estimated_delivery_date,errors='coerce')
    docs['purchase_date'] = purchase.dt.strftime('%Y-%m-%d').fillna('')
    # Calendar dates: an estimate at midnight does not imply same-day delivery is late.
    docs['late_delivery'] = [None if pd.isna(a) or pd.isna(b) else bool(a.normalize()>b.normalize())
                             for a,b in zip(delivered,estimate)]
    cols = ['doc_id','review_id','order_id','source_row','review_score','text','categories','purchase_date',
            'order_status','late_delivery']
    docs = docs[cols].fillna({'order_status':'nao_informado'}).sort_values('doc_id')
    audit.update(documents=len(docs), unique_orders=int(docs.order_id.nunique()),
                 repeated_review_ids=int(docs.review_id.duplicated().sum()),
                 repeated_texts=int(docs.text.duplicated().sum()),
                 score_distribution={str(k):int(v) for k,v in docs.review_score.value_counts().sort_index().items()},
                 purchase_min=docs.loc[docs.purchase_date.ne(''),'purchase_date'].min(),
                 purchase_max=docs.purchase_date.max())
    assert docs.doc_id.is_unique and len(docs)==len(reviews)
    out.mkdir(parents=True, exist_ok=True); evidence.mkdir(parents=True,exist_ok=True)
    docs.to_json(out/'documents.jsonl',orient='records',lines=True,force_ascii=False)
    (evidence/'data_audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False),encoding='utf-8')
    return audit
