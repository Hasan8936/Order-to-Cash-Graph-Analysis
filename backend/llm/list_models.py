import os
import sys
import json
import google.generativeai as genai

# Allow passing the key as a CLI argument for shells where setting env vars
# inline is problematic. Priority: argv[1] -> GEMINI_API_KEY env -> exit.
key = sys.argv[1] if len(sys.argv) > 1 else os.getenv('GEMINI_API_KEY')
if not key:
    print('ERROR: GEMINI_API_KEY not set (pass as arg or set env var)')
    raise SystemExit(1)

genai.configure(api_key=key)

try:
    models = genai.list_models()
    out = []
    for m in models:
        name = getattr(m, 'name', None) or getattr(m, 'model', None) or str(m)
        out.append(name)
    print(json.dumps(out, indent=2))
except Exception as e:
    print('ERROR', e)
