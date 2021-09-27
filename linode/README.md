* Linode doesn't have support for resizing volumes provisioned through k8s yet: https://github.com/kubernetes/enhancements/issues/556 (doesn't look like it's going to happen anytime soon either)
* You can't snapshot at the volume level.  Instead, you need a CronJob container with a script that leverages the API to clone/delete snapshots.
* Reusing an existing volume may prove tricky.  If you get a 403 error, you'll have to figure out how to pass access tokens to the CSI driver (https://github.com/linode/linode-blockstorage-csi-driver#create-a-kubernetes-secret)
