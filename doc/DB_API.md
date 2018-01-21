## 接口文档

注：如无特别说明，请求方式均默认POST

### 用户操作接口
#### 1. 添加用户
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | userAdd | 添加用户 |
| 入参1 | request_id | 99 |
| 入参2 | msg_body | 用户信息(json格式: {"name": "xx", "gender": "x"}) |

#### 2. 通过json文件批量添加用户
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | addUsersFromFile | 通过json文件批量添加用户 |
| 入参1 | request_id | 99 |
| 入参2 | json_file | 多个用户信息，json文件格式参考 [批量添加示例文件](batch_add_example.json) |

#### 3. 删除用户
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | userDel | 删除多个用户 |
| 入参1 | request_id | 99 |
| 入参2 | user_ids | 要删除的用户id列表(json格式: [1,2,3]) |

#### 4. 修改用户
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | userUpdate | 修改用户信息 |
| 入参1 | request_id | 99 |
| 入参2 | msg_body | 用户信息(json格式, 同userAdd接口，需传入用户id) |

#### 5. 查询用户
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | userSelectAll | 分页查询用户信息 |
| 入参1 | request_id | 99 |
| 入参2 | page | 页数 |
| 入参3 | page_size | 每页个数 |
| 入参4 | conditions | 查询过滤条件（json格式，过滤字段名为数据库表字段名）<br/>该参数为空，默认查询所有用户 |

#### 6. 根据用户id查询
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | getUserById | 根据id查询用户信息 |
| 入参1 | request_id | 99 |
| 入参2 | user_id | 用户id |


### 链接操作接口
#### 1. 添加链接
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | linkAdd | 添加链接 |
| 入参1 | request_id | 99 |
| 入参2 | msg_body | 链接信息(json格式: {"name": "xx", "link": "http://xxx"}) |

#### 2. 通过json文件批量添加链接
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | addLinksFromFile | 通过json文件批量添加链接 |
| 入参1 | request_id | 99 |
| 入参2 | json_file | 多个链接信息，json文件格式参考 [批量添加示例文件](batch_add_example.json) |

#### 3. 删除链接
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | linkDel | 删除多个链接 |
| 入参1 | request_id | 99 |
| 入参2 | link_ids | 要删除的链接id列表(json格式: [1,2,3]) |

#### 4. 修改链接
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | linkUpdate | 修改链接信息 |
| 入参1 | request_id | 99 |
| 入参2 | msg_body | 链接信息(json格式, 同linkAdd接口，需传入链接id) |

#### 5. 查询链接
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | linkSelectAll | 分页查询链接信息 |
| 入参1 | request_id | 99 |
| 入参2 | page | 页数 |
| 入参3 | page_size | 每页个数 |
| 入参4 | conditions | 查询过滤条件（json格式，过滤字段名为数据库表字段名）<br/>该参数为空，默认查询所有链接 |


### 类别操作接口
#### 1. 增加类别
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | categoryAdd | 添加类别 |
| 入参1 | request_id | 99 |
| 入参2 | msg_body | 类别信息(json格式: {"name": "视频"}) |

#### 2. 删除类别
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | categoryDel | 删除1个或多个类别 |
| 入参1 | request_id | 99 |
| 入参2 | category_ids | 要删除的类别id列表(json格式: [1,2,3]) |

#### 3. 修改类别
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | categoryUpdate | 修改类别信息 |
| 入参1 | request_id | 99 |
| 入参2 | msg_body | 链接信息(json格式, {"id": 1, "name": "xxxx"}, 必须传入id和name) |

#### 4. 查询类别
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | categorySelectAll | 分页查询类别信息 |
| 入参1 | request_id | 99 |
| 入参2 | page | 页数 |
| 入参3 | page_size | 每页个数 |
| 入参4 | conditions | 查询过滤条件（json格式，过滤字段名为数据库表字段名）<br/>该参数为空，默认查询所有类别 |


### 其他操作
#### 1. 查询某用户保存的所有链接
| 定义 | 值 | 备注 |
| --- | --- | --- |
| 接口 | links | 分页查询某个用户自己保存的链接信息 |
| 入参1 | 