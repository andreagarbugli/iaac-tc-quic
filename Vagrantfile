# -*- mode: ruby -*-
# vi: set ft=ruby :

IMAGE_NAME = "generic/ubuntu2204"
USER = "vagrant"

NETWORK1 = "192.168.10"
GATEWAY1 = "#{NETWORK1}.1"
NETWORK2 = "192.168.20"
GATEWAY2 = "#{NETWORK2}.1"

SHARED_FOLDER = "./tc-daemon/"

$common_script = <<-'SCRIPT'
apt-get update
apt-get -y install python3-venv python3-pip traceroute net-tools libev-dev libssl-dev
SCRIPT

# build-essential git

Vagrant.configure("2") do |config|
  # Router
  config.vm.define "router", primary: true do |router|
    router.vm.box = IMAGE_NAME
    router.vm.hostname = "router"  
    router.vm.provider :libvirt do |libvirt|
    end

    router.vm.network :private_network,
      :libvirt__iface_name => "eth1",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.1.4.1",
      :libvirt__tunnel_local_port => "10001",
      :libvirt__tunnel_ip => "127.1.1.1",
      :libvirt__tunnel_port => "10001",
      auto_config: false
    router.vm.network :private_network,
      :libvirt__iface_name => "eth2",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.1.4.2",
      :libvirt__tunnel_local_port => "10001",
      :libvirt__tunnel_ip => "127.1.2.1",
      :libvirt__tunnel_port => "10001",
      auto_config: false

    router.vm.synced_folder "#{SHARED_FOLDER}", "/vagrant", type: "rsync"
    router.vm.provision "shell", inline: $common_script
    router.vm.provision "shell",
        inline: <<-SHELL
        echo -e "\nnet.ipv4.ip_forward=1" >> /etc/sysctl.conf
        sysctl -p
        ip link set dev eth1 up
        ip addr add dev eth1 #{GATEWAY1}/24
        ip link set dev eth2 up
        ip addr add dev eth2 #{GATEWAY2}/24
        # iptables config to enable NAT
        sudo iptables -t nat -A POSTROUTING -j MASQUERADE
        # apt-get -y install iptables-persistent
        # iptables-save > /etc/iptables/rules.v4
      SHELL
    # router.vm.provision "ansible" do |ansible|
    #   ansible.playbook = "ansible/playbook.yml"
    #   ansible.extra_vars = {
    #       user: USER,
    #       node_name: "router"
    #   }
    # end
  end

  # Client
  config.vm.define "client" do |client|
    client.vm.box = IMAGE_NAME
    client.vm.hostname = "client"
    client.vm.provider :libvirt do |libvirt|
    end

    client.vm.network :private_network,
      :libvirt__iface_name => "eth1",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.1.1.1",
      :libvirt__tunnel_local_port => "10001",
      :libvirt__tunnel_ip => "127.1.4.1",
      :libvirt__tunnel_port => "10001",
      auto_config: false
      
    client.vm.synced_folder "#{SHARED_FOLDER}", "/vagrant", type: "rsync"
    client.vm.provision "shell", inline: $common_script     
    client.vm.provision "shell",
      run: "always",
      inline: <<-SHELL
        ip link set dev eth1 up
        ip addr add dev eth1 #{NETWORK1}.10/24
        ip route delete default
        ip route add default via #{GATEWAY1}
      SHELL
  end
  

  # Server
  config.vm.define "server" do |server|
    server.vm.box = IMAGE_NAME
    server.vm.hostname = "server"
    server.vm.provider :libvirt do |libvirt|
    end

    server.vm.network :private_network,
      :libvirt__iface_name => "eth1",
      :libvirt__tunnel_type => "udp",
      :libvirt__tunnel_local_ip => "127.1.2.1",
      :libvirt__tunnel_local_port => "10001",
      :libvirt__tunnel_ip => "127.1.4.2",
      :libvirt__tunnel_port => "10001",
      auto_config: false

    server.vm.synced_folder "#{SHARED_FOLDER}", "/vagrant", type: "rsync"
    server.vm.provision "shell", inline: $common_script
    server.vm.provision "shell",
      run: "always",
      inline: <<-SHELL
        ip link set dev eth1 up
        ip addr add dev eth1 #{NETWORK2}.10/24
        ip route delete default
        ip route add default via #{GATEWAY2}
    SHELL
  end
  
end
