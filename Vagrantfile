# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "bento/fedora-22"
  config.vm.network "public_network"
  config.vm.provision "shell", inline: $script
end

$script = <<SCRIPT
dnf update -y 
dnf install -y @development-tools
dnf install -y fedora-packager
dnf install -y rpmdevtools
SCRIPT
