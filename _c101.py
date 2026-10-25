import subprocess
git = r'D:\tools\PortableGit\cmd\git.exe'
repo = r'E:\DSH-Project\opd2413-keyboard'
def run(*a):
    r = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '') + (r.stderr or '')
print(run('add', '-A'))
print(run('commit', '-q', '-m', '''release: version 1.0.1, screenshots at the medium step

1.1 was too big a jump for a patch release that only adds a size selector.
Renumber the package, the docs and the tag to 1.0.1.

Screenshots are regenerated at the medium step with the Quick Settings menu
open, the SSID in the Wi-Fi tile masked by filling each row with that row's own
background colour (a plain rectangle showed a seam against the tile gradient).
Image names no longer carry a version.'''))
print(run('log', '-2', '--format=%h %s'))
print(run('tag', '-d', 'v1.1'))
print(run('tag', '-f', '-a', 'v1.0.1', '-m', '''v1.0.1: 屏幕键盘支持 小 / 中 / 大 三档尺寸

- 拖动条新增 小(0.72) / 中(0.85) / 大(0.99) 分段控件
- 实测面板占屏宽 55% / 66% / 76%（逻辑屏宽 1696px）
- 尺寸写入 ~/.config/erhai-osk/position.kf 的 [layout] size，跨登录记忆
- 支持 scale_small / scale_medium / scale_large 覆盖，改配置点按钮即生效
- 修复：GJS 下 get_groups() 返回元组导致 [layout] 覆盖始终失效
- 修复：build-deb.sh 未修正 DEBIAN 目录 0707 权限
- 文档：新增 Quick Settings 与三档按钮截图'''))
print(run('tag', '--list'))