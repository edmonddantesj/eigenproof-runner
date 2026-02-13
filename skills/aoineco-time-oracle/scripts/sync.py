#!/usr/bin/env python3
import datetime
import time
import socket
import struct
import sys

def get_ntp_time(host="pool.ntp.org"):
    try:
        port = 123
        buf = 48
        address = (host, port)
        msg = '\x1b' + 47 * '\0'
        
        # Reference time (in seconds since 1900-01-01 00:00:00)
        TIME1900 = 2208988800
        
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(5)
        client.sendto(msg.encode('utf-8'), address)
        msg, address = client.recvfrom(buf)
        
        t = struct.unpack("!12I", msg)[10]
        t -= TIME1900
        return t
    except Exception as e:
        return None

def sync(tz_offset=9):
    local_now = time.time()
    ntp_now = get_ntp_time()
    
    if ntp_now is None:
        print("ERROR|NTP sync failed")
        return

    drift = ntp_now - local_now
    
    # Dynamic offset for Global Agents
    offset_seconds = tz_offset * 3600
    target_time = datetime.datetime.fromtimestamp(ntp_now + offset_seconds)
    
    print(f"SUCCESS|{target_time.strftime('%Y-%m-%d %H:%M:%S')}|{drift:.4f}|UTC{tz_offset:+}")

if __name__ == "__main__":
    # Default to 9 (KST) if no arg provided
    offset = float(sys.argv[1]) if len(sys.argv) > 1 else 9
    sync(offset)
