# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "centos/7"

  config.vm.provider "virtualbox" do |v|
    v.memory = 256
    v.cpus = 1
  end

  config.vm.define "rpmbuilder" do |rpmbuilder|
    rpmbuilder.vm.network "private_network", ip: "192.168.50.12", virtualbox__intnet: "net1"
    rpmbuilder.vm.hostname = "rpmbuilder"
  end

end
