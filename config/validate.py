import json,sys
d=json.load(open(sys.argv[1]));assert d['provider']['base_url'].startswith('https://');assert d['provider']['api_key_env'] not in d;print('valid')
