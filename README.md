### 安装依赖
```bash
    pip install -r requirements.txt
```

### 启动项目
由于没有配置虚拟环境所以直接在服务器中启动、需要在项目中启动
```bash
    nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload > uvicorn.log 2>&1 &
```