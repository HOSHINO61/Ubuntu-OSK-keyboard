import subprocess
repo = r'E:\DSH-Project\opd2413-keyboard'

# 文档：补 GJS 元组坑
p = repo + r'\docs\屏幕键盘-方案.md'
d = open(p, encoding='utf-8').read()
row = '''| 旧配置 | 没有 `[layout]` 组时按 `medium` 处理 | 老用户升级不炸 |'''
newrow = row + '''
| 读 `[layout]` 组 | **不要**用 `kf.get_groups().includes('layout')` | GJS 把 `gchar**` 出参映射成 `[["position","layout"], 2]` 元组，`includes()` 永远不匹配，覆盖值会被静默忽略。直接用 `try { kf.get_string('layout', key) } catch` 判断即可 |'''
if row in d and 'gchar**' not in d:
    d = d.replace(row, newrow, 1)
    open(p, 'w', encoding='utf-8', newline='\n').write(d)
    print('文档已补 GJS 元组坑')

git = r'D:\tools\PortableGit\cmd\git.exe'
def run(*a):
    r = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '') + (r.stderr or '')

msg = """fix: read the [layout] overrides without get_groups()

The overrides never worked.  _loadConfig() gated every get_string() on
kf.get_groups().includes('layout'), and in GJS that call does not return a
plain array: a gchar** out parameter comes back as [["position","layout"], 2],
so includes('layout') only ever compared against the outer tuple.  hasLayout
was therefore always false, all three scale_* came back null, and the defaults
were used no matter what the file said.  Verified with a standalone gjs script
against the real file:

    groups=[["position","layout"],2]     scale_small=0.72

Read the keys with try/catch instead; no group list needed.

Also record it in the design notes next to the other size pitfalls."""
print(run('add', '-A'))
print(run('commit', '-q', '-m', msg))
print(run('log', '-2', '--format=%h %s'))