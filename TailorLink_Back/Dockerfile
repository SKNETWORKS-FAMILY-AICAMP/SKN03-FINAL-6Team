# 빌드 단계
FROM eclipse-temurin:23-jdk AS build
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
FROM eclipse-temurin:23-jre
ENV APP_HOME=/apps
WORKDIR $APP_HOME

# 빌드된 JAR 파일 복사
COPY --from=build /apps/build/libs/SKN03-FINAL-6TEAM-0.0.1-SNAPSHOT.jar app.jar

# 애플리케이션 실행
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]