import csv
import sys
import os

try:
    from colorama import init, Fore, Style
    init()  # 初始化colorama
    COLOR_AVAILABLE = True
except ImportError:
    # 如果colorama不可用，定义占位符
    class Fore:
        GREEN = ''
        BLUE = ''
        RED = ''
        RESET = ''
    class Style:
        RESET_ALL = ''
    COLOR_AVAILABLE = False

def ip_to_int(ip):
    """将IP地址转换为整数"""
    parts = ip.split('.')
    if len(parts) != 4:
        raise ValueError("Invalid IP address format")
    return sum(int(part) << (24 - i * 8) for i, part in enumerate(parts))

def load_ip_database(file_path):
    """加载IP数据库"""
    import pickle
    import time
    
    # 优先尝试加载pickle格式
    pickle_path = 'data.pickle'
    if os.path.exists(pickle_path):
        try:
            print("Using pickle format for faster loading...")
            start_time = time.time()
            with open(pickle_path, 'rb') as f:
                ip_ranges = pickle.load(f)
            end_time = time.time()
            print(f"Pickle database loaded in {end_time - start_time:.2f} seconds")
            return ip_ranges
        except Exception as e:
            print(f"Error loading pickle database: {e}")
            print("Falling back to CSV format...")
    
    # 回退到CSV格式
    print("Loading CSV format (this may take a while)...")
    start_time = time.time()
    ip_ranges = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 10:
                continue
            start_ip = int(row[0])
            end_ip = int(row[1])
            country_code = row[2]
            country = row[3]
            province = row[4]
            city = row[5]
            latitude = row[6]
            longitude = row[7]
            zip_code = row[8]
            timezone = row[9]
            ip_ranges.append((start_ip, end_ip, {
                'country_code': country_code,
                'country': country,
                'province': province,
                'city': city,
                'latitude': latitude,
                'longitude': longitude,
                'zip_code': zip_code,
                'timezone': timezone
            }))
    end_time = time.time()
    print(f"CSV database loaded in {end_time - start_time:.2f} seconds")
    return ip_ranges

def search_ip(ip_int, ip_ranges):
    """二分查找IP地址"""
    left, right = 0, len(ip_ranges) - 1
    while left <= right:
        mid = (left + right) // 2
        start_ip, end_ip, info = ip_ranges[mid]
        if start_ip <= ip_int <= end_ip:
            return info
        elif ip_int < start_ip:
            right = mid - 1
        else:
            left = mid + 1
    return None

def get_local_ip():
    """获取本地IP地址"""
    try:
        import socket
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip
    except:
        return "Unknown"

def query_ip(ip, ip_ranges):
    """查询IP归属地"""
    try:
        ip_int = ip_to_int(ip)
        info = search_ip(ip_int, ip_ranges)
        if info:
            return info
        else:
            return {"error": "IP address not found"}
    except Exception as e:
        return {"error": str(e)}

def main():
    """主函数"""
    # 显示绿色ASCII艺术字工具名
    print("\n" + "="*60)
    green = Fore.GREEN
    reset = Style.RESET_ALL
    print(green + " /$$$$$$ /$$$$$$$           /$$$$$$                                         " + reset)
    print(green + "|_  $$_/| $$__  $$         /$$__  $$                                        " + reset)
    print(green + "  | $$  | $$  \\ $$        | $$  \\ $$ /$$   /$$  /$$$$$$   /$$$$$$  /$$   /$$" + reset)
    print(green + "  | $$  | $$$$$$$/ /$$$$$$| $$  | $$| $$  | $$ /$$__  $$ /$$__  $$| $$  | $$" + reset)
    print(green + "  | $$  | $$____/ |______/| $$  | $$| $$  | $$| $$$$$$$$| $$  \\__/| $$  | $$" + reset)
    print(green + "  | $$  | $$              | $$/$$ $$| $$  | $$| $$_____/| $$      | $$  | $$" + reset)
    print(green + " /$$$$$$| $$              |  $$$$$$/|  $$$$$$/|  $$$$$$$| $$      |  $$$$$$$" + reset)
    print(green + "|______/|__/               \\____ $$$ \\______/  \\_______/|__/       \\____  $$" + reset)
    print(green + "                                \\__/                               /$$  | $$" + reset)
    print(green + "                                                                  |  $$$$$$/" + reset)
    print(green + "                                                                   \\______/ " + reset)
    print("="*60)
    print(green + "        IP Address Query Tool" + reset)
    print("="*60)
    
    # 加载数据库
    database_path = 'data.csv'
    blue = Fore.BLUE
    green = Fore.GREEN
    red = Fore.RED
    reset = Style.RESET_ALL
    
    try:
        print("\n" + blue + "Loading IP database..." + reset)
        ip_ranges = load_ip_database(database_path)
        print(green + f"Database loaded successfully with {len(ip_ranges)} entries" + reset)
    except Exception as e:
        print(red + f"Error loading database: {e}" + reset)
        return
    
    # 主菜单
    while True:
        print("\n" + green + "Menu:" + reset)
        print(green + "1. Check my IP" + reset)
        print(green + "2. Query IP" + reset)
        print(green + "3. Exit" + reset)
        
        choice = input("\nSelect: ")
        
        if choice == "1":
            # 查询当前设备IP
            print("\n" + blue + "Checking your IP..." + reset)
            local_ip = get_local_ip()
            print(green + f"Your IP: {local_ip}" + reset)
            
            if local_ip != "Unknown":
                print(blue + "Querying location..." + reset)
                local_result = query_ip(local_ip, ip_ranges)
                if 'error' in local_result:
                    print(red + f"Note: {local_result['error']}" + reset)
                    print(red + "(Local IPs are usually private)" + reset)
                else:
                    print("\n" + green + "Location:" + reset)
                    print(green + f"Country: {local_result['country']} ({local_result['country_code']})" + reset)
                    print(green + f"Province: {local_result['province']}" + reset)
                    print(green + f"City: {local_result['city']}" + reset)
                    print(green + f"Latitude: {local_result['latitude']}" + reset)
                    print(green + f"Longitude: {local_result['longitude']}" + reset)
                    print(green + f"Zip Code: {local_result['zip_code']}" + reset)
                    print(green + f"Timezone: {local_result['timezone']}" + reset)
            
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            # 查询指定IP
            print("\n" + blue + "Query IP mode (enter 'back' to return)" + reset)
            
            while True:
                ip = input("\nIP: ")
                if ip.lower() == 'back':
                    break
                
                # 验证IP格式
                parts = ip.split('.')
                if len(parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                    print(red + "Invalid IP format" + reset)
                    continue
                
                result = query_ip(ip, ip_ranges)
                if 'error' in result:
                    print(red + f"Error: {result['error']}" + reset)
                else:
                    print("\n" + green + "Result:" + reset)
                    print(green + f"IP: {ip}" + reset)
                    print(green + f"Country: {result['country']} ({result['country_code']})" + reset)
                    print(green + f"Province: {result['province']}" + reset)
                    print(green + f"City: {result['city']}" + reset)
                    print(green + f"Latitude: {result['latitude']}" + reset)
                    print(green + f"Longitude: {result['longitude']}" + reset)
                    print(green + f"Zip Code: {result['zip_code']}" + reset)
                    print(green + f"Timezone: {result['timezone']}" + reset)
        
        elif choice == "3":
            # 退出
            print("\n" + green + "Goodbye!" + reset)
            break
        
        else:
            print(red + "Invalid choice. Enter 1-3." + reset)

if __name__ == "__main__":
    main()
