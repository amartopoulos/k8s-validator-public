# Getting Started

 1. Create your Kubernetes cluster in your cloud provider's UI and follow their
    instructions to enable local administration via kubectl.
 2. Check that your cluster is available: `kubectl get nodes`
 3. To avoid certain internal DoS attacks, set cluster limits as appropriate
    in resource-quotas.yaml, then run:

    `kubectl apply -f resource-quotas.yaml`

    There are other limits out there that you may want to add, depending on your
    setup.
 4. Update manifest.yaml with your specific settings.
 5. Deploy your pod and persistent volume to your cluster:
    `kubectl apply -f manifest.yaml`

# Restoring Clusters

If you are bringing up your cluster elsewhere or any other scenario in which
you already have an existing persistent volume that you need to attach to your
pod, put the relevant details in pv.yaml and run `kubectl apply -f pv.yaml`
BEFORE you apply manifest.yaml.  The CSI plugin will automatically match this
volume with the PersistentVolumeClaim in manifest.yaml because they will match
in details (size, storage class, etc.)
