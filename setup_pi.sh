#!/bin/bash
# sudo apt update && sudo apt upgrade && sudo apt install wget
# wget https://raw.githubusercontent.com/YAlsaady/IGUS_Delta_Robot/main/autosart.sh | bash

# while true; do
#
# read -p "Setup german Keyboard and locale? (Y/n) " CHOISE
#
# case $CHOISE in 
# 	y ) echo "german Keyboard and locale will be setup";
# 		break;;
# 	n ) echo "Keyboard and locale will not be changed";
# 		break;;
# 	* ) echo invalid response;;
# esac

if [ ! $SSID ] || [ ! $PSK ]; then
  read -p 'SSID: ' SSID
  read -sp 'Password: ' PSK
fi

# Assign a static IP address
sudo nmcli connection add \
type wifi \
ipv4.method auto \
ip4 192.168.1.11 \
gw4 192.168.1.1 \
wifi-sec.key-mgmt wpa-psk \
con-name "$SSID" \
ssid "$SSID" \
wifi-sec.psk "$PSK" \

sudo systemctl enable --now NetworkManager.service
sudo systemctl restart NetworkManager.service

# Update
sudo apt update
sudo apt upgrade -y

# Install the dependencies
sudo apt install python3-full git network-manager onboard -y
# sudo apt install python3-pymodbus python3-numpy python3-serial -y
pip3 install --break-system-packages pyModbusTCP pyserial numpy

# Clone the repository
if [ ! -d /home/$USER/src ]; then
    mkdir /home/$USER/src
fi

if [ ! -d /home/$USER/src/IGUS_Delta_Robot ]; then
    git clone --depth=1 https://github.com/YAlsaady/IGUS_Delta_Robot.git /home/$USER/src/IGUS_Delta_Robot
else cd /home/$USER/src/IGUS_Delta_Robto && git pull
fi

cd

# Autostart
## Desktop Entry
if [ ! -d /home/$USER/.config/autostart ]; then
    mkdir /home/$USER/.config/autostart
fi
echo "\
[Desktop Entry]
Name=User
Comment= Run the Delta-GUI and the gripper_global.py script
Type=Application
Exec=/usr/local/bin/delta.sh \
--not-show-in=GNOME,\
GNOME-Classic:GNOME \
--startup-delay=3.0
X-GNOME-Autostart-enable=true
X-GNOME-AutoRestart=true\
" > /home/$USER/.config/autostart/delta.desktop
chmod +x /home/$USER/.config/autostart/delta.desktop

## Autostart-Script
echo "\
#!/bin/bash

cd
sleep 2
python3 src/IGUS_Delta_Robot/Modbus/gripper_global.py&
sleep 2
python3 src/IGUS_Delta_Robot/Modbus/main.py&\
" > /home/$USER/delta.sh
chmod +x /home/$USER/delta.sh
sudo mv /home/$USER/delta.sh /usr/local/bin/delta.sh

# Wallpaper
if [ -f /home/$USER/.config/pcmanfm/LXDE-pi/desktop-items-0.conf ]; then
  rm /home/$USER/.config/pcmanfm/LXDE-pi/desktop-items-0.conf
fi
if [ ! -d /home/$USER/.config/pcmanfm/LXDE-pi ]; then
  mkdir -p /home/$USER/.config/pcmanfm/LXDE-pi
fi
echo "\
[*]
wallpaper_mode=fit
wallpaper_common=1
wallpaper=/home/$USER/src/IGUS_Delta_Robot/Modbus/GUI/img/campus_voll-1124x621.jpg
desktop_bg=#000000
desktop_fg=#e8e8e8
desktop_shadow=#000000
desktop_font=PibotoLt 24
show_wm_menu=0
sort=mtime;ascending;
show_documents=0
show_trash=1
show_mounts=1

[alacarte-made.desktop]
x=2
y=943\
" > /home/$USER/.config/pcmanfm/LXDE-pi/desktop-items-0.conf

# Menu
mkdir -p /home/$USER/.local/share/applications
if [ -f /home/$USER/.local/share/applications/alacarte-made.desktop ]; then
  rm /home/$USER/.local/share/applications/alacarte-made.desktop
fi
echo "\
[Desktop Entry]
Name=Delta
Exec=python3 src/IGUS_Delta_Robot/Modbus/main.py
Comment=GUI App for the Delta Robot
Terminal=false
Icon=/home/$USER/src/IGUS_Delta_Robot/Modbus/GUI/img/hsel_icon.png
Type=Application\
" > /home/$USER/.local/share/applications/alacarte-made.desktop

mkdir -p /home/$USER/.config/menus
if [ -f /home/$USER/.config/menus/lxde-pi-applications.menu ]; then
  rm /home/$USER/.config/menus/lxde-pi-applications.menu
