# -*- coding:utf-8 -*-
# !/usr/bin/env python
"""
Date: 2022/9/27 19:05
Desc: CLI 执行入口文件
运行 `python -m aktools` 相当于运行 `python -m aktools.__main__.py`
"""
from pathlib import Path
from subprocess import run
from typing import Optional

import akshare as ak
import typer

import aktools
from aktools.utils import get_latest_version

app = typer.Typer()


def version_callback(value: bool):
    if value:
        print(
            f"当前的 AKTools 版本为：{aktools.__version__}，AKShare 版本为：{ak.__version__} \n"
            f"最新的 AKTools 版本为：{get_latest_version(package='aktools')}，AKShare 版本为：{get_latest_version(package='akshare')}"
        )
        raise typer.Exit()


@app.command()
def main(
    host: str = typer.Option("127.0.0.1", "--host", "-H", help="设置主机地址"),
    port: int = typer.Option(
        8080, "--port", "-P", min=0, max=65535, clamp=True, help="设置端口"
    ),
    auto: bool = typer.Option(False, "--auto", "-A", help="自动打开游览器，默认为不打开"),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="查看 AKTools 的版本",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    app_dir = Path(__file__).parent
    order_str = f"uvicorn main:app --host {host} --port {port} --app-dir {app_dir}"
    print(f"点击打开 HTTP API 主页：http://{host}:{port}/")
    print(f"点击打开接口导览：http://{host}:{port}/docs")
    print(f"当前的 AKTools 版本为：{aktools.__version__}，AKShare 版本为：{ak.__version__}")
    if auto:
        typer.launch(f"http://{host}:{port}/")
    run(order_str, shell=True)


if __name__ == "__main__":
    typer.run(main)
