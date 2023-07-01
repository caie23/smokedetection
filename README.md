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
#### 安装 uvicorn
```bash
pip install uvicorn
```
```bash
uvicorn main:app --port 3000 --workers 4
```
### 测试
```bash
conda activate venv
```
```bash
cd test
```
```bash
python testapi.py
```