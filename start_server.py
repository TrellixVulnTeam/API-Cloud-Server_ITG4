import os
cwd = "cd D:/Python/Cloud_Server"
os.system(cwd)
os.system(".\chalice-env\\Scripts\\activate")
os.system("chalice local --host 0.0.0.0")