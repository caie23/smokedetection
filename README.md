## 电信吸烟检测

### 环境安装
```bash
conda create -n venv python=3.9
```
```bash
conda activate venv
```
```bash
pip install -r requirements.txt
```
### 运行
#### 下载uvicorn
```bash
pip install uvicorn
```
```bash
uvicorn main:app --port 3000 --workers 4
```
### 测试
```bash
cd test
python testapi.py
```