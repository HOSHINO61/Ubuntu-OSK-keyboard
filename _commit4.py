import subprocess
git = r'D:\tools\PortableGit\cmd\git.exe'
repo = r'E:\DSH-Project\opd2413-keyboard'
def run(*a):
    r = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '') + (r.stderr or '')

msg = """fix: calibrate the size steps against a measured panel width

scale 0.65 rendered a panel covering 52% of the screen, not the 49% the design
note implied.  Running the proportion backwards gives a 1387px panel at 1.00
(0.52 * 1734 / 0.65); the 1310px figure came from the design notes and made
every step one size too wide.

Steps are now 0.63 / 0.82 / 1.01 for the requested 50% / 65% / 80%.

_reflow() also logs the panel width and its share of the monitor, so the next
tuning round is a log line instead of a guess:

    erhai-osk: panel 1137x419 (65% of 1734px, step medium scale 0.82)"""
print(run('add', '-A'))
print(run('commit', '-q', '-m', msg))
print(run('log', '-2', '--format=%h %s'))
print(run('status', '--short'))