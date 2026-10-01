# Assumptions and validation record

The project is self contained and does not use RoomFit source files or secrets. Students with incomplete room groups receive a valid partial room and a warning because every student must be assigned. Local checks use Windows PowerShell. Docker, Kind, and kubectl availability depends on the local Docker Desktop state. Manual screenshots remain required because generated evidence cannot substitute for a live screen capture.

The GitHub push was attempted on 2 October 2026 and could not connect because the environment proxy at 127.0.0.1 port 9 was unavailable. From a connected shell, run `git push -u origin main` in the project folder.

Task 2 ran as the WSL root user because the default Ubuntu account requires an interactive sudo password. The project folder is mounted from Windows and Ansible ignores its configuration when discovered from a world writable path, so each evidence command supplies the inventory and configuration explicitly. Kind updated its API port during startup, so the kubeconfig was regenerated with `kind export kubeconfig --name roomfit`.
