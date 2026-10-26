"""Lấy dữ liệu công khai (tầng miễn phí) từ repo học liệu narikoreanbox → data/*.json.
Chạy: python3 tools/lay_du_lieu.py [../narikoreanbox]"""
import json, re, sys, os
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', '..', 'narikoreanbox')
here = os.path.join(os.path.dirname(__file__), '..', 'data')
g = json.load(open(os.path.join(src, 'thi-thu/vocab.json')))['g']
h = open(os.path.join(src, 'ngu-phap-luyen/index.html')).read()
exv = json.loads(re.search(r'var EXV=(\{.*?\});', h).group(1))
gn = json.loads(re.search(r'var GN=(\{.*?\});', h).group(1))
out = {}
for k, pre in (('12', 'V01_'), ('34', 'V03_')):
    out[k] = [{'id': x['id'], 'ko': x['ko'], 'vi': x['vi'],
               'gn': gn.get(x['id']),
               'w': [{'p': w[1], 'm': w[2], 'ex': w[3] if len(w) > 3 else '', 'v': exv.get(w[0], '')} for w in x['w']]}
              for x in sorted((x for x in g if x['id'].startswith(pre)), key=lambda x: x['id'])]
json.dump(out, open(os.path.join(here, 'ngu-phap.json'), 'w'), ensure_ascii=False, indent=0)
print({k: len(v) for k, v in out.items()})
