"""Render complete real evidence files in a terminal style image."""
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parents[1]
EVIDENCE = ROOT / "docs" / "evidence"
OUT = ROOT / "docs" / "screenshots"
FONT = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 16)
LINE = 21
ITEMS = {
    "term_ansible_first_run.png": ("ansible_02_first_run.txt", "ansible-playbook -i inventory.ini playbook.yml"),
    "term_ansible_second_run_idempotent.png": ("ansible_03_second_run_idempotent.txt", "ansible-playbook -i inventory.ini playbook.yml"),
    "term_ansible_service_check.png": ("ansible_04_verification.txt", "id roomfit; stat; systemctl status roomfit; curl health"),
    "term_docker_images.png": ("docker_01_build.txt", "docker build roomfit-api:v1 and roomfit-api:v2; docker images"),
    "term_k8s_pods_ready.png": ("k8s_01_deploy_v1.txt", "kubectl get nodes; kubectl get pods; kubectl get svc"),
    "term_k8s_rolling_update.png": ("k8s_02_rolling_update_pods.txt", "kubectl get pods -n roomfit -w"),
    "term_k8s_rollout_history.png": ("k8s_03_rollout_history.txt", "kubectl rollout status and history deployment roomfit"),
    "term_k8s_rollback.png": ("k8s_05_rollback.txt", "kubectl rollout undo deployment roomfit"),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for image_name, (file_name, command) in ITEMS.items():
        source = EVIDENCE / file_name
        raw = source.read_text(encoding="utf-8", errors="replace").splitlines()
        stamp = datetime.fromtimestamp(source.stat().st_mtime).isoformat(sep=" ", timespec="seconds")
        lines = [f"$ {command}", *raw, f"Rendered from docs/evidence/{file_name}, run on {stamp}"]
        width = max(1440, max((len(line) for line in lines), default=1) * 10 + 48)
        image = Image.new("RGB", (width, max(900, len(lines) * LINE + 40)), "#101820")
        draw = ImageDraw.Draw(image)
        for index, line in enumerate(lines):
            color = "#62d6a6" if index in {0, len(lines) - 1} else "#e6edf3"
            draw.text((24, 20 + index * LINE), line, font=FONT, fill=color)
        image.save(OUT / image_name)


if __name__ == "__main__":
    main()
