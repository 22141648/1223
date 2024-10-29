from netmiko import ConnectHandler

# Define device connection details
device = {
    'device_type': 'cisco_ios',  
    'host': '192.168.56.101',    # Update with your device's IP
    'username': 'cisco',         # Update with your username
    'password': 'cisco',         # Update with your password
    'secret': 'cisco',           # Enable password
}

# Connect to the device
def connect_to_device():
    try:
        net_connect = ConnectHandler(**device)
        net_connect.enable()  # Enter enable mode
        return net_connect
    except Exception as e:
        print(f"Failed to connect: {str(e)}")
        return None

# Configure ACLs on the device
def configure_acl(net_connect):
    acl_commands = [
        'access-list 10 permit 192.168.1.0 0.0.0.255',
        'access-list 10 deny any',
        'interface GigabitEthernet0/1',
        'ip access-group 10 in'
    ]

    try:
        output = net_connect.send_config_set(acl_commands)
        print("ACL configuration applied:\n", output)
    except Exception as e:
        print(f"Failed to configure ACL: {str(e)}")

# Configure basic IPSec on the device
def configure_ipsec(net_connect):
    ipsec_commands = [
        'crypto isakmp policy 10',
        'encryption aes 256',
        'hash sha256',
        'authentication pre-share',
        'group 14',
        'lifetime 86400',
        'exit',
        'crypto isakmp key cisco123 address 192.168.2.1',
        'crypto ipsec transform-set MY_TRANSFORM_SET esp-aes 256 esp-sha-hmac',
        'access-list 100 permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255',
        'crypto map MY_CRYPTO_MAP 10 ipsec-isakmp',
        'set peer 192.168.2.1',
        'set transform-set MY_TRANSFORM_SET',
        'match address 100',
        'exit',
        'interface GigabitEthernet0/1',
        'crypto map MY_CRYPTO_MAP'
    ]

    try:
        output = net_connect.send_config_set(ipsec_commands)
        print("IPSec configuration applied:\n", output)
    except Exception as e:
        print(f"Failed to configure IPSec: {str(e)}")

# Main script execution
def main():
    net_connect = connect_to_device()
    
    if net_connect:
        print("Connected to device successfully.")
        
        # Configure ACL
        configure_acl(net_connect)
        
        # Configure IPSec
        configure_ipsec(net_connect)

        # Save configuration
        try:
            save_output = net_connect.send_command('write memory')
            print("Configuration saved:\n", save_output)
        except Exception as e:
            print(f"Failed to save configuration: {str(e)}")

        # Disconnect from the device
        net_connect.disconnect()
    else:
        print("Could not establish connection to device.")

# Run the script
if __name__ == "__main__":
    main()
