import subprocess, re
repo = r'E:\DSH-Project\opd2413-keyboard'
p = repo + r'\README.md'
t = open(p, encoding='utf-8').read()

start = t.index('## 截图')
end = t.index('## 安装')
new = '''## 截图

「中」档（默认）——Quick Settings 里能看到「屏幕键盘」开关，WiFi 名称已打码：

![Quick Settings 里的屏幕键盘开关（中档）](docs/images/keyboard-quick-settings.png)

「小」档：

![Quick Settings 里的屏幕键盘开关（小档）](docs/images/keyboard-quick-settings-small.png)

三档按钮在拖动条右侧，当前档填充高亮：

| 小（55%） | 中（66%） |
|---|---|
| ![小](docs/images/keyboard-sizes-small.png) | ![中](docs/images/keyboard-sizes.png) |

'''
t = t[:start] + new + t[end:]
open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('README 截图章节已重写')

git = r'D:\tools\PortableGit\cmd\git.exe'
def run(*a):
    r = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '') + (r.stderr or '')
print(run('add', '-A'))
print(run('commit', '-q', '-m', '''docs: keep the small-step screenshots as well

Replacing them with the medium ones dropped the small step from the docs; both
states are worth showing, and the two crops sit side by side in a table.'''))
print(run('log', '-2', '--format=%h %s'))