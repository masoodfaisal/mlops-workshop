import openshift as oc
import os

# Get the Openshift API URL
server = "https://" + os.environ["KUBERNETES_SERVICE_HOST"] + ":" + os.environ["KUBERNETES_SERVICE_PORT"] 

print(server)

print("Retrieving Openshift token information...")
# Get the Openshift auth token
with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as file:
    token = file.read()
# print(f"Openshift Token{token}")

print("Retrieving Openshift project information...")
# Get the current project
with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as namespace:
    project = namespace.read()
print(f"Project name: {project}")

spark_crd_name = "SparkCluster"
cluster_prefix = "spark-cluster"

if os.getenv('SPARK_CLUSTER') is None:
    with open('spark-info.txt', 'r') as sparkinfo:
        cluster_name = sparkinfo.read()
    os.environ['SPARK_CLUSTER'] = cluster_name

# Connect to openshift API server
with oc.api_server(server):
    with oc.token(token):
        with oc.project(project), oc.timeout(10*60):
            print('OpenShift client version: {}'.format(oc.get_client_version()))

            print(f"Reading cluster info from spark-info.txt...")
            with open('spark-info.txt', 'r') as file:
                cluster_name = file.read()

            print(f"Searching for SparkCluster with name {cluster_prefix}-{cluster_name}...")
            cluster_count = oc.selector(f"{spark_crd_name}/{cluster_prefix}-{cluster_name}").count_existing()
            print(f"SparkCluster found: {cluster_prefix}-{cluster_count}")

            print(cluster_count)
            if cluster_count > 0:
                print(f"Deleting cluster {cluster_prefix}-{cluster_name}")
                oc.oc_action(oc.cur_context(), "delete", cmd_args=[spark_crd_name, f"{cluster_prefix}-{cluster_name}"])
                print("SparkCluster deleted")
            else:
                print(f"Spark Cluster does not exists {cluster_name}")
