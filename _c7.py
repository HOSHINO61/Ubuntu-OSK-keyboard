import subprocess
git = r'D:\tools\PortableGit\cmd\git.exe'
repo = r'E:\DSH-Project\opd2413-keyboard'
def run(*a):
    r = subprocess.run([git, '-C', repo, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '') + (r.stderr or '')

msg = """tune: bring the large step down to 0.99

1.03 rendered 1342px (79%); 0.99 lands around 1293px (76%), which is the
width that looked right on the device.  Small and medium are unchanged."""
print(run('add', '-A'))
print(run('commit', '-q', '-m', msg))
print(run('log', '-2', '--format=%h %s'))