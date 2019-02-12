import os
import time
import logging
import urllib3
import kubekeep
import datetime
import ConfigParser

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)
log_formatter = logging.Formatter('%(asctime)-15s [%(levelname)s] %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)

logger.setLevel(logging.INFO)
logging.getLogger("requests").setLevel(logging.ERROR)


def get_configuration():
    config = dict()
    logger.info("Looking for configurations in Environment")
    required_env = ["KUBE_URL", "KUBE_TOKEN", "GITLAB_URL", "GITLAB_TOKEN"]
    config_file = "config/kubekeep.conf"

    env = os.environ.keys()

    status = all(elem in env for elem in required_env)
    if status:
        config["KUBE_URL"] = os.environ["KUBE_URL"]
        config["KUBE_TOKEN"] = os.environ["KUBE_TOKEN"]
        config["GITLAB_URL"] = os.environ["GITLAB_URL"]
        config["GITLAB_TOKEN"] = os.environ["GITLAB_TOKEN"]

        logger.info("Found configurations in Environment")
    else:
        logger.info("Configurations not found in Environment")
        logger.info("Looking for configurations in 'config/kubekeep.conf'")
        conf = ConfigParser.ConfigParser()
        try:
            conf.read(config_file)
        except Exception, e:
            logger.error("Not able to read Configuration file 'config/kubekeep.conf' - " + str(e))
            return False

        try:
            config["KUBE_URL"] = conf.get('Backup', 'KUBE_URL').rstrip("/")
            config["KUBE_TOKEN"] = conf.get('Backup', 'KUBE_TOKEN')
            config["GITLAB_URL"] = conf.get('Default', 'GITLAB_URL').rstrip("/")
            config["GITLAB_TOKEN"] = conf.get('Default', 'GITLAB_TOKEN')

            logger.info("Found configurations in 'config/kubekeep.conf'")
        except KeyError, k:
            logger.error("Key not found in configuration file 'config/kubekeep.conf' - " + str(k))
            return False
    return config


def kubekeep_backup(kube_url, kube_token, gitlab_url, gitlab_token, repo_name):
    logger.info("Starting Kubernetes Backup...")

    gitlab = kubekeep.Gitlab(gitlab_url, gitlab_token)
    backup = kubekeep.Backup(kube_url, kube_token)

    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
    backup_dir = "backup-" + str(timestamp)

    response = gitlab.create_repository(str(repo_name))
    if response["code"] not in [200, 201]:
        exit(1)
    repo_id = response["result"]

    gitlab = kubekeep.Gitlab(gitlab_url, gitlab_token)
    backup = kubekeep.Backup(kube_url, kube_token)

    data = backup.get_all_storageclasses()
    gitlab.create_file(repo_id, backup_dir + "/storageclasses.json", data["result"])

    data = backup.get_all_clusterroles()
    gitlab.create_file(repo_id, backup_dir + "/clusterroles.json", data["result"])

    data = backup.get_all_clusterrolebindings()
    gitlab.create_file(repo_id, backup_dir + "/clusterrolebindings.json", data["result"])

    response = backup.get_all_namespaces()
    if response["code"] == 200:
        for n in response["result"]:
            data = backup.get_configmaps(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/configmaps.json", data["result"])

            data = backup.get_deployments(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/deployments.json", data["result"])

            data = backup.get_secrets(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/secrets.json", data["result"])

            data = backup.get_pvc(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/pvc.json", data["result"])

            data = backup.get_ingresses(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/ingresses.json", data["result"])

            data = backup.get_services(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/services.json", data["result"])

            data = backup.get_replicationcontrollers(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/replicationcontrollers.json", data["result"])

            data = backup.get_daemonsets(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/daemonsets.json", data["result"])

            data = backup.get_networkpolicies(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/networkpolicies.json", data["result"])

            data = backup.get_statefulsets(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/statefulsets.json", data["result"])

            data = backup.get_cronjobs(n)
            gitlab.create_file(repo_id, backup_dir + "/" + str(n) + "/cronjobs.json", data["result"])


if __name__ == "__main__":
    backup_repo_name = "kubekeep"
    config = get_configuration()
    if config:
        kubekeep_backup(config["KUBE_URL"], config["KUBE_TOKEN"], config["GITLAB_URL"],
                        config["GITLAB_TOKEN"], backup_repo_name)

