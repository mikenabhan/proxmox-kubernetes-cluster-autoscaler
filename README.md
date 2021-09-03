# proxmox-kubernetes-cluster-autoscaler

# Prerequisites
1. `Terraform` Appropriate for scaling a Proxmox cluster with a single variable
2. Some sort of container runtime.  (This COULD be run outside of your cluster)
3. A kubernetes cluster

## How it works

### Scaling Up
This container monitors a kubernetes cluster for unschedulable workloads due to compute and memory resources and adds additional nodes.

### Scaling Down
This continually checks the AutoScaling nodes for free compute resources.  A combination of the following will result in one AutoScaling node being cordoned, drained, then removed from the cluster.  After the node is removed, the ProxMox VM will be deprovisioned.

* 1 free vCPU
* 2GB of RAM

## Assumptions
* ASG Nodes will have 1 vCPU and 2GB of Ram
* ASG Nodes will automatically join the cluster
  * You can do this with a static image, user-data, or a provisioner such as Terraform SSH or Ansible.


## Potential Future Features
* Parameterizing scale down free resources and node size