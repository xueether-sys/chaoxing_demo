import re
import getpass

# 原始脚本文件名
TARGET_PHO_AND_PWD = "login_chaoxing.py"

# 获取用户输入
username = input("请输入手机号/账号: ")
password = input("请输入密码: ")

# 读取原始脚本
with open(TARGET_PHO_AND_PWD, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 修改对应的两行（直接按行替换）
new_lines = []
for line in lines:
    if 'username.send_keys("' in line or "username.send_keys('" in line:
        # 提取前导空白（空格或制表符）
        indent = re.match(r'^\s*', line).group()
        new_lines.append(f'{indent}username.send_keys("{username}")\n')
    elif 'password.send_keys("' in line or "password.send_keys('" in line:
        indent = re.match(r'^\s*', line).group()
        new_lines.append(f'{indent}password.send_keys("{password}")\n')
    else:
        new_lines.append(line)

# 写回原文件
with open(TARGET_PHO_AND_PWD, "w", encoding="utf-8") as f:
    f.writelines(new_lines)
    print(f"✅ 账号密码已永久写入 {TARGET_PHO_AND_PWD}")