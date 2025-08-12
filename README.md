## Smoke Detection Using Yolo

### environment setup
```bash
conda create -n venv python=3.9
```
```bash
conda activate venv
```
```bash
pip install -r requirements.txt
```
### Running
#### Download uvicorn
```bash
pip install uvicorn
```
```bash
uvicorn main:app --port 3000 --workers 4
```
### testing
```bash
cd test
python testapi.py
```
