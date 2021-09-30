import os
# task_instance = context['task_instance']

# spark_name = task_instance.xcom_pull(task_id="start-spark-cluster", key="spark_cluster")

# print(spark_name)

#/var/run/secrets/kubernetes.io/serviceaccount
with open('spark-info.txt', 'r') as namespace:
    project = namespace.read()
    
print(project)