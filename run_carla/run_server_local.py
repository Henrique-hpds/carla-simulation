import os
import sys
import subprocess
import carla
from time import sleep
from typing import Dict
import psutil

def start_UE4(env: Dict[str, str], rendering: bool, verbose: bool = False, epic: bool = "Low") -> psutil.Process:
    """
    Inicia o server do Unreal Engine 4 
    """
    print("Iniciando o processo do Unreal Engine 4..." if verbose else "")

    # Apagar o conteúdo do arquivo temporário
    with open('../tmp/carla_child_pid.txt', 'w') as f:
        f.write('')

    try:

        if rendering:
            process = subprocess.Popen(f'../CarlaUE4.sh --quality-level={epic}', shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        else:
            process = subprocess.Popen(f'../CarlaUE4.sh -carla-settings=CarlaSettings.ini --quality-level={epic}', shell=True, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        sleep(1)

        # Ler o PID do processo filho do arquivo temporário
        with open('../tmp/carla_child_pid.txt', 'r') as f:
            child_pid = int(f.read().strip())
            print(f"PID do UE4: {child_pid}" if verbose else "")

        if process.poll() is None or process.poll() == 0:
            try:
                return psutil.Process(child_pid)
            except psutil.NoSuchProcess:
                print("Erro ao iniciar o processo do Unreal Engine 4.")
                process.terminate()
                sys.exit(1)
    except KeyboardInterrupt:
        process.terminate()
    finally:
        process.terminate()
        sys.exit(1)

def main(args: Dict[str, bool]):
    try:
        # Definindo variáveis de ambiente para usar Vulkan e a GPU da NVIDIA
        env = os.environ.copy()
        env['VK_ICD_FILENAMES'] = '/usr/share/vulkan/icd.d/nvidia_icd.json'

        UE4_process = start_UE4(env, args['rendering'], args['verbose'])

        sleep(10)
        
        try:
            client = carla.Client('localhost', 2000)
            print("Conectado ao servidor do CARLA.")
        except Exception as e:
            print(f"Erro ao conectar ao servidor do CARLA: {e}")
            os.kill(UE4_process.pid, 9)
            sys.exit(1)

        world = client.get_world()
        settings = world.get_settings()
        settings.synchronous_mode = False
        settings.fixed_delta_seconds = 0.05
        settings.no_rendering_mode = True

        world.apply_settings(settings)

        # traffic_manager = client.get_trafficmanager()
        # traffic_manager.set_synchronous_mode(False)

        try:
            while True:
                sleep(1.5)
                print(".")
                sleep(1.5)
                print("..")
                sleep(1.5)
                print("...")
        except KeyboardInterrupt:
            os.kill(UE4_process.pid, 9)
        except Exception as e:
            print(f"Erro: {e}")
            os.kill(UE4_process.pid, 9)
    
    except KeyboardInterrupt:
        os.kill(UE4_process.pid, 9)
    except Exception as e:
        print(f"Erro: {e}")
        os.kill(UE4_process.pid, 9)
        sys.exit(1)

if __name__ == "__main__":
    args = dict()
    args['rendering'] = False if '--no-rendering' in sys.argv else True
    args['verbose'] = True if '--verbose' in sys.argv else False
    args['epic'] = "Epic" if '--epic' in sys.argv else "Low"
    main(args)
