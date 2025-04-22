import os
import sys
import time
from datetime import datetime, timedelta
import json
import logging

# 强制标准输出不缓冲
sys.stdout.reconfigure(line_buffering=True)

# 配置日志立即刷新
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(stream=sys.stdout)],
)

logger = logging.getLogger("jellyfin-library-poster")

# 导入用于解析cron表达式的库
from croniter import croniter

# 导入自定义模块
import config
from gen_poster import gen_poster_workflow
from get_library import get_libraries
from get_poster import download_posters_workflow
from update_poster import upload_poster_workflow


def process_libraries():
    """
    处理所有媒体库的核心逻辑
    """
    logger.info("=" * 50)
    logger.info(f"开始执行 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    # 1. 获取媒体库列表
    libraries = get_libraries()
    if not libraries:
        logger.info("未能获取媒体库列表，任务终止")
        return

    logger.info(f"成功获取到 {len(libraries)} 个媒体库:")
    for i, library in enumerate(libraries, 1):
        logger.info(f"  {i}. {library['Name']} (ID: {library['Id']})")

    # 这里可以根据需要选择特定的媒体库
    for library in libraries:
        logger.info(f"找到媒体库: {library['Name']} (ID: {library['Id']})")
        # 2. 下载海报
        success = download_posters_workflow(library["Id"], library["Name"])
        if not success:
            logger.info(f"下载海报失败: {library['Name']} (ID: {library['Id']})")
            continue

        # 3. 生成九宫格海报
        gen_poster_workflow(library["Name"])

        # 4. 上传海报到Jellyfin
        if config.JELLYFIN_CONFIG["UPDATE_POSTER"]:  # 检查是否需要更新海报
            if library["Name"] not in config.EXCLUDE_LIBRARY:
                logger.info(f"[4/4] 上传[{library['Name']}]海报...")
                logger.info("-" * 40)
                upload_poster_workflow(library["Id"], library["Name"])
            else:
                logger.info(f"[4/4] 不更新[{library['Name']}]海报...")
                logger.info("-" * 40)
        else:
            logger.info(f"[4/4] 不更新[{library['Name']}]海报...")
            logger.info("-" * 40)

    logger.info("\n所有任务已完成")
    logger.info("=" * 50)


def main():
    """
    主函数：根据配置设置定时任务或直接执行
    """
    # 获取cron配置
    cron_expression = config.CRON

    if not cron_expression:
        logger.info("未配置cron表达式，立即执行一次")
        process_libraries()
        return

    # 验证cron表达式有效性
    try:
        # 创建一个croniter实例
        cron = croniter(cron_expression, datetime.now())
        next_run = cron.get_next(datetime)
        logger.info(f"已设置定时任务: {cron_expression}")
        logger.info(f"下次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

        # 是否立即执行一次
        run_immediately = True  # 默认首次启动立即执行一次
        if run_immediately:
            logger.info("首次启动立即执行一次")
            process_libraries()
            # 重新计算下一次执行时间
            next_run = cron.get_next(datetime)
            logger.info(f"下次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")

        # 进入定时循环
        logger.info("进入定时任务循环，按 Ctrl+C 退出")
        while True:
            # 获取当前时间
            now = datetime.now()

            # 计算等待时间（秒）
            wait_seconds = (next_run - now).total_seconds()

            # 等待到下次执行时间
            if wait_seconds > 0:
                # 不需要一直等待到下一次执行，每分钟检查一次
                if wait_seconds > 60:
                    logger.info(
                        f"等待执行，下次运行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    time.sleep(min(60, wait_seconds))
                else:
                    # 最后一分钟精确等待
                    logger.info(f"即将执行任务，等待 {wait_seconds:.2f} 秒...")
                    time.sleep(wait_seconds)
                    logger.info("执行定时任务...")
                    process_libraries()
                    # 更新下次执行时间
                    next_run = cron.get_next(datetime)
                    logger.info(
                        f"任务完成，下次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}"
                    )
            else:
                # 如果已经过了执行时间，立即执行
                logger.info("已过执行时间，立即执行...")
                process_libraries()
                # 更新下次执行时间
                next_run = cron.get_next(datetime)
                logger.info(
                    f"任务完成，下次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}"
                )

    except Exception as e:
        logger.info(f"Cron表达式无效或执行错误: {e}")
        logger.info("立即执行一次")
        process_libraries()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n程序已手动停止")
    except Exception as e:
        logger.info(f"程序运行出错: {e}")
