# Configuration management

[ansible/playbook.yml](../ansible/playbook.yml) configures WSL Ubuntu localhost. It installs Python, curl, Git and logrotate, creates roomfit and devops users, creates application and log paths, installs requirements, writes the environment file, enables the systemd service, then verifies port 5000 and health.

The repeated run is idempotent. Its real recap reports `changed=0`. The matching CA II verification visual is [page-8-2.png](diagrams/ca-ii-reference/page-8-2.png). See [ansible evidence](evidence/ansible_03_second_run_idempotent.txt) and [service verification](evidence/ansible_04_verification.txt).
