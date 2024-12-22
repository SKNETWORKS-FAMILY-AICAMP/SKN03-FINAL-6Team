FROM gradle:8.11.1-jdk17-alpine as build
ENV APP_HOME=/apps
WORKDIR $APP_HOME

# Gradle 환경 복사
COPY ./build.gradle ./settings.gradle ./gradlew $APP_HOME/
COPY ./gradle $APP_HOME/gradle
RUN chmod +x gradlew

# 소스 코드 복사 및 빌드
COPY ./src $APP_HOME/src
RUN ./gradlew clean build -x test

# 실행 단계
FROM openjdk:17-jdk
ENV APP_HOME=/apps
WORKDIR $APP_HOME

# 빌드된 JAR 파일 복사
COPY --from=build /apps/build/libs/SKN03-FINAL-6TEAM-0.0.1-SNAPSHOT.jar app.jar

# 컨테이너 실행 유무 확인 
HEALTHCHECK CMD curl http://localhost:8080/actuator/health

# 애플리케이션 실행
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]