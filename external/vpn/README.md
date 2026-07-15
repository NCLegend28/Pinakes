# Simple VPN Implementation

A basic VPN implementation to learn VPN fundamentals using Python and TUN interfaces.

## Files

1. **simple_vpn.py** - Basic TUN interface demo
2. **vpn_server.py** - Basic unencrypted VPN server
3. **vpn_client.py** - Basic unencrypted VPN client  
4. **secure_vpn_server.py** - Encrypted VPN server
5. **secure_vpn_client.py** - Encrypted VPN client

## Requirements

```bash
pip install cryptography
```

## How VPN Works

1. **TUN Interface**: Virtual network interface that captures IP packets
2. **Tunnel**: Encrypted connection between client and server
3. **Encapsulation**: Original packets wrapped in encrypted envelope
4. **Routing**: Traffic redirected through VPN tunnel

## Usage

### Basic TUN Demo

**Linux:**
```bash
sudo python3 simple_vpn.py
# In another terminal:
sudo ip addr add 10.8.0.1/24 dev tun0
sudo ip link set tun0 up
ping 10.8.0.2  # Watch packets being captured
```

**macOS:**
```bash
sudo python3 macos_vpn.py
# In another terminal:
sudo ifconfig utun2 10.8.0.1 10.8.0.2
ping 10.8.0.2  # Watch packets being captured
```

### Basic VPN (Unencrypted)

**Linux:**
```bash
# Server:
sudo python3 vpn_server.py
sudo ip addr add 10.8.0.1/24 dev tun0
sudo ip link set tun0 up

# Client:
sudo python3 vpn_client.py
sudo ip addr add 10.8.0.2/24 dev tun1  
sudo ip link set tun1 up
```

**macOS:**
```bash
# Server:
sudo python3 macos_vpn_server.py

# Client:
sudo python3 macos_vpn_client.py
```

### Secure VPN (Encrypted)
```bash
# Server:
sudo python3 secure_vpn_server.py mypassword
sudo ip addr add 10.8.0.1/24 dev tun0
sudo ip link set tun0 up
sudo iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -o eth0 -j MASQUERADE
sudo sysctl -w net.ipv4.ip_forward=1

# Client:  
sudo python3 secure_vpn_client.py 127.0.0.1 mypassword
sudo ip addr add 10.8.0.2/24 dev tun1
sudo ip link set tun1 up
```

## Security Features

- **PBKDF2**: Password-based key derivation
- **Fernet encryption**: Symmetric encryption with authentication
- **Packet integrity**: Prevents tampering
- **Forward secrecy**: Keys derived from passwords

## Learning Points

1. **TUN interfaces** capture layer 3 IP packets
2. **Encapsulation** wraps packets for transport
3. **Encryption** protects data in transit
4. **Routing** directs traffic through tunnel
5. **NAT/Masquerading** allows internet access

## Production Considerations

- Use certificates instead of passwords
- Implement proper key exchange
- Add compression
- Handle MTU discovery
- Implement reconnection logic
- Add logging and monitoring