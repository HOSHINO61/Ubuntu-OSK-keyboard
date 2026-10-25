import subprocess
repo = r'E:\DSH-Project\opd2413-keyboard'
p = repo + r'\README.md'
t = open(p, encoding='utf-8').read()

start = t.index('## 截图')
end = t.index('## 安装')
new = '''## 截图

「中」档（默认）——Quick Settings 里能看到「屏幕键盘」开关，WiFi 名称已打码：

![Quick Settings 里的屏幕键盘开关（中档）](docs/images/keyboard-quick-settings.png)

三档尺寸（按钮在拖动条右侧，当前档填充高亮）：

| 小（55%） | 中（66%） | 大（76%） |
|---|---|---|
| ![小](docs/images/keyboard-sizes-small.png) | ![中](docs/images/keyboard-sizes.png) | ![大](docs/images/keyboard-sizes-large.png) |

另外两档的全屏截图：[小档](docs/images/keyboard-quick-settings-small.png) · [大档](docs/images/keyboard-quick-settings-large.png)

'''
t = t[:start] + new + t[end:]
open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('README 已加「大」档')

git = r'D:\tools\PortableGit\cmd\git.exe'
def run(*a):
    r = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '') + (r.stderr or '')
print(run('add', '-A'))
print(run('commit', '-q', '-m', '''docs: add the large-step screenshots

Both crops now sit in one table so the three steps can be compared at a glance.
The keyboard is 1295 logical px wide at this step; the crop box is derived from
that (physical = 2x logical) rather than from a dark-pixel scan -- the scan kept
grabbing the dock and the top bar.'''))
print(run('log', '-1', '--format=%h %s'))