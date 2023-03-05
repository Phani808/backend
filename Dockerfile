# Build stage
FROM maven:3.8.4-openjdk-11-slim AS build
WORKDIR /app
COPY pom.xml .
RUN mvn -B dependency:go-offline
COPY src/ ./src/
RUN mvn -B package

# Final stage
FROM openjdk:11.0.13-jre-slim-buster
WORKDIR /app
COPY --from=build /app/target/devopsodia.war .
CMD ["java", "-Xmx256m", "-jar", "devopsodia.war"]