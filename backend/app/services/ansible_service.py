from pathlib import Path
import ansible_runner

BASE_DIR = Path(__file__).resolve().parents[2]
ANSIBLE_DIR = BASE_DIR / 'ansible'

def handle_event(event: dict) -> bool:
    event_name = event.get('event')
    event_data = event.get('event_data') or {}

    if not isinstance(event_data, dict):
        return True

    if event_name in (
        'runner_on_ok',
        'runner_on_failed',
        'runner_on_unreachable'
    ):
        host = event_data.get('host')
        result = event_data.get('res') or {}

        print(f'host: {host}')
        print(f'event: {event_name}')
        print(f'result: {result}')

    return True

def run_playbook(
    playbook: str,
    inventory: str
) -> tuple[str, int]:
    result = ansible_runner.run(
        private_data_dir=str(ANSIBLE_DIR),
        playbook=playbook,
        inventory=inventory,
        event_handler=handle_event,
        quiet=True
    )

    print(result.stdout.read())

    return result.status, result.rc