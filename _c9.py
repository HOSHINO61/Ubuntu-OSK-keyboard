import subprocess
repo = r'E:\DSH-Project\opd2413-keyboard'
p = repo + r'\README.md'
t = open(p, encoding='utf-8').read()

shot = '''## 截图

Quick Settings 里能看到「屏幕键盘」开关，键盘处于「小」档（WiFi 名称已打码）：

![Quick Settings 里的屏幕键盘开关](docs/images/keyboard-1.1-quick-settings.png)

三档尺寸按钮在拖动条右侧，当前档填充高亮：

![三档尺寸](docs/images/keyboard-1.1-sizes.png)

'''
anchor = '## 安装'
if '## 截图' not in t:
    t = t.replace(anchor, shot + anchor, 1)
    open(p, 'w', encoding='utf-8', newline='\n').write(t)
    print('README 已插入截图章节')

git = r'D:\tools\PortableGit\cmd\git.exe'
def run(*a):
    r = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '') + (r.stderr or '')

print(run('add', '-A'))
print(run('commit', '-q', '-m', '''docs: add screenshots of the size selector and the Quick Settings toggle

The Quick Settings shot has the WiFi SSID masked out of the Wi-Fi tile --
it is a personal network name and does not belong in a public repo.'''))
print(run('log', '-1', '--format=%h %s'))
print(run('status', '--short'))