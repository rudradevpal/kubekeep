import requests
import logging
import urllib3
import urllib

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


class Gitlab:
    def __init__(self, URL, token):
        self.__gitlab_url = str(URL)
        self.__gitlab_token = str(token)

    def __check_repository(self, repository_name):
        logger.info("Checking Gitlab Repository - " + str(repository_name))
        try:
            headers = {"PRIVATE-TOKEN": str(self.__gitlab_token)}
            response = requests.get(str(self.__gitlab_url) + '/api/v4/projects', headers=headers)
            res_code = response.status_code

            if res_code == 200:
                for r in response.json():
                    if str(repository_name) == str(r["name"]):
                        logger.info("Gitlab Repository " + str(repository_name) + " exists!")
                        return {"result": r["id"], "code": res_code}
                logger.info("Gitlab Repository " + str(repository_name) + " does not exists!")
                return {"result": "Does not exists", "code": 203}
            else:
                logger.error("Unable to check Gitlab Repository - Error Code " + str(res_code))
                return {"result": str(response.json()["message"]), "code": res_code}
        except Exception, e:
            logger.error("Unable to check Gitlab Repository - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def create_file(self, repository_id, file_name, content):
        logger.info("Creating " + str(file_name))
        file_name_encoded = urllib.quote_plus(file_name)
        file_name_short = str(file_name)[str(file_name).rstrip("/").rfind("/") + 1:]
        try:
            data = {"branch": "master", "author_email": "admin@kube-keep.com",
                    "author_name": "KubeKeep", "content": str(content),
                    "commit_message": str(file_name_short) + " Added!"}

            headers = {"PRIVATE-TOKEN": str(self.__gitlab_token), "Content-Type": "multipart/form-data"}
            response = requests.post(str(self.__gitlab_url) + '/api/v4/projects/' + str(repository_id) +
                                     '/repository/files/' + str(file_name_encoded),
                                     data=data, headers=headers)
            res_code = response.status_code

            if res_code == 201:
                logger.info("File " + str(file_name_short) + " created Successfully!")
                return {"result": str(file_name_short), "code": res_code}
            else:
                logger.error("Unable to create file " + str(file_name_short) + " - Error Code " + str(res_code))
                return {"result": str(response.json()), "code": res_code}
        except Exception, e:
            logger.error("Unable to create file " + str(file_name_short) + " - " + str(e))
            return {"result": "Internal Error - " + str(e), "code": 500}

    def create_repository(self, repository_name):
        result = self.__check_repository(repository_name)

        if result["code"] == 203:
            logger.info("Creating Gitlab Repository - " + str(repository_name))
            try:
                headers = {"PRIVATE-TOKEN": str(self.__gitlab_token)}
                params = {"name": str(repository_name)}
                response = requests.post(str(self.__gitlab_url) + '/api/v4/projects', headers=headers, params=params)
                res_code = response.status_code

                if res_code == 201:
                    logger.info("Gitlab Repository " + str(repository_name) + " created!")
                    return {"result": response.json()["id"], "code": res_code}
                else:
                    logger.error("Unable to create Gitlab Repository - Error Code " + str(res_code))
                    return {"result": str(response.json()["message"]), "code": res_code}
            except Exception, e:
                logger.error("Unable to create Gitlab Repository - " + str(e))
                return {"result": "Internal Error - " + str(e), "code": 500}
        else:
            return result
