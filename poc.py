from dind import Pipeline, bcolors

class POC(Pipeline):
    def uatTest(self, path):
        self.pocPath = path
        self.pocVolumes = {
            self.pocPath: { 'bind': '/tmp', 'mode': 'rw'}
        }
        self.working_dir = '/tmp'
        cleanMe = []
       
        cleanMe.append(self.runContainer(image='local/poc_app', name='poc-app-test'))
        self.runContainerInteractive(image='tutum/curl', name='poc-uat', working_dir=self.working_dir,
                                     volumes=self.pocVolumes, command='./tests/uat.sh poc-app-test')

        self.purgeEnvironment(cleanMe)

    def runLatest(self):
        self.localPorts = { 80: 8888 }
        self.runContainer(image=self.dockerRegistry+'/poc_app:latest', name='poc-app')
        print(bcolors.HEADER+'  * Latest version of POC app accessible at http://localhost:8888'+bcolors.ENDC)

    def runLocal(self):
        self.localPorts = { 80: 8888 }
        self.runContainer(image='local/poc_app', name='poc-app', ports=self.localPorts)
        print(bcolors.HEADER+'  * Local instance of POC app accessible at http://localhost:8888'+bcolors.ENDC)
    
    def runMYSQL(self):
        env_vars = {
            'MYSQL_ROOT_PASSWORD': 'root',
            'MYSQL_DATABASE': 'poc-db',
            'MYSQL_ROOT_HOST': '%'
        }
        command = '--sql-mode="ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION"'
        return self.runContainer(image='mysql:5.6', name='mysql.ci.local', env_vars=env_vars, command=command)