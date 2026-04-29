
#1.build compile
FROM maven:3.8.5-openjdk-17 AS build
WORKDIR /app

#copy the project dependency from pom.xml to 
COPY pom.xml .
RUN mvn dependency:go-offline

#copy src source code
COPY src ./src
#skip exec test, but still have compile test
RUN mvn clean package -DskipTests

#2.Run .jar file
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app
#copy to "build" env by constructed 
COPY --from=build /app/target/news-dispatcher-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
