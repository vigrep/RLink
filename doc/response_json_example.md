
### 获取权限列表返回示例
#### failed
```json
{
  "action": 30,
  "resp_cd": "00",
  "resp_msg": "查询失败",
  "resp_msg_code": 12
}
```
#### success
```json
{
  "action": 30,
  "permissions": [
    {
      "description": "普通用户最基本操作",
      "permission_id": 1
    },
    {
      "description": "链接表操作权限",
      "permission_id": 2
    },
    {
      "description": "用户表操作权限",
      "permission_id": 4
    },
    {
      "description": "类别表操作权限",
      "permission_id": 8
    },
    {
      "description": "角色表操作权限",
      "permission_id": 16
    },
    {
      "description": "推荐表操作权限",
      "permission_id": 32
    }
  ],
  "resp_cd": "00",
  "resp_msg": "查询成功",
  "resp_msg_code": 12
}
```

### 添加角色返回示例
####success
```json
{
    "action": 30,
    "resp_cd": "00",
    "resp_msg": "添加成功",
    "resp_msg_code": 10
}
```
####failed
```json
{
    "action": 30,
    "resp_cd": "30",
    "resp_msg": "添加失败",
    "resp_msg_code": 10
}
```
