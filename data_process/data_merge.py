#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import glob

def merge_json_files(base_path, dev_output_file, train_output_file):
    """
    在 base_path 下的所有子文件夹中搜索 *_dev.json 和 *_train.json，
    并分别合并到 dev_output_file 和 train_output_file。

    :param base_path: 要搜索的主路径
    :param dev_output_file: 合并后的 dev.json 输出文件路径
    :param train_output_file: 合并后的 train.json 输出文件路径
    """
    # 存放合并数据的列表
    dev_data = []
    train_data = []

    # 使用 os.walk 遍历所有子目录和文件
    for root, dirs, files in os.walk(base_path):
        # root: 当前遍历到的目录
        # dirs: 该目录下的所有子目录列表
        # files: 该目录下的所有文件列表

        # 针对当前目录下的所有文件进行匹配
        for file_name in files:
            # 拼接完整文件路径
            file_path = os.path.join(root, file_name)

            # 根据文件名后缀判断
            if file_name.endswith('_dev.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)  # data应为[{}]这样的列表
                        # 判断 data 是否为列表，若是则与 dev_data 合并
                        if isinstance(data, list):
                            dev_data.extend(data)
                        else:
                            print(f"警告: 文件 {file_path} 不是列表结构，已跳过。")
                except (json.JSONDecodeError, IOError) as e:
                    print(f"警告: 无法解析 {file_path} 或读写错误: {e}")
            
            elif file_name.endswith('_train.json'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            train_data.extend(data)
                        else:
                            print(f"警告: 文件 {file_path} 不是列表结构，已跳过。")
                except (json.JSONDecodeError, IOError) as e:
                    print(f"警告: 无法解析 {file_path} 或读写错误: {e}")

    # 最后将合并后的列表分别写入 dev.json 和 train.json
    try:
        with open(dev_output_file, 'w', encoding='utf-8') as dev_out:
            json.dump(dev_data, dev_out, ensure_ascii=False, indent=4)
        with open(train_output_file, 'w', encoding='utf-8') as train_out:
            json.dump(train_data, train_out, ensure_ascii=False, indent=4)
        print(f"合并成功: {dev_output_file} 和 {train_output_file}")
    except IOError as e:
        print(f"错误: 写入输出文件时发生异常: {e}")


if __name__ == '__main__':
    """
    示例用法：
    假设 path 目录下有若干子文件夹，每个文件夹中含有 *_dev.json 与 *_train.json。
    我们想要将所有 *_dev.json 合并到 dev.json，将所有 *_train.json 合并到 train.json。
    """
    # 您可以根据实际情况修改此路径
    PATH_TO_SEARCH = "./Raw_data"

    # 指定最终输出文件的路径和名称
    DEV_OUTPUT_FILE = "./data/dev.json"
    TRAIN_OUTPUT_FILE = "./data/train.json"

    # 调用合并函数
    merge_json_files(PATH_TO_SEARCH, DEV_OUTPUT_FILE, TRAIN_OUTPUT_FILE)
