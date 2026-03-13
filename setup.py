#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化汇总系统 - 启动脚本
兼容OpenClaw调用方式
"""

import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入主模块
from main import main

if __name__ == '__main__':
    main()
