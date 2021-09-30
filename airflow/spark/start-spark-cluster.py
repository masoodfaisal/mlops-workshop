import openshift as oc
import os
from jinja2 import Template

print("Start OCP things...")

server = "https://" + os.environ["KUBERNETES_SERVICE_HOST"] + ":" + os.environ["KUBERNETES_SERVICE_PORT"] 
print(server)

#build from source Docker file
with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as file:
    token = file.read()
print(f"Openshift Token{token}")

#/var/run/secrets/kubernetes.io/serviceaccount
with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as namespace:
    project = namespace.read()
print(f"Project name: {project}")

cluster_name = os.environ["SPARK_CLUSTER"]

#build from source Docker file
with oc.api_server(server):
    with oc.token(token):
        with oc.project(project), oc.timeout(10*60):
            print('OpenShift client version: {}'.format(oc.get_client_version()))
            
            template_data = {"clustername": cluster_name, "project": "anz-ml"}
            applied_template = Template(open("spark-cluster.yaml").read())
            print(applied_template.render(template_data))
            oc.create(applied_template.render(template_data))
            
            with open('spark-info.txt', 'w') as file:
                file.write(f"spark-cluster-{cluster_name}")
                
#             task_instance = context['task_instance']
            # Pulls the return_value XCOM from "pushing_task"
            #task_instance.xcom_push(key="spark_cluster", value="ross")