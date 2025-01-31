from functools import wraps
from flask import request, g, jsonify
import jwt
from app.models.user import User
from eth_utils import is_address

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')
        
        if not token:
            return jsonify({'error': '缺少token'}), 401
        
        try:
            data = jwt.decode(token, 'your-secret-key', algorithms=['HS256'])
            g.current_user = User.query.get(data['id'])
        except:
            return jsonify({'error': 'token无效或已过期'}), 401
            
        return f(*args, **kwargs)
    return decorated

def eth_address_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        eth_address = None
        if 'X-Eth-Address' in request.headers:
            eth_address = request.headers['X-Eth-Address']
        
        if not eth_address:
            return jsonify({'error': '缺少以太坊地址'}), 401
            
        if not is_address(eth_address):
            return jsonify({'error': '无效的以太坊地址'}), 401
            
        g.eth_address = eth_address
        return f(*args, **kwargs)
    return decorated 