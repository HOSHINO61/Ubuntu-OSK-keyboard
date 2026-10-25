import subprocess
git = r'D:\tools\PortableGit\cmd\git.exe'
repo = r'E:\DSH-Project\opd2413-keyboard'
def run(*a):
    r = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '') + (r.stderr or '')

msg = """feat: set the three steps to 50% / 65% / 80% of the screen width

Measured against the panel size: width is roughly scale * 1310px on this
tablet's 1734px-wide logical screen, so the requested coverage maps to
0.66 / 0.86 / 1.06.  The medium step is now below the 1.00 design baseline --
the baseline stays in the px values, the steps just sit around it.

scale_medium joins scale_small / scale_large in the config overrides, and
_saveConfig() preserves all three.  The previous build only carried two of
them, so a file-tuned medium step was erased by the next position save."""
print(run('add', '-A'))
print(run('commit', '-q', '-m', msg))
print(run('log', '-3', '--format=%h %s'))
print(run('status', '--short'))