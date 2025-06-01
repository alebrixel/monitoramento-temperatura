import psutil
import requests
import time
import datetime

def coletar_temperatura():
    temps = psutil.sensors_temperatures()
    if not temps:
        return None
    for nome, sensores in temps.items():
        for s in sensores:
            if s.current:
                return s.current
    return None

def main():
    while True:
        temperatura = coletar_temperatura()
        cpu_percent = psutil.cpu_percent(interval=1)
        processos = sorted(psutil.process_iter(['name', 'cpu_percent']), key=lambda p: p.info['cpu_percent'], reverse=True)
        top_processos = [p.info for p in processos[:5]]

        payload = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "temperatura": temperatura,
            "cpu_percent": cpu_percent,
            "top_processos": top_processos
        }

        try:
            response = requests.post("http://localhost:5000", json=payload)
            print(f"Enviado: {response.status_code} - {payload}")
        except Exception as e:
            print(f"Erro ao enviar: {e}")

        time.sleep(10)

if __name__ == "__main__":
    main()
