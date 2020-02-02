# cloud_data_science
Cloud Data Science Env for starters


1. Get a VM from AWS/Azure/Alibaba Cloud/IBM Cloud/Any cloud service provider. make sure port 8888 is open
2. SSH and clone the repo
3. Make sure you have docker installed. such as 
```bash
$ sudo snap install docker
```

In case if you have no permission to docker 

https://stackoverflow.com/questions/48957195/how-to-fix-docker-got-permission-denied-issue

```bash
$ sudo groupadd docker
$ sudo usermod -aG docker $USER
$ sudo systemctl restart docker
$ docker run hello-world
```
4. Install python

python3
```bash
$ wget https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
$ chmod +x Anaconda3-2019.10-Linux-x86_64.sh
$ Anaconda3-2019.10-Linux-x86_64.sh
```

make sure you add it to bash
```bash
vi .bashrc
export PATH=/home/ubuntu/anaconda3/bin:$PATH
```

5. run ./scirpts/init.sh
6. go to port 8888 and check it out


Recommended : https://github.com/jakevdp/PythonDataScienceHandbook.git