fi
echo "\
<?xml version=\"1.0\" ?>
<!DOCTYPE Menu
  PUBLIC '-//freedesktop//DTD Menu 1.0//EN'
  'http://standards.freedesktop.org/menu-spec/menu-1.0.dtd'>
<Menu>
	<Name>Applications</Name>
	<MergeFile type=\"parent\">/etc/xdg/menus/lxde-pi-applications.menu</MergeFile>
	<Include>
		<Filename>alacarte-made.desktop</Filename>
	</Include>
	<Layout>
		<Merge type=\"menus\"/>
		<Filename>alacarte-made.desktop</Filename>
		<Menuname>Development</Menuname>
		<Menuname>Education</Menuname>
		<Menuname>Office</Menuname>
		<Menuname>Internet</Menuname>
		<Menuname>Multimedia</Menuname>
		<Menuname>Graphics</Menuname>
		<Menuname>Games</Menuname>
		<Menuname>Other</Menuname>
		<Menuname>System</Menuname>
		<Menuname>Accessories</Menuname>
		<Menuname>Universal Access</Menuname>
		<Separator/>
		<Menuname>Help</Menuname>
		<Separator/>
		<Menuname>DesktopSettings</Menuname>
		<Merge type=\"files\"/>
	</Layout>
</Menu>\
" > /home/$USER/.config/menus/lxde-pi-applications.menu


# Panel
if [ /home/$USER/.config/lxpanel/LXDE-pi/panels/panel ]; then 
  rm /home/$USER/.config/lxpanel/LXDE-pi/panels/panel
fi
echo "\
# lxpanel <profile> config file. Manually editing is not recommended.
# Use preference dialog in lxpanel to adjust config when you can.

Global {
  edge=top
  align=left
  margin=0
  widthtype=percent
  width=100
  height=52
  transparent=0
  tintcolor=#000000
  alpha=0
  autohide=0
  heightwhenhidden=2
  setdocktype=1
  setpartialstrut=1
  usefontcolor=0
  fontsize=12
  fontcolor=#ffffff
  usefontsize=0
  background=0
  backgroundfile=/usr/share/lxpanel/images/background.png
  iconsize=52
  monitor=0
  point_at_menu=0
}
Plugin {
  type=smenu
  Config {
    padding=4
    image=start-here
    system {
    }
    separator {
    }
    item {
      image=system-run
      command=run
    }
    separator {
    }
    item {
      image=system-shutdown
      command=logout
    }
  }
}
Plugin {
  type=launchbar
  Config {
    Button {
      id=lxde-x-www-browser.desktop
    }
    Button {
      id=pcmanfm.desktop
    }
    Button {
      id=lxterminal.desktop
    }
  }
}
Plugin {
  type=space
  Config {
    Size=8
  }
  expand=0
}
Plugin {
  type=launchbar
  Config {
    Button {
      id=alacarte-made.desktop
    }
  }
}
Plugin {
  type=taskbar
  expand=1
  Config {
    tooltips=1
    IconsOnly=0
    ShowAllDesks=0
    UseMouseWheel=1
    UseUrgencyHint=1
    FlatButton=0
    MaxTaskWidth=300
    spacing=1
    GroupedTasks=0
  }
}
Plugin {
  type=space
  Config {
    Size=2
  }
}
Plugin {
  type=tray
  Config {
  }
}
Plugin {
  type=updater
  Config {
  }
}
Plugin {
  type=ejecter
  Config {
    AutoHide=1
  }
}
Plugin {
  type=space
  Config {
    Size=2
  }
}
Plugin {
  type=bluetooth
  Config {
  }
}
Plugin {
  type=space
  Config {
    Size=2
  }
}
Plugin {
  type=netman
  Config {
  }
}
Plugin {
  type=dhcpcdui
  Config {
  }
}
Plugin {
  type=space
  Config {
    Size=2
  }
}
Plugin {
  type=volumepulse
  Config {
  }
}
Plugin {
  type=micpulse
  Config {
  }
}
Plugin {
  type=space
  Config {
    Size=2
  }
}
Plugin {
  type=dclock
  Config {
    ClockFmt=%R
    TooltipFmt=%A %x
    BoldFont=0
    IconOnly=0
    CenterText=1
  }
}
Plugin {
  type=space
  Config {
    Size=2
  }
}
Plugin {
  type=ptbatt
  Config {
  }
}
Plugin {
  type=space
  Config {
    Size=2
  }
}
Plugin {
  type=magnifier
  Config {
  }
}\
" > /home/$USER/.config/lxpanel/LXDE-pi/panels/panel
sudo reboot
