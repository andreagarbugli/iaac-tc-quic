# QUIC Traffic Shaping Test and IaC

## Clone the repository

To clone the repository, and its submodules, run the following command:

```bash
git clone --recurse-submodules git@github.com:andreagarbugli/iaac-tc-quic.git
```

## Dependencies

- Install Vagrant:
  - Follow the installation instructions for Vagrant from the [official website](https://developer.hashicorp.com/vagrant/docs/installation).
- Install libvirt provider for Vagrant:
  - Follow the installation instructions for the libvirt provider from the [vagrant-libvirt GitHub page](https://vagrant-libvirt.github.io/vagrant-libvirt/installation.html).
- The project uses qperf to test the traffic shaping. The qperf submodule is included in the repository otherwise it can be downloaded from the [qperf GitHub page](https://github.com/rbruenig/qperf)
- **(Optional)** Install `qperf` and its dependencies:
  - Install `libev-dev` and `libssl-dev` as dependencies.
  - Generate a certificate using the command: `openssl req -x509 -newkey rsa:4096 -keyout server.key -out server.crt -sha256 -days 365 -nodes -subj "/C=IT/L=Bologna/O=Company Name/CN=www.middleware.unibo.it"`

## Project Structure

The project contains a `Vagrantfile` that sets up three virtual machines (VMs): `client`, `server`, and `router`. The client and server VMs are connected to the router VM through a private network. All VMs have a public network connection to the host machine and can access the Internet. The router VM is configured to forward traffic from the client to the server.

To start the VMs, run `vagrant up`. To stop the VMs, run `vagrant halt`. To destroy the VMs, run `vagrant destroy`.

Once the VMs are up and running, you can connect to them using `vagrant ssh <vm_name>`, where `<vm_name>` can be **client**, **server**, or **router**.

| :exclamation: The Ansible playbook is not currently in use. The configuration is managed through the `Vagrantfile` and inline shell scripts. |
| -------------------------------------------------------------------------------------------------------------------------------------------- |

## How to Run

Follow these steps to run the project.

### Compile qperf

If not present, clone the qperf repository by running `git submodule update --init --recursive`.

Then, run the following commands to compile qperf:

```bash
cd qperf
mkdir build
cd build
cmake ..
make -j $(nproc)
```

### Run the project

To run the project, follow these steps:

- Start the VMs by running `vagrant up`.
- Connect to the client and server VMs by running `vagrant ssh client` and `vagrant ssh server` respectively.
- Change to the shared folder between the host and the VMs by running `cd /vagrant`.
- In the server VM, run `./qperf/qperf -s` to start the server.
- In the client VM, run `./qperf/qperf -c 192.168.20.10` to initiate the test.
