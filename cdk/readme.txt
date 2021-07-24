//Create VPC
vpc = ec2.Vpc(self, "kfd-vpc")
cluster = eks.Cluster(self, "kfd-eks", cluster_name="kfd-test", version=eks.KubernetesVersion.V1_20, vpc=vpc, default_capacity=0, masters_role="arn:aws:iam::169883652261:role/kfd-test-eks-role")
cluster.add_nodegroup_capacity("kfd-t2small-node-group", instance_types=[ec2.InstanceType("t2.small")], min_size=1, disk_size=20,)

//get config 
aws eks --region us-east-1 update-kubeconfig --name kfd-test

//Assume role
aws sts assume-role --role-arn arn:aws:iam::169883652261:role/kfd-test-eks-role --role-session-name test2

// give access to iam users
kubectl edit configmap aws-auth
Add this:
  mapUsers: '[{"userarn":"arn:aws:iam::169883652261:user/Yogesh.Bhat@knowles.com",
    "username":"yogesh","groups":["system:masters"]}, {"userarn":"arn:aws:iam::169883652261:user/Javed.Lingasur@knowles.com",
    "username":"javed","groups":["system:masters"]}]'


//Create policy
aws iam create-policy --policy-name cluster-owner-policy --policy-document file://new-policy.json

//https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/
{
    "Version": "2012-10-17",
    "Statement": {
        "Effect": "Allow",
        "Principal": { "AWS": "arn:aws:iam::169883652261:user/Javed.Lingasur@knowles.com" },
        "Action": "sts:AssumeRole"
    }
}

// update kube config
aws eks --region us-east-1 update-kubeconfig --name kfd-test

aws iam create-role --role-name kfd-test-eks-role --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name kfd-test-eks-role --policy-arn "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
aws iam list-attached-role-policies --role-name kfd-test-eks-role

export AWS_ACCESS_KEY_ID=
export AWS_SESSION_TOKEN=
export AWS_SECRET_ACCESS_KEY=

//Add role in python
role = iam.Role.from_role_arn(self, "Role", "arn:aws:iam::169883652261:role/kfd-test-eks-role", mutable=False)

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "eks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}


,
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::169883652261:user/Javed.Lingasur@knowles.com"
      },
      "Action": "sts:AssumeRole"
    }



/logs
ClusterName=kube-test
RegionName=us-east-1
FluentBitHttpPort='2020'
FluentBitReadFromHead='Off'
[[ ${FluentBitReadFromHead} = 'On' ]] && FluentBitReadFromTail='Off'|| FluentBitReadFromTail='On'
[[ -z ${FluentBitHttpPort} ]] && FluentBitHttpServer='Off' || FluentBitHttpServer='On'
curl https://raw.githubusercontent.com/aws-samples/amazon-cloudwatch-container-insights/latest/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluent-bit-quickstart.yaml | sed 's/{{cluster_name}}/'${ClusterName}'/;s/{{region_name}}/'${RegionName}'/;s/{{http_server_toggle}}/"'${FluentBitHttpServer}'"/;s/{{http_server_port}}/"'${FluentBitHttpPort}'"/;s/{{read_from_head}}/"'${FluentBitReadFromHead}'"/;s/{{read_from_tail}}/"'${FluentBitReadFromTail}'"/' | kubectl apply -f - 
