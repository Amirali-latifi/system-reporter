from datetime import datetime
import sqlite3
import time
#sqlite database
sql=sqlite3.connect("memorydata.db")
cursor=sql.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS memory_data(
        timestamp INTEGER,
        total INTEGER,
        free INTEGER,
        used INTEGER
)"""
)
#timestamp
now = datetime.now()
timestamp = int(datetime.timestamp(now))
def get_memory_info():
    mem_info = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            parts = line.split()
            key = parts[0].rstrip(':')
            value = int(parts[1])
            mem_info[key] = value
    total_memory = int(mem_info['MemTotal'])
    free_memory = mem_info['MemFree']
    available_memory = mem_info.get('MemAvailable',free_memory)
    used_memory = total_memory - available_memory
    return total_memory, used_memory, free_memory, available_memory
while True:
    total_memory, used_memory, free_memory, available_memory = get_memory_info()
    print(f"Total Memory: {total_memory / 1024:.2f} MB")
    print(f"Used Memory: {used_memory / 1024:.2f} MB")
    print(f"Free Memory: {free_memory / 1024:.2f} MB")
    print(f"Available Memory: {available_memory / 1024:.2f} MB")
    print("60 sec")
    cursor.execute("""INSERT INTO memory_data(timestamp,total,free,used) VALUES(?,?,?,?)""",
                  (timestamp,total_memory,free_memory,used_memory))
    sql.commit()
    time.sleep(60)
sql.close()

