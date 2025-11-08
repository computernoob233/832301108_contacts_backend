# 832301108_contacts_backend

这是一个基于 Flask 的通讯录后端 API，支持 CRUD 操作。

## 功能
- GET /contacts：获取所有联系人
- POST /contacts：添加新联系人
- PUT /contacts/<id>：更新联系人
- DELETE /contacts/<id>：删除联系人

## 技术栈
- Python 3.12
- Flask
- Flask-CORS

## 部署方式
1. 克隆代码
2. 安装依赖：`pip install -r requirements.txt`
3. 启动服务：`python main.py`
4. 访问：`http://localhost:5000/contacts`
