FROM openjdk:12-alpine
RUN apk update
RUN apk add --no-cache nginx
COPY ./nginxWebUI-3.4.8.jar /app/app.jar
WORKDIR /app
ENTRYPOINT ["java", "-jar", "app.jar"]
EXPOSE 8080
