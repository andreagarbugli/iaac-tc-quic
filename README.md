# Dependencies

- Install vagrant
    - Install libvirt provider for vagrant https://vagrant-libvirt.github.io/vagrant-libvirt/installation.html.
- Install poetry
    -  To show the virtual env in the project `poetry config virtualenvs.in-project true`
- Install `qperf` and all the submodules. `libev-dev` and `libssl-dev` is a dependency
    - create a certificate `openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -sha256 -days 365 -nodes -subj "/C=IT/L=Bologna/O=Company Name/CN=www.middleware.unibo.it"`
