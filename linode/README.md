# Dashboard Installation

After following the main README's instructions, you can get the Kubernetes dashboard up and running by installing first the metrics server, and then the dashboard itself:

1. `kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml`
2. Grab the URL for the latest dashboard from https://github.com/kubernetes/dashboard (see README), then kubectl apply it. 
3. Run `kubectl proxy` and access via http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/workloads?namespace=default

# Notes

* Linode doesn't have support for resizing volumes provisioned through k8s yet: https://github.com/kubernetes/enhancements/issues/556 (doesn't look like it's going to happen anytime soon either)
* You can't snapshot at the volume level.  Instead, you need a CronJob container with a script that leverages the API to clone/delete snapshots.
* Reusing an existing volume may prove tricky.  If you get a 403 error, you'll have to figure out how to pass access tokens to the CSI driver (https://github.com/linode/linode-blockstorage-csi-driver#create-a-kubernetes-secret)
