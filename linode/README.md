# Generating Volume Backups

In the linode/manage-volumes directory, you will find a Dockerfile for building
an image that will run as a cronjob, cloning your validator data volume every
day and deleting old backups.  See the README in that directory for more info.

Note that if you try to restore your validator data volume from a snapshot 
backup, it will fail to attach to any of your kubernetes nodes with 403 
Unauthorized error.  Linode denies this is the case, but it's definitely broken
with no fix in sight.  Instead, you'll have to create a new persistent volume, 
shut the container down, manually mount the new and backup PVs somewhere and 
finally rsync the backup to the new volume.

# Dashboard Installation

After following the main README's instructions, you can get the Kubernetes dashboard up and running by installing first the metrics server, and then the dashboard itself.  The cleanest method is via helm.  First, install the helm binary locally and then run:

  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm install -f metrics-server-params.yaml metrics-server bitnami/metrics-server
  helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
  helm install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard

# Notes

* Linode doesn't have support for resizing volumes provisioned through k8s yet: https://github.com/kubernetes/enhancements/issues/556 (doesn't look like it's going to happen anytime soon either)
