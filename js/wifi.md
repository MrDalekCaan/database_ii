Create a symlink to the AirPort command in Terminal
`ln -s /System/Library/PrivateFrameworks/Apple80211.framework/
Versions/Current/Resources/airport /Usr/bin/airport`

Network connections list
​networksetup -listallhardwareports

Enable or Disable Wi-Fi
networksetup -setairportpower en0 on (or off)


networksetup -getinfo "wi-fi"

View available Wi-Fi networks
​airport -s

Join Wi-Fi network
networksetup -setairportnetwork en0 SSID_OF_WIRELESS_NETWORK WIRELESS_NETWORK_PASSPHRASE