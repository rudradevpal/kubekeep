# KubeKeep

With KubeKeep one can take backup of Kubernetes platform. The backup procedure is totally an automatic procedure.

## Getting Started

These instructions will give you an idea of how to deploy the project on a live system and how to use it.

### Prerequisites

To set up this platform the required Tools and Packages are:
* VM or System (This will be backup server. Min Requirements: 1vCPU, 2GB RAM)
* Kubernetes
* GitLab (To store the backup files)
* Python 2.7.x (Need to install in Backup Server to run kubekeep)
    - os
    - sys
    - time
    - json
    - shutil
    - urllib3
    - datetime
    - requests
    - ConfigParser


### Installing

1. Set Environment Variables
    - GITLAB_URL    : Gitlab URL to store Backup files
    - GITLAB_TOKEN    : Gitlab Private token
    - KUBE_URL        : Target Kubernetes URL
    - KUBE_TOKEN    : Target Kubernetes token (Should have access to all the namespaces & should be permanent)
2. If you skip step 1 put all the details in the config directory
    
## Usages
Below are the procedure to schedule auto Backup

### Scheduling Backup
1.    Go to the crontab file
    ```shell
    crontab -e
    ```
2.    Schedule main.py in crontab (Check [this guide for crontab](http://adminschoice.com/crontab-quick-reference))
3.    Now you are done your backup will be stored in the gitlab you have given.


## Built With

* [Python 2.7.x](http://www.dropwizard.io/1.0.2/docs/)

## Versioning

We use [GitHub]() for versioning. For the versions available, see the [releases on this repository](https://github.com/rudradevpal/kube-keep/releases). 

## Authors

* **Rudradev Pal** - *Server Setup & Scripting*

## License

The owner of this project is Rudradev Pal and licensed under MIT License.
