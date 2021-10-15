# Dashboard Installation

After following the main README's instructions, you can get the Kubernetes dashboard up and running by installing first the metrics server, and then the dashboard itself.  The cleanest method is via helm.  First, install the helm binary locally and then run:

  helm repo add bitnami https://charts.bitnami.com/bitnami
  helm install -f metrics-server-params.yaml metrics-server bitnami/metrics-server
  helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
  helm install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard

# Notes

* Linode doesn't have support for resizing volumes provisioned through k8s yet: https://github.com/kubernetes/enhancements/issues/556 (doesn't look like it's going to happen anytime soon either)
* You can't snapshot at the volume level.  Instead, you need a CronJob container with a script that leverages the API to clone/delete snapshots.
* Reusing an existing volume may prove tricky.  If you get a 403 error, you'll have to figure out how to pass access tokens to the CSI driver (https://github.com/linode/linode-blockstorage-csi-driver#create-a-kubernetes-secret)
