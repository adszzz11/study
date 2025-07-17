# Jenkins Pipeline 구축 with Docker

Server 배포 전 테스트환경 구축, 이후 실제 배포까지 필요한 Process 및 resource 정리

1. docker 설치
- 필요한 대부분의 환경을 Docker 위에서 실행하기에, 미리 Docker를 설치하여 진행
3. jenkins 설치
- DockerHub를 이용하여 최신 버전의 Jenkins 다운로드 및 Jenkins 실행
- Jenkins image 다운로드
```
docker pull jenkins/jenkins:lts
```
- Jenkins Container build
```
docker run -d -p 8181:8080 -v /Users/sm/docker/jenkins:/var/jenkins_home --name jenkins -u root jenkins/jenkins:lts
```
5. jenkins build
- jenkins를 실행한 첫 화면에 Password 입력을 요청하는데
  Docker logs jenkins를 통하여 initial password 확인 가능
  해당 Password 입력 후 Default plugins 설치
  시간 지나면 Jenkins 메인 화면 확인 가능
7. test project 생성
![[Pasted image 20221101211055.png]]
- Pipeline 선택
![[Pasted image 20221101212306.png]]
- GitHub project url 설정(여기서는 테스트용으로 생성된 CI/CD Project 활용)
- GitHub hook trigger for GITScm polling 활성화
9. GitHub WebHook 생성
- 한계점 : 로컬로 진행하는 중 현재 Macbook의 IP domain화 할 필요가 있음
	- ngrok 프로그램 사용하여 현재 IP를 도메인으로 publish
	![[Pasted image 20221101212637.png]]
- Deploy할 GitHub project의 WebHook 설정
- Payload URL : https://[IP]/github-webhook/ 설정
![[Pasted image 20221101212731.png]]
- Recent Deliveries 탭을 통하여 commit 시 실제 Jenkins로 요청을 보내는지 확인 가능
10. Pipeline Script 작성
```
pipeline {
    agent any
    
    stages {
        stage('Prepare') {
            agent any

            steps {
                git branch: 'main',
                    credentialsId: 'adszzz11',
                    url: 'https://github.com/adszzz11/cicd-test.git'
            }

            post {

                success {
                    echo 'prepare success'
                }

                always {
                    echo 'done prepare'
                }

                cleanup {
                    echo 'after all other post conditions'
                }
            }
        }

        stage('JUnit Test') {
            agent any
            steps {
                sh './gradlew test'
                
            }
            post {

                success {
                    echo 'prepare success'
                }

                always {
                    junit '**/build/test-results/test/**/*.xml'
                }

                cleanup {
                    echo 'after all other post conditions'
                }
            } 
        }


        stage('build gradle') {
            agent any
            steps {
                sh 'chmod +x ./gradlew'
                sh  './gradlew -x build'


                sh 'ls -al ./build'
            }
            post {
                success {
                    echo 'gradle build success'
                }

                failure {
                    echo 'gradle build failed'
                }
            }
        }
        
        // stage('Test Report') {
        //     agent any
        //     steps {
        //         junit '**/build/test-results/test/**/*.xml'
        //     }
        // }


        stage('dockerizing'){
            agent any
            steps{
                sh 'docker build -t spring_test:latest .'
                script {
                    bo = sh(script: 'docker ps -q --filter name=spring1', returnStdout: true)
                    echo bo.toString()
                }
                
            }
        }
        
        
        stage('Deploy_stop') {
            agent any
            
            when{
                expression { bo.toString() != "" }
            }
            steps {
                sh 'docker stop spring1'
                sh 'docker rm spring1'
            }

            post {
                success {
                    echo 'success'
                }

                failure {
                    echo 'failed'
                }
            }
        }
        
        stage('Deploy') {
            agent any
            steps {
                echo bo.toString()
                sh 'docker run -d -p 8080:8080 --name spring1 spring_test:latest'
            }
        }
    }
}
```

0. ETC
- 실제 프로젝트 진행사진
![[Pasted image 20221101213629.png]]
![[Pasted image 20221101213641.png]]
![[화면 기록 2022-11-01 오후 10.21.12.mov]]

![[Pasted image 20221101224126.png]]

```
<html><head>
<meta http-equiv="Content-Type" content="text/html;charset=euc-kr">
</head>
<body align="center">
<table border="0" style="margin-top:30px;width:1000px">
<tbody><tr width="100%">
	<td width="50">&nbsp;</td>
	<td width="950">
		<b>
		요청하신 페이지가 존재하지 않거나, 응답에 일시적인 에러가 발생 되었습니다.<br>
		잠시 후 다시 시도해 주시길 바랍니다.<br>
		</b><br>
		문제가 지속되시면 아래의 메일로 문의 주시길 바랍니다.<br>
		문의: <a href="mailto:help@danal.co.kr">help@danal.co.kr</a><br>
		<br>
		감사합니다.<br>
	</td>
</tr>


</tbody></table></body></html>
```
f![[화면 기록 2022-11-01 오후 10.58.11.mov]]