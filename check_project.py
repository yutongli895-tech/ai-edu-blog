import os
import sys
import subprocess

def check_hugo():
    print("--- 检查 Hugo 环境 ---")
    try:
        result = subprocess.run(["hugo", "version"], capture_output=True, text=True)
        print(f"[OK] Hugo 已安装: {result.stdout.strip()}")
    except FileNotFoundError:
        print("[ERROR] 未找到 Hugo 命令，请确保已添加至环境变量。")

def check_structure():
    print("\n--- 检查项目结构 ---")
    conflict_configs = ["config.toml", "config.yaml", "config.json"]
    for cfg in conflict_configs:
        if os.path.exists(cfg):
            print(f"[WARNING] 发现冲突配置文件: {cfg}。建议删除，只保留 hugo.toml")

    paths = [
        "hugo.toml",
        "themes/PaperMod",
        "layouts/partials/extend_head.html",
        "content/posts"
    ]
    
    for path in paths:
        if os.path.exists(path):
            print(f"[OK] 找到路径: {path}")
        else:
            print(f"[MISSING] 缺失关键路径: {path}")
            if "extend_head.html" in path:
                print("    提示: 请确保 layouts 文件夹在项目根目录下，而不是 themes 目录下。")

def check_config_content():
    print("\n--- 检查 hugo.toml 配置内容快照 ---")
    if not os.path.exists("hugo.toml"):
        return

    with open("hugo.toml", "r", encoding="utf-8") as f:
        lines = f.readlines()
        content = "".join(lines)
        
        print(">>> 关键配置行预览:")
        found_theme = False
        for line in lines:
            stripped = line.strip()
            if "theme =" in stripped:
                print(f"    [FOUND] {stripped}")
                found_theme = True
            if "enabled =" in stripped or "subtitle =" in stripped:
                print(f"    {stripped}")

        if "\\" + "[" in content:
            print("[CRITICAL] 仍然发现非法反斜杠 '\\['！请手动删除。")
        
        if not found_theme:
            print("[ERROR] 配置文件中完全缺失 theme 定义！请添加 theme = \"PaperMod\"")
        elif 'theme = "PaperMod"' not in content and "theme = 'PaperMod'" not in content:
            print("[ERROR] theme 名称指定错误，应为 \"PaperMod\"")
        else:
            print("[OK] 主题配置检查通过。")

def check_css_injection():
    print("\n--- 检查样式注入内容 ---")
    path = "layouts/partials/extend_head.html"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            if "<style>" in content and "body::before" in content:
                print("[OK] extend_head.html 包含有效的样式代码。")
            else:
                print("[WARNING] extend_head.html 内容似乎不完整。")

if __name__ == "__main__":
    print("=== AI 语文教育项目深度诊断工具 ===\n")
    check_hugo()
    check_structure()
    check_config_content()
    check_css_injection()
    print("\n诊断完成。")
    print("如果看到效果没变，请尝试执行命令: hugo server --disableFastRender --ignoreCache")