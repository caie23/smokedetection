import time

from smokedetection import detectsmoke

import base64

from fastapi import FastAPI, Request, Response
import requests
import json

from PIL import Image

app = FastAPI()
input_image = "inputimage.jpg"
imageURL = False

# 解析请求
async def parse_request(req) -> dict:
    """解析请求"""
    req = await req.json()
    return req

# 解析图片
async def parseimg(_param):
    if "imageBase64" in _param.keys() and _param["imageBase64"] is not None and len(_param["imageBase64"]) > 0:
        # 图片的64位编码字符串转换为字节码
        try:
            decoded_bytes = base64.b64decode(_param['imageBase64'])
            # img = Image.open(io.BytesIO(base64.urlsafe_b64decode(_param['imageBase64'])))
            # img = img.rotate(-90)
            # img.save(input_image)
        except Exception as exc:
            raise Exception(f'图片64位编码错误, reason: {exc}')
        # 写入图片文件
        with open(input_image, "wb") as f:
            f.write(decoded_bytes)
    elif "imageUrl" in _param.keys():
        imageURL = True
        try:
            img = Image.open(requests.get(_param['imageUrl'], stream = True).raw)
            img.save(input_image)
        except Exception as exc:
            raise Exception(f'图片URL错误, reason: {exc}')
    else:
        raise Exception(f"图片和图片地址字段不存在！")


@app.post("/detect")
async def detect(req: Request) -> Response:
    """检测接口"""

    _param = await parse_request(req)
    # _param = param.copy()

#     # 是否画框
#     drawFrame = False
#     if 'analysisRule' in _param.keys() and 'drawFrame' in _param['analysisRule'].keys():
#         drawFrame = _param['analysisRule']['drawFrame']

    return_result = {'code':None,
                    'message':None,
                    'data':None}

    try:
        await parseimg(_param)
    except Exception as exc:
        reason = f"图片解析失败: {exc}"
        return_result['code']=1
        return_result['message']=reason
        return Response(
            content=json.dumps(return_result),
            media_type="application/json"
        )

    # 检测
    try:
        start = time.time()
        result = detectsmoke('v8best.onnx', input_image)  # list of json
        print(f"inference time: {time.time()-start}")
        return_result['code']=0

        if len(result) > 0:
            # 原始图片URL（如果请求图片为URL形式）
            if imageURL:
                for res in result:
                    res['imgUrl'] = _param['imageUrl']

            # 检测置信度是否超过请求参数的置信度
            return_result['message'] = "未检测到吸烟"
            for res in result:
                if res['score'] >= _param['analysisRule']['---score']:
                    res['analysisType'] = 1
                    return_result['message'] = "检测到吸烟！"
            return_result['data'] = result
        else:
            return_result['message'] = "未检测到吸烟"
        return Response(
            content=json.dumps(return_result),
            media_type="application/json"
        )
    except Exception as exc:
        reason = f"识别失败, reason: {exc}"
        return_result['code']=1
        return_result['message'] = reason
        return Response(
            content=json.dumps(return_result),
            media_type="application/json"
        )
