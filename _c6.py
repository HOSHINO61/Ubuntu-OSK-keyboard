import subprocess
git = r'D:\tools\PortableGit\cmd\git.exe'
repo = r'E:\DSH-Project\opd2413-keyboard'
def run(*a):
    r = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '') + (r.stderr or '')

msg = """feat: bake the measured step sizes in as defaults

0.72 / 0.85 / 1.03 are the factors that were actually accepted on the device,
and they are now the defaults, so a fresh install needs no config file:

    小  0.72 -> 927x349  (55% of the 1696px screen)
    中  0.85 -> 1120x421 (66%)
    大  1.03 -> 1342x493 (79%)

The doc also stops claiming a formula.  The panel does not scale strictly
linearly: at some sizes a text label ('Shift', 'Ctrl') outgrows the key's
min-width and widens the whole row, so the proportions drift by a percent or
two.  Tune against the numbers _reflow() logs, not against a constant."""
print(run('add', '-A'))
print(run('commit', '-q', '-m', msg))
print(run('log', '-3', '--format=%h %s'))
print(run('tag', '-f', 'v1.1'))
print(run('tag', '--list'))