"""Envia o codigo gerado para o Raspberry Pi e o executa via SSH."""
import paramiko

from config import PI_HOST, PI_REMOTE_DIR, PI_USER

SCRIPT_NAME = "current_program.py"


def _connect() -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(PI_HOST, username=PI_USER)
    return client


def deploy_and_run(code: str) -> None:
    """Copia o script, mata a execucao anterior e inicia a nova."""
    client = _connect()
    try:
        client.exec_command(f"mkdir -p {PI_REMOTE_DIR}")
        sftp = client.open_sftp()
        remote_path = f"{PI_REMOTE_DIR}/{SCRIPT_NAME}"
        with sftp.file(remote_path, "w") as f:
            f.write(code)
        sftp.close()

        client.exec_command(f"pkill -f {SCRIPT_NAME}")
        client.exec_command(
            f"nohup python3 {remote_path} > {PI_REMOTE_DIR}/run.log 2>&1 &"
        )
        print(f"[deploy] rodando em {PI_USER}@{PI_HOST}:{remote_path}")
    finally:
        client.close()


def stop() -> None:
    client = _connect()
    try:
        client.exec_command(f"pkill -f {SCRIPT_NAME}")
    finally:
        client.close()
