from linode_api4 import LinodeClient, Volume
from datetime import datetime
import sys
from os import environ

retainNumBackups = 2 # each of these will cost you about $22/month
sourceVolume = 'pvcXXXXXXXXXXXXXXXX'

########################################

try:
    environ['LINODE_API_TOKEN']
except:
    print("LINODE_API_TOKEN env variable not set!")
    sys.exit(1)

client = LinodeClient(environ['LINODE_API_TOKEN'])

# make a new backup first
now = datetime.now()
backupName = 'backup_' + now.strftime("%Y%m%d_%H%M%S")
try:
    client.volumes(Volume.label==sourceVolume)[0].clone(backupName)
    print("Successfully cloned source volume to", backupName)
except:
    print("Could not clone source volume!")
    sys.exit(1)

# fetch list of current backup labels
volumes = client.volumes()
backup_labels = []
for v in volumes:
    if v.label.startswith('backup'):
        backup_labels.append(v.label)

# delete older backups until we only have retainNumBackups worth
backup_labels.sort(reverse=True)
while len(backup_labels) > retainNumBackups:
   match = client.volumes(Volume.label==backup_labels.pop())[0]
   print("Deleting " + match.label)
   match.delete()

