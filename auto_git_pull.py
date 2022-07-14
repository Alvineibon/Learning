#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/15 17:32
# @File    : auto_pull_code.py
# @Desc    : 自动拉取仓库代码
import argparse
import pathlib
import subprocess
import threading


def exec_command(command):
    """
    执行命令
    :param command:
    :return:
    """
    return subprocess.getoutput(command)


def get_branch_name(repo_dir_path):
    """
    获取分支名称
    :param repo_dir_path: 仓库目录
    :return:
    """
    dir_path = pathlib.Path(repo_dir_path)
    git_dir_path = dir_path.joinpath(".git")

    if not dir_path.is_dir():  # 目录不存在
        return None

    if not git_dir_path.is_dir():  # .git目录不存在, 不是git仓库
        return None

    # command = "cd {} && git branch --show-current;".format(repo_dir_path)

    command = "cd {} && git branch -a;".format(repo_dir_path)
    exec_res = exec_command(command).strip()

    for line in exec_res.split('\n'):
        if "*" in line:
            return line.split('*')[-1].strip()
    return


def auto_update(root):
    """
    自动拉取指定目录下所有仓库的最新代码
    :return:
    """
    path = pathlib.Path(root)
    thread_list = []

    if not path.is_dir():
        raise ValueError('<{}> is not a valid path.')
    for sub_dir in path.iterdir():

        if not sub_dir.is_dir():  # 非目录
            continue

        branch_name = get_branch_name(sub_dir.absolute())
        if not branch_name:  # 没有获取到分支名
            continue

        command = "cd {} && git fetch --all && git reset --hard origin/{} && php artisan config:clear && php artisan queue:restart;".format(sub_dir.absolute(), branch_name)

        def update(name, cmd):
            print("项目:{}, 正在更新...".format(name))
            exec_command(cmd)
            print("项目:{}, 更新完成...".format(name))

        thread = threading.Thread(target=update, args=(sub_dir.name, command))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    print("所有项目更新完成, 共{}个...".format(len(thread_list)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto pull code')
    parser.add_argument('--root_dir', default="./", help='root directory of all projects')
    args = parser.parse_args()
    auto_update(args.root_dir)
