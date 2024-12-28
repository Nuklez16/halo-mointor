from flask import Flask, jsonify
import socket

app = Flask(__name__)

# Function to check the Halo:CE server status
def check_halo_server(ip, port=2302):
    query_packet = b"\\status\\"
    timeout = 5

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)

        sock.sendto(query_packet, (ip, port))
        response, _ = sock.recvfrom(4096)
        response = response.decode('utf-8', errors='ignore')

        return {"status": "online", "response": response}
    except socket.timeout:
        return {"status": "offline", "error": "No response (timeout)"}
    except Exception as e:
        return {"status": "offline", "error": str(e)}
    finally:
        sock.close()

# Flask route to check the Halo:CE server status
@app.route('/halo/status', methods=['GET'])
def halo_status():
    server_ip = "67.219.110.143"  # Replace with your Halo:CE server IP
    server_port = 2302  # Default UDP port for Halo:CE

    result = check_halo_server(server_ip, server_port)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Expose on port 5000
