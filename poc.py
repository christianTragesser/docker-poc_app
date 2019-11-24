from pyplineCI import Pipeline, bcolors

class POC(Pipeline):
    def unit_test(self, path):
        self.pocPath = path
        self.pocVolumes = {
            self.pocPath: { 'bind': '/tmp', 'mode': 'rw'}
        }
        self.working_dir = '/tmp' 
        self.runi(image='registry.gitlab.com/christiantragesser/pypline-ci:poc', name='poc-unit', working_dir=self.working_dir,
                                     volumes=self.pocVolumes, command='pytest ./tests')

    def uat_test(self, path):
        self.pocPath = path
        self.pocVolumes = {
            self.pocPath: { 'bind': '/tmp', 'mode': 'rw'}
        }
        self.working_dir = '/tmp'
        cleanMe = []
       
        cleanMe.append(self.rund(image='local/poc_app', name='poc-app-test'))
        self.runi(image='tutum/curl:latest', name='poc-uat', working_dir=self.working_dir,
                                     volumes=self.pocVolumes, command='./tests/uat.sh poc-app-test:5000')

        self.purge_containers(cleanMe)

    def run_latest(self):
        self.localPorts = { 5000: 8888 }
        self.rund(image=self.dockerRegistry+'/poc_app:latest', name='poc-app')
        print(bcolors.HEADER+'  * Latest version of POC app accessible at http://localhost:8888'+bcolors.ENDC)

    def run_local(self):
        self.localPorts = { 5000: 8888 }
        self.rund(image='local/poc_app', name='poc-app', ports=self.localPorts)
        print(bcolors.HEADER+'  * Local instance of POC app accessible at http://localhost:8888'+bcolors.ENDC)
    
    def run_mysql(self):
        env_vars = {
            'MYSQL_ROOT_PASSWORD': 'root',
            'MYSQL_DATABASE': 'poc-db',
            'MYSQL_ROOT_HOST': '%'
        }
        command = '--sql-mode="ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"'
        return self.rund(image='mysql:5.6', name='mysql.ci.local', env_vars=env_vars, command=command)
