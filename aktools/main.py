# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/9/16 20:05
Desc: 主程序入口
"""
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import akshare
import aktools
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from aktools.core.api import app_core, templates
from aktools.datasets import get_favicon_path, get_homepage_html
from login import app_user_login
from aktools.utils import get_latest_version

favicon_path = get_favicon_path(file="favicon.ico")
html_path = get_homepage_html(file="homepage.html")


app = FastAPI(
    title="欢迎来到为 AKShare 打造的 HTTP API 文档",
    description="AKTools 是 AKShare 的 HTTP API 工具, 主要目的是使 AKShare 的数据接口部署到服务器从而通过 HTTP 访问来获取所需要的数据",
    version=akshare.__version__,
    redoc_url=None,
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> FileResponse:
    return FileResponse(favicon_path)


@app.get("/", tags=["主页"], description="主要展示网站首页", summary="网站首页")
async def get_homepage(request: Request):
    return templates.TemplateResponse(
        "homepage.html",
        context={
            "request": request,
            "ip_address": request.headers["host"],
            "ak_current_version": akshare.__version__,
            "at_current_version": aktools.__version__,
            "ak_latest_version": get_latest_version("akshare"),
            "at_latest_version": get_latest_version("aktools"),
        },
    )


@app.get("/version", tags=["版本"], description="获取 AKTools 和 AKShare 的版本", summary="获取开源库版本")
async def get_version():
    return {
            "ak_current_version": akshare.__version__,
            "at_current_version": aktools.__version__,
            "ak_latest_version": get_latest_version("akshare"),
            "at_latest_version": get_latest_version("aktools"),
        }


origins = ["*"]  # 此处设置可以访问的协议，IP和端口信息

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(app_core, prefix="/api", tags=["数据接口"])
app.include_router(app_user_login, prefix="/auth", tags=["登录接口"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True, debug=True)
