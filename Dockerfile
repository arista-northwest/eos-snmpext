FROM fedora:22

RUN \
  useradd builder -u 1000 -m -G users,wheel && \
  dnf update -y && \
  dnf install -y @development-tools fedora-packager rpmdevtools

VOLUME ["/eos_snmpext"]

WORKDIR /eos_snmpext

USER builder

ENTRYPOINT ["python", "setup.py", "bdist_rpm"]
