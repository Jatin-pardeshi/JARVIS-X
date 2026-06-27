import asyncio

async def start_vms():
    vms = ["Kali-Linux", "Parrot-OS", "Arch", "Windows-Server"]
    print("Initiating Lab Environment Startup Sequence...")
    for vm in vms:
        try:
            print(f"Attempting to start {vm}...")
            process = await asyncio.create_subprocess_exec(
                "VBoxManage", "startvm", vm, "--type", "headless",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode == 0:
                print(f"[{vm}] Startup command queued successfully.")
            else:
                print(f"[{vm}] Failed to start. Error: {stderr.decode().strip()}")
        except FileNotFoundError:
            print(f"[{vm}] VBoxManage not found. Is VirtualBox installed and in PATH?")
        except Exception as e:
            print(f"Failed to start {vm}: {e}")

if __name__ == "__main__":
    asyncio.run(start_vms())
