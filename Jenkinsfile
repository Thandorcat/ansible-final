node("${env.SLAVE}") {

  stage("Build"){
    
    git branch: 'adoropei', url: 'git@git.epam.com:siarhei_beliakou/mntlab-exam.git'
    wrap([$class: 'BuildUser']) {
      sh "echo Build User Name: ${BUILD_USER} > src/main/resources/build-info.txt" 
    }  
    sh 'echo GIT Branch: $(git branch | cut -c 3-) >> src/main/resources/build-info.txt'   
    sh 'echo GIT Commit: $(git rev-parse --short HEAD) >> src/main/resources/build-info.txt'
    sh 'echo GIT URL: $(git config remote.origin.url) >> src/main/resources/build-info.txt'
    sh 'echo Build date: $(date) >> src/main/resources/build-info.txt'
    sh "cat src/main/resources/build-info.txt" 
    sh '/usr/local/maven/bin/mvn clean package -DbuildNumber=$BUILD_NUMBER'
    sh "echo build artefact"
  }

  stage("Package"){
    
    sh "tar -czvf mnt-exam.tar.gz -C target mnt-exam.war"
    sh "ls -l"
    sh "echo package artefact"
  }

  stage("Roll out Dev VM"){
    sh "cat createvm.yml"
    
    withEnv(["ANSIBLE_FORCE_COLOR=true", "PYTHONUNBUFFERED=1"])
    { ansiColor('xterm') { sh "nohup ansible-playbook createvm.yml -vv"}}

    sh "echo ansible-playbook createvm.yml ..."
  }

  stage("Provision VM"){
    sh "cat provisionvm.yml"
    
    withEnv(["ANSIBLE_FORCE_COLOR=true", "PYTHONUNBUFFERED=1"])
    { ansiColor('xterm') { sh "nohup ansible-playbook provisionvm.yml -vv"}}

    sh "echo ansible-playbook provisionvm.yml ..."
  }

  stage("Deploy Artefact"){
    sh "cat deploy.yml "
    
    withEnv(["ANSIBLE_FORCE_COLOR=true", "PYTHONUNBUFFERED=1"])
    { ansiColor('xterm') { sh "nohup ansible-playbook deploy.yml -e artefact=mnt-exam.tar.gz -vv"}}
    
    sh "echo ansible-playbook deploy.yml -e artefact=... ..."
  }

  stage("Test Artefact is deployed successfully"){
    sh "cat application_tests.yml "
    
    withEnv(["ANSIBLE_FORCE_COLOR=true", "PYTHONUNBUFFERED=1"])
    { ansiColor('xterm') { sh "nohup ansible-playbook application_tests.yml -vv"}}

    sh "echo ansible-playbook application_tests.yml"
  }

  stage("Destroying VM"){
    sh "cat destroy.yml "
    
    withEnv(["ANSIBLE_FORCE_COLOR=true", "PYTHONUNBUFFERED=1"])
    { ansiColor('xterm') { sh "nohup ansible-playbook destroy.yml -vv"}}

    sh "echo ansible-playbook destroy.yml"
  }

}

