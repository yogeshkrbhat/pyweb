from aws_cdk import core as cdk
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_eks as eks
from aws_cdk import aws_iam as iam
import requests

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class CdktestStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        vpc = ec2.Vpc(self, "kfd-vpc")
        role = iam.Role.from_role_arn(self, "Role", "arn:aws:iam::169883652261:role/kfd-test-eks-role", mutable=False)
        cluster = eks.Cluster(self, "kfd-eks", cluster_name="kfd-test", version=eks.KubernetesVersion.V1_20, vpc=vpc, default_capacity=0, masters_role=role)
        #cluster = eks.Cluster(self, "kfd-eks", version=eks.KubernetesVersion.V1_20, vpc=vpc, default_capacity=0)
        cluster.add_nodegroup_capacity("kfd-t2small-node-group", instance_types=[ec2.InstanceType("t2.small")], min_size=1, disk_size=20,)
        
        awsLoadBalancerControllerVersion = 'v2.2.0'
        awsControllerBaseResourceBaseUrl = "https://raw.githubusercontent.com/kubernetes-sigs/aws-load-balancer-controller/" + awsLoadBalancerControllerVersion + "/docs"
        awsControllerPolicyUrl = awsControllerBaseResourceBaseUrl + "/install/iam_policy.json"
        albNamespace = 'kube-system'
        albServiceAccount = cluster.add_service_account('aws-load-balancer-controller', namespace= albNamespace)

        policyJson = requests.get(awsControllerPolicyUrl).json()
        for statement in policyJson["Statement"]:
            albServiceAccount.add_to_policy(iam.PolicyStatement.from_json(statement))
        awsLoadBalancerControllerChart = cluster.add_helm_chart('AWSLoadBalancerController', 
        chart='aws-load-balancer-controller',
        repository='https://aws.github.io/eks-charts',
        namespace= albNamespace,
        release= 'aws-load-balancer-controller',
        version= '1.2.0', # mapping to v2.2.0
        wait= True,
        timeout= cdk.Duration.minutes(15),
        values= {
            "clusterName": cluster.cluster_name,
            "image": {
            "repository": "602401143452.dkr.ecr.us-east-1.amazonaws.com/amazon/aws-load-balancer-controller",
            },
            "serviceAccount": {
            "create": False,
            "name": albServiceAccount.service_account_name,
            },
            # must disable waf features for aws-cn partition
            "enableShield": False,
            "enableWaf": False,
            "enableWafv2": False,
        }
        )
                
