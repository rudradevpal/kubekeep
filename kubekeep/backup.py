import requests
import logging
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)
log_formatter = logging.Formatter('%(asctime)-15s [%(levelname)s] %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

# file_handler = logging.FileHandler("/var/log/backup/" + str(backupDict["script_Name"]) + ".log", mode='w')
# file_handler.setFormatter(log_formatter)
# file_handler.setLevel(logging.WARNING)
# logger.addHandler(file_handler)

logger.setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.ERROR)


class Backup:
    def __init__(self, URL, token):
        self.__kube_url = str(URL)
        self.__kube_token = str(token)

    def get_all_namespaces(self):
        logger.info("Fetching all Namespaces")
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/api/v1/namespaces', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                namespaces = list()
                for i in response.json()["items"]:
                    if i["metadata"]["name"] not in ('default', 'kube-public', 'kube-system'):
                        namespaces.append(i["metadata"]["name"])
                return {"result": namespaces, "code": res_code}
            else:
                logger.error("Unable to fetch Kubernetes Namespaces - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch Kubernetes Namespaces - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_all_storageclasses(self):
        logger.info("Fetching all StorageClasses")
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/apis/storage.k8s.io/v1/storageclasses', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch Kubernetes StorageClasses - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch Kubernetes StorageClasses - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_all_clusterroles(self):
        logger.info("Fetching all ClusterRoles")
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/apis/rbac.authorization.k8s.io/v1/clusterroles', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch Kubernetes ClusterRoles - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch Kubernetes ClusterRoles - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_all_clusterrolebindings(self):
        logger.info("Fetching all ClusterRoleBindings")
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/apis/rbac.authorization.k8s.io/v1/clusterrolebindings', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch Kubernetes ClusterRoleBindings - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch Kubernetes ClusterRoleBindings - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_deployments(self, namespace):
        logger.info("Fetching Deployments for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/apis/apps/v1/namespaces/' + str(namespace) + '/deployments', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch Deployments for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch Deployments for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_configmaps(self, namespace):
        logger.info("Fetching ConfigMaps for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/api/v1/namespaces/' + str(namespace) + '/configmaps', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch ConfigMaps for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch ConfigMaps for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_secrets(self, namespace):
        logger.info("Fetching Secrets for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/api/v1/namespaces/' + str(namespace) + '/secrets', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch Secrets for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch Secrets for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_pvc(self, namespace):
        logger.info("Fetching PVC for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/api/v1/namespaces/' + str(namespace) + '/persistentvolumeclaims', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch PVC for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch PVC for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_ingresses(self, namespace):
        logger.info("Fetching Ingresses for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/apis/extensions/v1beta1/namespaces/' + str(namespace) + '/ingresses', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch Ingresses for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch Ingresses for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_services(self, namespace):
        logger.info("Fetching Services for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/api/v1/namespaces/' + str(namespace) + '/services', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch Services for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch Services for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_replicationcontrollers(self, namespace):
        logger.info("Fetching ReplicationControllers for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/api/v1/namespaces/' + str(namespace) + '/replicationcontrollers', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch ReplicationControllers for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch ReplicationControllers for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_daemonsets(self, namespace):
        logger.info("Fetching DaemonSets for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/apis/apps/v1/namespaces/' + str(namespace) + '/daemonsets', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch DaemonSets for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch DaemonSets for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_networkpolicies(self, namespace):
        logger.info("Fetching NetworkPolicies for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/apis/networking.k8s.io/v1/namespaces/' + str(namespace) + '/networkpolicies', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch NetworkPolicies for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch NetworkPolicies for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_statefulsets(self, namespace):
        logger.info("Fetching StatefulSets for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/apis/apps/v1/namespaces/' + str(namespace) + '/statefulsets', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch StatefulSets for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch StatefulSets for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def get_cronjobs(self, namespace):
        logger.info("Fetching CronJobs for Namespace " + str(namespace))
        try:
            headers = {'Authorization': 'Bearer ' + str(self.__kube_token)}
            response = requests.get(str(self.__kube_url) + '/apis/batch/v1beta1/namespaces/' + str(namespace) + '/cronjobs', headers=headers, verify=False)
            res_code = response.status_code

            if res_code == 200:
                json_data = response.json()
                return {"result": json.dumps(json_data, indent=4), "code": res_code}
            else:
                logger.error("Unable to fetch CronJobs for namespace - " + str(namespace) + " - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to fetch CronJobs for namespace - " + str(namespace) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}
