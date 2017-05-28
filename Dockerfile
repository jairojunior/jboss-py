FROM jboss/wildfly:10.1.0.Final

USER jboss

RUN curl -o /tmp/hawtio.war http://central.maven.org/maven2/io/hawt/hawtio-web/1.5.0/hawtio-web-1.5.0.war

RUN /opt/jboss/wildfly/bin/add-user.sh python python0! --silent

CMD ["/opt/jboss/wildfly/bin/standalone.sh", "-b", "0.0.0.0", "-bmanagement", "0.0.0.0"]
