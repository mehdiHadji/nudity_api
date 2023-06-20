def COMMIT_HASH

pipeline {
    agent any
    stages {

        stage('Setup SSH Tunnel') {
            when {
                branch 'master'
            }
            steps {
                script {
                    sh 'ssh -f -o ExitOnForwardFailure=yes -NL 2234:127.0.0.1:22 jenkins@2a01:cb00:38e:7500:a00:27ff:fee6:ca39 sleep 120'
                }
            }

        }

        stage('Build and push docker image') {
            steps {
                script {
                    COMMIT_HASH = sh(returnStdout: true, script: 'git rev-parse HEAD').trim().take(7)
                    dockerImage = docker.build("registry.gitlab.com/mehdihadji/python_service:latest", "-f ./Dockerfile .")
                }

                withCredentials([usernamePassword(
                    credentialsId: "registry", usernameVariable: "USER", passwordVariable: "PASS")]) {
                        sh "echo $PASS | docker login registry.gitlab.com -u $USER --password-stdin"
                }

                sh "docker tag registry.gitlab.com/mehdihadji/python_service:latest registry.gitlab.com/mehdihadji/python_service:${COMMIT_HASH}"
                sh "docker push registry.gitlab.com/mehdihadji/python_service:latest"
                sh "docker push registry.gitlab.com/mehdihadji/python_service:${COMMIT_HASH}"
            }

        }


        stage('Deploy') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "registry", usernameVariable: "USER", passwordVariable: "PASS")]) {
                        sh 'echo "### Deploying..."'
                        sh """
                        if [ ! -d "/tmp/deploy" ] ; then
                            git clone git@gitlab.com:mehdiHadji/tooling_deploy_playbook.git /tmp/deploy
                        else
                            cd /tmp/deploy
                            git pull
                        fi
                        ansible-playbook /tmp/deploy/python_service/site.yml -i /tmp/deploy/python_service/inventory/dev --extra-vars "ansible_sudo_pass=hadapassword profile=dev registry_password=$PASS registry_user=$USER img_version=${COMMIT_HASH}"
                        """
                 }


            }
        }
    }
}