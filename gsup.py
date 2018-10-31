import subprocess

config = yaml.safe_load(open("config/config.yml"))
dlPath = config['downloads']['downloadpath']
#gsbucket = config['gsbucket']['src']


def remote(args):
    remoteoptions = ["gsutil", "-m", "cp", "-R", filePath]
    remoteoptions.append(args)
    subprocess.call(remoteoptions)

filePath = dlPath + 'master.csv'
remote(gsbucket + '/' + filePath)
