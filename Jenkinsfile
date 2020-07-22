/*
File: Jenkinsfile
Author: Dalwar Hossain (dalwar23@protonmail.com)
Copyright: Dalwar Hossain
*/

pipeline {
    agent any
    environment {
        PYTHON_INTERPRETER = "python3.7"
        REPOSITORY_NAME = sh (script: 'echo $(echo `git config --get remote.origin.url` | rev | cut -d "/" -f 1 | cut -d "." -f 2 | rev)', returnStdout: true).trim()
    }
    options {
        buildDiscarder(logRotator(numToKeepStr: '2', artifactNumToKeepStr: '1'))
    }
    stages {
        stage ('Sanity Check') {
            parallel {
                stage ('Check Python3') {
                    steps {
                        sh "${PYTHON_INTERPRETER} --version"
                    }
                }
                stage ('Python3 virtualenv') {
                    steps {
                        sh 'virtualenv --version'
                    }
                }
                stage ('Check setup.py') {
                    steps {
                        sh 'test -f setup.py'
                        sh 'echo \$?'
                    }
                }
            }
        }
        stage ('Initialize') {
            steps {
                sh "virtualenv --always-copy -p ${PYTHON_INTERPRETER} venv"
                sh '''
                source venv/bin/activate
                pip install --upgrade pip
                pip --version
                '''
            }
        }
        stage ('Pre-Build') {
            parallel {
                stage ('Dev Dependencies') {
                    when {
                        expression {
                            fileExists('requirements_dev.txt')
                        }
                    }
                    steps {
                        sh '''
                        source venv/bin/activate
                        pip install --upgrade setuptools wheel
                        pip install -r requirements_dev.txt
                        deactivate
                        '''
                    }
                }
                stage ('Pkg Dependencies') {
                    when {
                        expression {
                            fileExists('requirements.txt')
                        }
                    }
                    steps {
                        sh '''
                        source venv/bin/activate
                        pip install -r requirements.txt
                        deactivate
                        '''
                    }
                }
            }
       }
        stage ('Build') {
            stage ('Build HTML') {
                steps {
                    sh '''
                    source venv/bin/activate
                    cd docs/
                    make clean html
                    deactivate
                    '''
                }
            }
        }
        stage ('Create Artifacts') {
            environment {
                PROJECT_VERSION = sh (script: '"${PYTHON_INTERPRETER}" setup.py --version', returnStdout: true).trim()
            }
            steps {
                sh '''
                if [[ -d "${WORKSPACE}/docs/build/html/" ]]; then
                    cd "${WORKSPACE}/docs/build/html/"
                    tar -vczf "${WORKSPACE}/${REPOSITORY_NAME}-${BRANCH_NAME}-${PROJECT_VERSION}-${BUILD_NUMBER}.tar.gz" *
                fi
                '''
            }
        }
        stage ('Manage Artifacts') {
            parallel {
                stage ('Archive Artifacts - tarball') {
                    steps {
                        archiveArtifacts artifacts: '*.gz ',
                        onlyIfSuccessful: true
                    }
                }             
                stage ('Publish to Test') {
                    steps {
                        sh '''
                        DST="/var/www/html/staging/docs/${REPOSITORY_NAME}"
                        SRC="docs/build/html/*"
                        if [[ -d "${DST}" ]]; then
                            sudo cp -r $SRC $DST
                        else
                            sudo mkdir -p $DST
                            sudo cp -r $SRC $DST
                        fi
                        '''
                    }
                }
            }
        }
    }
}
