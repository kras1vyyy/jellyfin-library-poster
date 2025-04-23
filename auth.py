import requests
import json
import os
from logger import get_module_logger

# 获取模块日志记录器
logger = get_module_logger("auth")


def authenticate(base_url, username, password):
    """
    进行Jellyfin/Emby身份验证并返回User.Id和AccessToken

    Returns:
        dict: 包含User.Id和AccessToken的字典，验证失败则返回None
    """

    url = f"{base_url}/Users/AuthenticateByName"

    payload = json.dumps({"username": username, "Pw": password})

    headers = {
        "authorization": 'MediaBrowser Client="other", Device="jellyfin-library-poster", DeviceId="123", Version="0.0.0"',
        "Content-Type": "application/json",
    }

    try:
        logger.info(f"正在连接服务器: {base_url}")
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()  # 检查HTTP错误

        data = response.json()
        auth_info = {
            "user_id": data.get("User", {}).get("Id"),
            "access_token": data.get("AccessToken"),
            "base_url": base_url,  # 同时返回base_url方便后续使用
        }

        # 验证是否成功获取了必要信息
        if auth_info["user_id"] and auth_info["access_token"]:
            logger.info(f"认证成功: 用户 {username}")
            return auth_info
        else:
            logger.error("认证成功但未能获取User.Id或AccessToken")
            return None

    except requests.exceptions.RequestException as e:
        logger.error(f"认证请求失败: {str(e)}")
        return None
    except json.JSONDecodeError:
        logger.error("无法解析服务器响应")
        return None
