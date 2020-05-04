
import socket

forwarding_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
forwarding_socket.connect(('localhost', 8080))

forwarding_socket.send("""POST /var/phpsessid= HTTP/1.1\r\nHost: localhost:5000\r\nContent-Length: 10\r\n\r\ntxt=<script>adasdas</script""")

forwarding_socket.close()