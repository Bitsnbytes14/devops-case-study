# Ansible

From WSL Ubuntu run `ansible-playbook playbook.yml --ask-become-pass` from this folder. The inventory targets localhost. The play installs the service, waits for port 5000, then checks health.
