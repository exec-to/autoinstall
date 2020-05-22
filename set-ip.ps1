# Configure IP Address, Subnet & Gateway in Windows using PowerShell

# Variables
$IPAddress = "109.248.222.111"
$IPSubnetPrefix = "255.255.255.0"
$IPGateway = "109.248.222.1"

$ifaceindex = get-wmiobject win32_networkadapter -filter "netconnectionstatus = 2" | select -expand InterfaceIndex
netsh interface ipv4 set address name=$ifaceindex source=static addr=$IPAddress  mask=$IPSubnetPrefix gateway=$IPGateway gwmetric=1
netsh interface ipv4 add dns $ifaceindex 8.8.8.8 index=1
