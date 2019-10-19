# 登录 API
## 请求
- 允许请求：`POST`
- Ajax示例
```
url: 'http://japi.sghen.cn/api/user/login',
type: 'POST',
dataType: "json",
contentType:'application/x-www-form-urlencoded',
data: {
    id: id,         //用户ID
    pw: pw          //用户密码
},
```

## 返回
```
{"code":1000, "msg":"登录成功"}
{"code":1002, "msg":"账号不存在"}
{"code":1003, "msg":"密码错误"}
{"code":1001, "msg":exception}      //异常捕获
```

# 用户列表 API
## 请求
- 允许请求：`GET`
- 示例：`http://japi.sghen.cn/api/user/query/<token>?请求参数`
- 可传递参数
```
page        //分页
limit       //每页显示行数
id          //根据用户ID过滤，模糊查询
authType    //根据用户权限过滤，精确查询
name        //根据用户名过滤，模糊查询
```
- 示例：
```
http://japi.sghen.cn/api/user/query/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyaWQiOiIxNTY4ODg4ODg4OCIsInVzZXJuYW1lIjoic3VwZXJfYWRtaW4iLCJhdXRoX3R5cGUiOiI5IiwianVyb3JpZCI6IjAiLCJkZXB0X2lkIjoiMCJ9.5SE9nsQAWeBCGwLj3M0ySF-aujg3y5NM7rVUTxgn_Eg?mAuthType=9&page=1&authType=0
```

## 返回
```
{"code":1000, "msg":"查询成功"}
{"code":1002, "msg":"token为空"}
{"code":1003, "msg":"token验证不通过"}
{"code":1001, "msg":exception}             //异常捕获
```

# 创建用户API
## 请求
- 允许请求：`POST`
- Ajax示例
```
url: 'http://japi.sghen.cn/api/user/create',
type: 'POST',
dataType: "json",
contentType:'application/x-www-form-urlencoded',
data: {
    id: id,
    pw: pw
    name: name,
    authType: authType,
    jurorId: jurorId,
    dept_id: dept_id,
    token: token        //非必须
},
```

## 返回
```
{"code":1000", "msg":"请求成功"}
{"code":1002", "msg":"userid已存在"}
{"code":1003", "msg":"前端参数传递不完整"}
{"code":1004", "msg":"权限不足"}
{"code":1001, "msg":exception}             //异常捕获
```

# 删除用户 API
## 请求
- 允许请求：`DELETE`
- Ajax示例
```
url: 'http://japi.sghen.cn/api/user/drop',
type: 'DELETE',
dataType: "json",
contentType:'application/x-www-form-urlencoded',
data: {
    id: id,
    token: token
},
```

## 返回
```
{"code":1000, "msg":删除用户成功"}
{"code":1002, "msg":账号权限不足"}
{"code":1003, "msg":token验证不通过"}
{"code":1004, "msg":传入的token为空"}
{"code":1001, "msg":exception"}         //异常捕获
```

# 修改用户信息 API
## 请求
- 允许请求：`PUT`
- Ajax示例
```
url: 'http://japi.sghen.cn/api/user/modify',
type: 'PUT',
dataType: "json",
contentType:'application/x-www-form-urlencoded',
data: {
    id: id,
    pw: pw
    name: name,
    authType: authType,
    jurorId: jurorId,
    dept_id: dept_id,
    token: token
},
```

## 返回
```
{"code":1000, "msg":"请求成功"}
{"code":1002, "msg":"token为空"}
{"code":1003, "msg":"token验证不通过"}
{"code":1004, "msg":"权限不足"}
{"code":1001, "msg":exception"}         //异常捕获
```