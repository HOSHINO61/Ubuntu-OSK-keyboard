import subprocess
git = r'D:\tools\PortableGit\cmd\git.exe'
repo = r'E:\DSH-Project\opd2413-keyboard'
def run(*a):
    r = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '') + (r.stderr or '')

msg = """feat: retune the size steps and let the file override them

0.80/1.28 turned out to sit at the wrong ends of the range: the small step was
still almost as wide as the medium one, and the large one filled the screen.

Defaults are now 0.65 / 1.00 / 1.12 (panel ~850 / 1310 / 1467 px wide).

Tuning by rebuilding the package and logging out each time is not a workable
loop, so the two factors can also come from the config file:

    [layout]
    scale_small=0.60
    scale_large=1.05

_setSize() re-reads them on every click, clamped to 0.40..2.00, so retuning
needs neither a rebuild nor a re-login.  _saveConfig() copies the two keys back
verbatim -- it rewrites the whole file, and would otherwise erase the tuning
the moment it saved a position."""
print(run('add', '-A'))
print(run('commit', '-q', '-m', msg))
print(run('log', '-2', '--format=%h %s'))
print(run('status', '--short'))