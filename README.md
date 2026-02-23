# Project server

Creates a project server target, which is basically a docker container acting as
a stangalone server, depending on the type, it can be a:
- proxmox: A proxmox virtualisation platform you can run emulated virtual machines
- systemd: A standalone server you can customize trough ssh(+ansible)
- docker: Like systemd + docker preinstalled
- kibernetes: like docker but with kind (kuberrnetes in docker) installed

If you deploy into the ecorp infrastructure you can deepen the complexity of
your infrasturcure, you can route subnets there and use DNS names inside these
networks.


## TODO
- implement add/remove routing on host machine
