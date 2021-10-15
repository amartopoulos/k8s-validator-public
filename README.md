# Getting Started

 1. Create your Kubernetes cluster in your cloud provider's UI and follow their
    instructions to enable local administration via kubectl.
 2. Check that your cluster is available: `kubectl get nodes`
 3. To avoid certain internal DoS attacks, set cluster limits as appropriate
    in resource-quotas.yaml, then run:

    `kubectl apply -f resource-quotas.yaml`

    There are other limits out there that you may want to add, depending on your
    setup.
 4. Deploy your pod and persistent volume to your cluster:
    `kubectl apply -f manifest.yaml`

# TCP Port Monitor

The script `handler.py` can be used as an AWS Lambda to monitor the
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
in details (size, storage class, etc.)
