# Getting Started

 1. Create your Kubernetes cluster in your cloud provider's UI and follow their
    instructions to enable local administration via kubectl.
 2. Check that your cluster is available: `kubectl get nodes`
 3. To avoid certain internal DoS attacks, set cluster limits as appropriate
    in resource-quotas.yaml, then run:

    `kubectl apply -f resource-quotas.yaml`

    There are other limits out there that you may want to add, depending on your
    setup.
 4. In manifest.yaml, update the NODE_NAME_HERE and ACCESS_KEY_HERE fields.  You
    shouldn't commit either of these things to source control, if forking this
    repo, ideally.  (Provider-specific versions of this file are found in the
    linode and digitalocean directories).
 5. Deploy your pod and persistent volume to your cluster:
    `kubectl apply -f manifest.yaml`

# TCP Port Monitor

The script `common/handler.py` can be used as an AWS Lambda to monitor the
availability of the validator port (30333). It's not fancy; it merely looks
for an open port and publishes metrics to CloudWatch.  You'll need to set a
cron scheduler as a trigger to run it every minute: cron(* * * * ? *).  The
Lambda's role will need the following permissions:

 - logs:PutLogEvents
 - logs:DescribeLogStreams
 - logs:DescribeLogGroups
 - cloudwatch:PutMetricData

After the Lambda is functional, create an SNS topic with your phone number
or e-mail as a subscriber.  Lastly, add a CloudWatch Alarm that watches
the metric named "Available" and set it to notify you when the available
count goes below 1.  You should also add notifications for OK and Missing
Data, as well.

If you want to use your phone number for SMS notifications, you'll have to
add a toll-free number as an "Origination Number", which costs $2/month.
Once that has been created, you can then subscribe your number to a topic.
New accounts are sandboxed and limited to $1 worth of SMSes per month, but
that should be enough (each SMS is a fraction of a penny).

# Restoring Clusters

If you are bringing up your cluster elsewhere or any other scenario in which
you already have an existing persistent volume that you need to attach to your
pod, put the relevant details in pv.yaml and run `kubectl apply -f pv.yaml`
BEFORE you apply manifest.yaml.  The CSI plugin will automatically match this
volume with the PersistentVolumeClaim in manifest.yaml because they will match
in details (size, storage class, etc.)  NOTE: This will NOT work in Linode.
See the README file in the linode directory.

# DARP

If you also want to run DARP on your standby node, configure the anti-affinity
settings in darp.yaml (set it to match your validator labels).  You'll also
need to install the descheduler helm chart if you want DARP to be evicted in
the event of failover:

  `helm repo add descheduler https://kubernetes-sigs.github.io/descheduler/`
  `helm install descheduler --namespace kube-system --set schedule="* * * * *" descheduler/descheduler`

The default install runs a cron check every 2 mins to see if anything needs
to be evicted, but I prefer it to check every minute, so I updated the policy
after installation:

  `kubectl apply -f descheduler.yaml`

Finally, run the DARP manifest:

  `kubectl apply -f darp.yaml`

# Troubleshooting

* In the case of DNS resolution failures (particularly, if 'kubernetes.default'
  cannot be resolved, try restarting coredns:
  
  `kubectl -n kube-system rollout restart deployment/coredns`
