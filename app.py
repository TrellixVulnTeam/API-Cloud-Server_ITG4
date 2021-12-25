from chalice import Chalice
import os
from datetime import datetime as dt
try:
    import psutil
except ImportError:
    os.system('python -m pip install psutil')
try:
    import requests
    from requests import get
except ImportError:
    os.system('python -m pip install requests')
try:
    import geoip2.database
except ImportError:
    os.system('python -m pip install geoip2')
app = Chalice(app_name='Cloud_Server')
@app.route('/')
def index():
    return "Jarvis API"

@app.route('/time')
def getTime(): 
    now = dt.now()
    currentTime = now.strftime('%H:%M:%S')
    return currentTime
@app.route('/ip_address/private')
def private():
    import socket
    ip = socket.gethostbyname(socket.gethostname())
    return ip
@app.route('/ip_address/public')
def public():
    ip = get('https://api.ipify.org').text
    return ip
@app.route('/weather')
def weather(): 
    api_key = "90e19536df9f0408dfc9f39e73a0ff89"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    from datetime import date
    Ip = public()
    with geoip2.database.Reader('GeoLite2-City_20210105/GeoLite2-City.mmdb') as reader:
        ip_address_location = reader.city(Ip)
        ip_rasa = ip_address_location.city.name
        city_name = ip_rasa
        complete_url = base_url + "appid=" + api_key + "&q=" + str(city_name)
        response = get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidiy = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            round(current_temperature, 2)
            Temperature = current_temperature - 273
            Temperature = int(Temperature)
            current_pressure = current_pressure * 0.75
            data = "City: " + city_name + "\n" + "Temperature: " + str(Temperature) + " C" + "\n" + "Pressure: " + str(current_pressure) + " mmHg" + "\n" + "Humidity: "  + str(current_humidiy) + "%"+ "\n" + "Weather Description: " + weather_description
            return data
@app.route('/help')
def help():
    data = "1. Weather(" + private() + ":8000/ip_address/private) \n2.Time(" + private() + ":8000/time)" + "\n" + "3.Public IP Address(IPv4)(" + private() + ":8000/ip_address/public" + "\n" + "4.Private IP Address(" + private() + ":8000/ip_address/private" + "\n" + "More to be added soon, be in touch..."
    return data
@app.route("/files")
def server():
    def receiver():
        import socket
        import tqdm
        import os
        hostname = socket.gethostname()
        SERVER_HOST = socket.gethostbyname(hostname)
        SERVER_PORT = 8001
        BUFFER_SIZE = 1024 * 4
        SEPARATOR = "<SEPARATOR>"
        s = socket.socket()
        s.bind((SERVER_HOST,SERVER_PORT))
        s.listen()
        client_socket,address=s.accept()
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename,filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        with open(filename, "wb") as f:
            while True:
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read: 
                    break
                f.write(bytes_read)
        client_socket.close()
        current_folder = os.getcwd()
        file_location = str(current_folder) + "/" + str(filename)
        s.close()
        returner = f"Received from {address} to {SERVER_HOST} through port {SERVER_PORT}.\nFile Location: " + str(file_location) + "\n"
        return returner
    receiver()
@app.route("/system_info")
def system_info():
    import platform
    import psutil
    from datetime import datetime
    def get_size(bytes, suffix="B"):
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor
    title = "====System Information====" 
    uname = platform.uname()
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    cpufreq = psutil.cpu_freq()
    System = uname.system
    Node_Name = uname.node
    Release = uname.release
    Version = uname.version
    Machine = uname.machine
    Processor = uname.processor
    Boot_Time_Section = "\n" + "====BOOT TIME===="
    Bootime = f"{bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}"
    CPU_Section = "\n" + "====CPU Info===="
    Phisical_Cores = "Phisycal Cores: " + str(psutil.cpu_count(logical=False))
    Total_Cores = "Total Cores: " + str(psutil.cpu_count(logical=True))
    CPU_Usage = "CPU Usage: " + str(psutil.cpu_percent()) + "%"
    Current_Freq = "Current Frequency: " + str(int(cpufreq.current)) + " MHz"
    return title + "\n" + "System: " + System + "\n" + "Release: " + Release + "\n" + "Version: " + Version + "\n" + Machine + "\n" + Processor + "\n" + Boot_Time_Section + "\n" + Bootime + "\n" + CPU_Section + "\n" + Phisical_Cores + "\n" + Total_Cores + "\n" + CPU_Usage + "\n" + Current_Freq
    print("="*40, "Memory Information", "="*40)
    # get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    print(f"Available: {get_size(svmem.available)}")
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    print("="*20, "SWAP", "="*20)
    # get the swap memory details (if exists)
    swap = psutil.swap_memory()
    print(f"Total: {get_size(swap.total)}")
    print(f"Free: {get_size(swap.free)}")
    print(f"Used: {get_size(swap.used)}")
    print(f"Percentage: {swap.percent}%")
    print("="*40, "Disk Information", "="*40)
    print("Partitions and Usage:")
    # get all disk partitions
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(f"=== Device: {partition.device} ===")
        print(f"  Mountpoint: {partition.mountpoint}")
        print(f"  File system type: {partition.fstype}")
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        print(f"  Total Size: {get_size(partition_usage.total)}")
        print(f"  Used: {get_size(partition_usage.used)}")
        print(f"  Free: {get_size(partition_usage.free)}")
        print(f"  Percentage: {partition_usage.percent}%")
    # get IO statistics since boot
    disk_io = psutil.disk_io_counters()
    print(f"Total read: {get_size(disk_io.read_bytes)}")
    print(f"Total write: {get_size(disk_io.write_bytes)}")
    print("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            print(f"=== Interface: {interface_name} ===")
            if str(address.family) == 'AddressFamily.AF_INET':
                print(f"  IP Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast IP: {address.broadcast}")
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                print(f"  MAC Address: {address.address}")
                print(f"  Netmask: {address.netmask}")
                print(f"  Broadcast MAC: {address.broadcast}")
    
    # get IO statistics since boot
    net_io = psutil.net_io_counters()
    print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")