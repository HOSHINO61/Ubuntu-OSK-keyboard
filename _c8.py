import subprocess
repo = r'E:\DSH-Project\opd2413-keyboard'

p = repo + r'\scripts\erhai-osk-ext\extension.js'
t = open(p, encoding='utf-8').read()
t = t.replace('//     scale 0.99 -> ~1293x475 (76%)', '//     scale 0.99 -> 1295x491 (76%)')
open(p, 'w', encoding='utf-8', newline='\n').write(t)

p2 = repo + r'\README.md'
r = open(p2, encoding='utf-8').read()
r = r.replace('| 大 | 0.99 | 24px | 63px | ~1293×475 | **76%** |',
              '| 大 | 0.99 | 24px | 63px | 1295×491 | **76%** |')
open(p2, 'w', encoding='utf-8', newline='\n').write(r)

p3 = repo + r'\docs\屏幕键盘-方案.md'
d = open(p3, encoding='utf-8').read()
d = d.replace('| 0.99 | ~1293×475 | 76% |', '| 0.99 | 1295×491 | 76% |')
open(p3, 'w', encoding='utf-8', newline='\n').write(d)

git = r'D:\tools\PortableGit\cmd\git.exe'
def run(*a):
    res = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (res.stdout or '') + (res.stderr or '')

print(run('add', '-A'))
print(run('commit', '-q', '-m', 'docs: record the measured large-step panel size\n\n1295x491 (76%) after the 0.99 click -- replaces the estimate.'))
print(run('log', '-3', '--format=%h %s'))
print(run('log', '--oneline', 'origin/master..master'))