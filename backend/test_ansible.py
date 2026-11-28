from pathlib import Path

from app.services.ansible_service import run_playbook, ANSIBLE_DIR

status, rc = run_playbook(
    playbook='playbooks/test.yml',
    inventory=str(ANSIBLE_DIR / 'inventory' / 'localhost.ini')
)

print(f'Status: {status} \nReturn code: {rc}')