import re
import json
from typing import Any, Dict

async def desensitize_data(data) -> Dict[str, Any]:
    """数据脱敏处理函数
    
    Args:
        data: 原始数据字典
        
    Returns:
        脱敏后的数据字典
    """
    if not isinstance(data, dict):
        return data
        
    # 处理用户名
    if 'username' in data and data['username']:
        username = str(data['username'])
        data['username'] = username[0] + '*' * (len(username) - 1) if len(username) > 1 else '*'
    
    # 处理邮箱
    if 'email' in data and data['email']:
        email = str(data['email'])
        parts = email.split('@')
        if len(parts) == 2:
            data['email'] = f"{parts[0][0]}***@{parts[1]}"
    
    # 处理手机号
    if 'mobile' in data and data['mobile']:
        mobile = str(data['mobile'])
        if len(mobile) >= 7:
            data['mobile'] = f"{mobile[:3]}****{mobile[-4:]}"
    
    # 处理部门信息
    if 'department' in data and data['department']:
        dept = str(data['department'])
        parts = dept.split('-')
        if len(parts) > 2:
            data['department'] = '-'.join(parts[:2]) + '-***'
    
    # 处理真实姓名
    if 'realname' in data and data['realname']:
        name = str(data['realname'])
        data['realname'] = name[0] + '*' * (len(name) - 1) if len(name) > 1 else '*'
    
    # 处理地址
    if 'address' in data and data['address']:
        addr = str(data['address'])
        # 保留省市信息
        match = re.match(r'^([^\s]+市[^\s]+)', addr)
        if match:
            data['address'] = match.group(1) + '-***'
        else:
            data['address'] = '***'
    
    # 处理密码字段
    for pwd_field in ['password', 'pwd']:
        if pwd_field in data:
            data[pwd_field] = '******'
    
    # 处理token相关字段
    for token_field in ['token', 'accesskey', 'access_token']:
        if token_field in data and data[token_field]:
            token = str(data[token_field])
            if len(token) > 10:
                data[token_field] = token[:5] + '***' + token[-2:]
    
    # 处理slice数组中的敏感信息
    if 'slice' in data and isinstance(data['slice'], list):
        for i, item in enumerate(data['slice']):
            if isinstance(item, str):
                if '@' in item:  # 邮箱
                    parts = item.split('@')
                    if len(parts) == 2:
                        data['slice'][i] = f"{parts[0][0]}***@{parts[1]}"
                elif item.isdigit() and len(item) >= 7:  # 手机号
                    data['slice'][i] = f"{item[:3]}****{item[-4:]}"
                elif len(item) > 1:  # 姓名
                    data['slice'][i] = item[0] + '*' * (len(item) - 1)
    
    # 处理多个手机号
    if 'group_concat(mobile)' in data and data['group_concat(mobile)']:
        mobiles = str(data['group_concat(mobile)']).split(',')
        masked = []
        for m in mobiles:
            m = m.strip()
            if len(m) >= 7:
                masked.append(f"{m[:3]}****{m[-4:]}")
            else:
                masked.append('***')
        data['group_concat(mobile)'] = ','.join(masked)
    
    return data


PLUGIN_INFO = {
    "name": "desensitize_data",
    "description": """desensitize_data""",
    "function": desensitize_data,
    "schema": {
        "type": "object",
        "properties": {
        },
        "required": [],
        "title": "desensitize_data"
    }
} 


# if __name__ == '__main__':
#     # 测试数据
#     test_data = {
#         "id": "1",
#         "username": "chenxu9",
#         "email": "chenxu9@jd.com",
#         "mobile": "17600123456",
#         "department": "京东集团-CCO体系-信息安全部-数据安全组",
#         "realname": "陈旭",
#         "address": "福建省厦门市杏林街道-幸福里小区1号楼2单元-门牌号码306",
#         "slice": [17600123456, "陈旭", "chenxu9@jd.com"],
#         "group_concat(mobile)": "18612345678,18810234567,18601010101,18323456789,18698765432,13167891234",
#         "password": "123456",
#         "pwd": "123456",
#         "token": "c.j.s.d.u.l.AssetRegisterListener",
#         "accesskey": "c.j.s.d.u.l.AssetRegisterListener",
#         "access_token": "c.j.s.d.u.l.AssetRegisterListener"
#     }
    
#     print("原始数据:")
#     print(json.dumps(test_data, indent=2, ensure_ascii=False))
    
#     print("\n脱敏后数据:")
#     print(json.dumps(desensitize_data(test_data), indent=2, ensure_ascii=False))
