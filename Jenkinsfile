/*
File: Jenkinsfile
Author: Dalwar Hossain (dalwar.hossain@dimensiondata.com)
Copyright: Dalwar Hossain, Dimensiondata Germany AG & Co. KG
*/

pipeline {
    agent any
    environment {
        PYTHON_INTERPRETER = "python3.7"
        REPOSITORY_NAME = sh (script: 'echo $(echo `git config --get remote.origin.url` | rev | cut -d "/" -f 1 | cut -d "." -f 2 | rev)', returnStdout: true).trim()
    }
    options {
        office365ConnectorWebhooks([[
            name: 'MSTeams', notifyAborted: true, notifyBackToNormal: true,
            notifyFailure: true, notifyNotBuilt: true, notifyRepeatedFailure: true,
            notifySuccess: true, notifyUnstable: true, url: "${MSTEAMS_WEBHOOK_CARNIVAL}"
        ]])
        buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '1'))
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
                stage ('Check Setup') {
                    steps {
                        sh 'test -f setup.py'
                        sh 'echo \$?'
                    }
                }
            }
        }
        stage ('Policy Check') {
            environment {
                SCANNER_HOME = tool 'ScannerQube'
                PROJECT_VERSION = sh (script: '"${PYTHON_INTERPRETER}" setup.py --version', returnStdout: true).trim()
            }
            steps {
                withSonarQubeEnv ('SonarQube') {
                    /*
                    Double quote is necessary for variable management in groovy syntax
                    REPOSITORY_NAME is a custom ENV Variable that resolves to
                    REPOSITORY_NAME=$(echo $JOB_NAME | cut -d '/' -f 1)
                    [Valid only for multibranch pipline]
                    */
                    sh "${SCANNER_HOME}/bin/sonar-scanner " +
                    "-Dsonar.projectKey=${REPOSITORY_NAME}-${BRANCH_NAME} " +
                    "-Dsonar.projectName=${REPOSITORY_NAME}-${BRANCH_NAME} " +
                    "-Dsonar.projectVersion=${PROJECT_VERSION} " +
                    "-Dsonar.sources=. "
                }
            }
        }
        stage ('Quality Gate') {
            /*
            1. SonarQube server 6.2+ is required
            2. A webhook in SonarQube server pointing to <jenkins server>/sonarqube-webhook/ (The trailing slash is important)
            3. Use withSonarQubeEnv step in your pipeline (so that SonarQube taskId is correctly attached to the pipeline context).
            */
            steps {
                timeout (time: 3, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
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
                        pip install --upgrade setuptools wheel twine
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
            parallel {
                stage ('Build Package') {
                    steps {
                        sh '''
                        source venv/bin/activate
                        python3 setup.py build
                        deactivate
                        '''
                    }
                }
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
                stage ('Build PDF') {
                     steps {
                        sh '''
                        source venv/bin/activate
                        cd docs/
                        make latexpdf LATEXMKOPTS="-silent -f -no-shell-escape"
                        deactivate
                        '''
                    }
                }
            }
        }
        stage ('Package') {
            parallel {
                stage ('Source') {
                    steps {
                        sh '''
                        source venv/bin/activate
                        python3 setup.py egg_info --tag-build=".${BRANCH_NAME}" sdist
                        deactivate
                        '''
                    }
                }
                stage ('Wheel') {
                    steps {
                        sh '''
                        source venv/bin/activate
                        python3 setup.py egg_info --tag-build=".${BRANCH_NAME}" bdist_wheel
                        deactivate
                        '''
                    }
                }
                stage ('Egg') {
                    steps {
                        sh '''
                        source venv/bin/activate
                        python3 setup.py egg_info --tag-build=".${BRANCH_NAME}" bdist_egg
                        deactivate
                        '''
                    }
                }
            }
        }
        stage ('Create Artifacts') {
            environment {
                PROJECT_VERSION = sh (script: 'python3 setup.py --version', returnStdout: true).trim()
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
                stage ('Archive Artifacts - Packages') {
                    steps {
                        archiveArtifacts artifacts: 'dist/*'
                    }
                }
                stage ('Archive Artifacts - tarball') {
                    steps {
                        archiveArtifacts artifacts: '*.gz ',
                        onlyIfSuccessful: true
                    }
                }
                stage ('Archive Artifacts - pdf') {
                    steps {
                        archiveArtifacts artifacts: 'docs/build/latex/*.pdf',
                        onlyIfSuccessful: true
                    }
                }
                stage ('Publish Docs to Production') {
                    when {
                        branch 'master'
                    }
                    steps {
                        sshPublisher(
                            publishers: [sshPublisherDesc(configName: 'Documentation Server',
                            transfers: [sshTransfer(cleanRemote: true,
                            excludes: '', execCommand: '', execTimeout: 120000,
                            flatten: false, makeEmptyDirs: true, noDefaultExcludes: false,
                            patternSeparator: '[, ]+', remoteDirectory: "${REPOSITORY_NAME}",
                            remoteDirectorySDF: false, removePrefix: 'docs/build/html/',
                            sourceFiles: 'docs/build/html/**/*')],
                            usePromotionTimestamp: false,
                            useWorkspaceInPromotion: false, verbose: false)]
                        )
                    }
                }
                stage ('Publish to Test') {
                    when {
                        branch 'dev'
                    }
                    steps {
                        sh '''
                        DST="/var/www/html/docs/${REPOSITORY_NAME}"
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
                stage ('Upload to DD Artifactory') {
                    when {
                        anyOf {
                            branch 'master'
                        }
                    }
                    steps {
                        rtUpload (
                            serverId: "JFrog-DimensionData",
                            buildName: "${REPOSITORY_NAME}-${BRANCH_NAME}",
                            buildNumber: "${BUILD_NUMBER}",
                            specPath: 'jfrog-spec.json',
                            failNoOp: true
                        )
                    }
                }
                stage ('Upload to DDLAB Artifactory') {
                    steps {
                        rtUpload (
                            serverId: "JFrog-Local",
                            buildName: "${REPOSITORY_NAME}-${BRANCH_NAME}",
                            buildNumber: "${BUILD_NUMBER}",
                            specPath: 'jfrog-spec.json',
                            failNoOp: true
                        )
                    }
                }
            }
        }
        stage ('Publish Build Info') {
            steps {
                rtPublishBuildInfo (
                    serverId: "JFrog-Local",
                    buildName: "${REPOSITORY_NAME}-${BRANCH_NAME}",
                    buildNumber: "${BUILD_NUMBER}"
                )
            }
        }
    }
}
