from flask import Flask, jsonify
import socket

app = Flask(__name__)

# Function to check server status via UDP
def check_udp_server(ip, port, query_packet):
    timeout = 5

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)

        sock.sendto(query_packet, (ip, port))
        response, _ = sock.recvfrom(4096)

        return {"status": "online", "response": response.decode('utf-8', errors='ignore')}
    except socket.timeout:
        return {"status": "offline", "error": "No response (timeout)"}
    except Exception as e:
        return {"status": "offline", "error": str(e)}
    finally:
        sock.close()

# Function to check server status via TCP
def check_tcp_server(ip, port):
    timeout = 5

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        sock.connect((ip, port))
        response = sock.recv(4096)

        return {"status": "online", "response": response.decode('utf-8', errors='ignore')}
    except socket.timeout:
        return {"status": "offline", "error": "No response (timeout)"}
    except Exception as e:
        return {"status": "offline", "error": str(e)}
    finally:
        sock.close()

# Halo: CE server status (UDP port)
@app.route('/halo/status', methods=['GET'])
def halo_status():
    server_ip = "67.219.110.143"  # Replace with your Halo server IP
    server_port = 2302  # Default Halo: CE UDP port
    query_packet = b"\\status\\"  # Halo query packet

    result = check_udp_server(server_ip, server_port, query_packet)
    return jsonify(result)

# TeamSpeak 3 voice port status (UDP port)
@app.route('/teamspeak/udp', methods=['GET'])
def teamspeak_udp_status():
    server_ip = "your-teamspeak-server-ip"  # Replace with your TeamSpeak server IP
    server_port = 9987  # Default TeamSpeak UDP port
    query_packet = b"ping"  # TeamSpeak query packet

    result = check_udp_server(server_ip, server_port, query_packet)
    return jsonify(result)

# TeamSpeak 3 Query Port status (TCP port)
@app.route('/teamspeak/query', methods=['GET'])
def teamspeak_query_status():
    server_ip = "your-teamspeak-server-ip"  # Replace with your TeamSpeak server IP
    server_port = 10011  # Default TeamSpeak Query port

    result = check_tcp_server(server_ip, server_port)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Expose Flask app on port 5000
