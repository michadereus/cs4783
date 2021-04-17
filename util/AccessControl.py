#%%
from flask import jsonify

def validate_api_key(api_key):
    if api_key == "cs4783ftw!":
        return True
    else:
        return False

# %%
