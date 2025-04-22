#!/bin/bash
# 使用 stdbuf 禁用标准输出和标准错误流的缓冲
exec stdbuf -oL -eL python main.py
