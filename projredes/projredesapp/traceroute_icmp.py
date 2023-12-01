import socket
import struct
import time
import re
import matplotlib.pyplot as plt
import numpy
rtt_array = []
num_hops = []
ip_addresses = []


def checksum(data):
    # Função para calcular o checksum do cabeçalho ICMP
    if len(data) % 2 != 0:
        data += b'\x00'
    words = struct.unpack('!{0}H'.format(len(data) // 2), data)
    chksum = sum(words)
    chksum = (chksum >> 16) + (chksum & 0xFFFF)
    chksum += chksum >> 16
    return ~chksum & 0xFFFF


def send_icmp_packet(dest_addr, ttl):
    # Construir cabeçalho ICMP Echo Request
    icmp_type = 8  # Echo Request
    icmp_code = 0
    icmp_checksum = 0
    icmp_identifier = 12345
    icmp_sequence = 1

    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum,
                              icmp_identifier, icmp_sequence)

    # Calcular o checksum para o cabeçalho ICMP
    icmp_checksum = checksum(icmp_header)

    # Atualizar o cabeçalho com o checksum calculado
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum,
                              icmp_identifier, icmp_sequence)

    # Criar socket ICMP
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    icmp_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

    # Enviar pacote ICMP
    icmp_socket.sendto(icmp_header, (dest_addr, 0))

    # Registrar o tempo de envio
    send_time = time.time()

    return icmp_socket, send_time


def receive_icmp_response(icmp_socket, send_time):
    # Esperar por uma resposta ICMP
    while True:
        icmp_socket.settimeout(1.0)
        try:
            response, addr = icmp_socket.recvfrom(1024)
            receive_time = time.time()
        except socket.timeout:
            return None, None

        # Extrair o tipo de ICMP e código da resposta
        icmp_type, icmp_code = struct.unpack('!BB', response[20:22])

        # Verificar se é uma resposta Time Exceeded ou Echo Reply
        if icmp_type == 11 and icmp_code == 0:
            # Time Exceeded
            return addr[0], receive_time - send_time
        elif icmp_type == 0 and icmp_code == 0:
            # Echo Reply
            return addr[0], receive_time - send_time


def traceroute_icmp(destination, max_hops=30, timeout=2):
    port = 33434  # Porta padrão usada pelo traceroute

    for ttl in range(1, max_hops + 1):
        # Enviar pacote ICMP com o TTL atual
        icmp_socket, send_time = send_icmp_packet(destination, ttl)

        # Receber resposta ICMP
        addr, rtt = receive_icmp_response(icmp_socket, send_time)

        # Fechar o socket ICMP
        icmp_socket.close()

        # Exibir informações
        if addr is not None:
            rtt_array.append(round(rtt * 1000, 2))
            ip_addresses.append(addr)
            print(f"{ttl}: {addr}  RTT: {round(rtt * 1000, 2)} ms")
        else:
            rtt_array.append(0)
            ip_addresses.append("*")
            print(f"{ttl}: *")

        num_hops.append(ttl)

        # Verificar se é a resposta final
        # ip_regex = "\d\.\d\.\d\.\d"
        # if  not re.match(ip_regex,destination):
        #     destination = socket.gethostbyname(destination)

        if addr == destination:
            break
        elif ttl == max_hops:
            print("ICMP Type: 11")
            print("ICMP Code: 0")
            print("TTL expired in transit")


def create_bar_plot(rtt_array, num_hops):
    # Dados para o gráfico de barras
    rtts = rtt_array
    hops = num_hops

    # Criar um gráfico de barras
    bars = plt.bar(hops, rtts, color='blue')

    # Adicionar rótulos em cima das barras
    for bar, ip in zip(bars, ip_addresses):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, f'{ip}', ha='center', color='black',
                 size='x-small', rotation=45)

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    # Adicionar rótulos e título
    plt.xlabel('Hops')
    plt.ylabel('Rtts(ms)')

    # Exibir o gráfico
    #plt.savefig('projredesapp/static/projredesapp/images/fig.png', dpi=300, bbox_inches='tight')
    plt.savefig("C:/Users/franc/OneDrive/Área de Trabalho/projrede/projredes/projredesapp/static/projredesapp/images/graph.jpg") 
    plt.show()


def validate_ip_address(ip):
    ip_regex = r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$'
    return re.match(ip_regex, ip) is not None


def validate_ttl(ttl):
    ttl_regex = r'^[1-9][0-9]*$'
    return re.match(ttl_regex, ttl) is not None

'''
if __name__ == "__main__":
    while True:
        destination_ip = input("Digite o endereço IP de destino: ")
        if validate_ip_address(destination_ip):
            max_hops = input("Digite o número máximo de saltos (TTL): ")
            if validate_ttl(max_hops):
                break
            else:
                print("Formato inválido do TTL")
        else:
            print("Formato inválido do IP")

    traceroute_icmp(destination_ip, int(max_hops))
    create_bar_plot(rtt_array, num_hops)
'''