By default Jetson Nano 2GB Developer Kit supports Raspberry Pi V2 camera (IMX219). To work with Raspberry Pi High Definition Camera (IMX477) connected to Jetson Nano 2GB Developer Kit, please follow the steps below:

NOTE: Once the below steps are executed, only IMX477 would work with the developer kit. To go back to working with Raspberry Pi V2 camera (IMX219), please refer to the next section below.

1. Copy bl_update_payload_imx477 from the downloaded tar file to /usb/sbin on the developer kit
Run the following commands -
2. cd /usr/sbin
3. sudo dpkg-reconfigure nvidia-l4t-bootloader
4. sudo l4t_payload_updater_t210 bl_update_payload_imx477
5. Copy libnvodm_imager.so included in the tar on to the Jetson developer kit to the path shown below.
   -	sudo cp libnvodm_imager.so /usr/lib/aarch64-linu-gnu/tegra/libnvodm_imager.so
6. Reboot the device

NOTE: When working with IMX 477 camera, orientation of the preview can be rotated by 180 degrees. To rotate the camera preview, please refer to the section "Video Rotation with GStreamer-1.0"  in Jetson Developer Guide (https://docs.nvidia.com/jetson/l4t/index.html) under "Accelerated GStreamer" section.

To go back to working with Raspberry Pi V2 camera (IMX219) connected to Jetson Nano 2GB Developer Kit, please follow below steps:
NOTE: Once the below steps are executed, only IMX219 would work with the developer kit.

1. Copy bl_update_payload_imx219 from the downloaded tar file to /usb/sbin on the developer kit
Run the following commands -
2. cd /usr/sbin
3. sudo dpkg-reconfigure nvidia-l4t-bootloader
4. sudo l4t_payload_updater_t210 bl_update_payload_imx219
5. reboot the device

To use the customized dtb and generate the payload itself for IMX477, you will need access to a x86 host. On the host
1. cd Linux_for_tegra
2. sudo ./l4t_generate_soc_bup.sh t21x
3. cp bootloader/payload_t21x/bl_update_payload bootloader/payload_t21x/bl_update_payload_imx219
4. copy IMX477's dtb from the tar file (tegra210-p3448-0003-p3542-0000.dtb) to Linux_for_Tegra/kernel/dtb
5. cd Linux_for_tegra
6. sudo ./l4t_generate_soc_bup.sh t21x
7. cp bootloader/payload_t21x/bl_update_payload bootloader/payload_t21x/bl_update_payload_imx477
8. copy bl_update_payload_imx219 and bl_update_payload_imx477 to device /usr/sbin.
On the target
9. cd /usr/sbin
10. sudo l4t_payload_updater_t210 bl_update_payload_imx477
11. Copy libnvodm_imager.so included in the tar on to the Jetson developer kit at the path shown below.
   -	sudo cp libnvodm_imager.so /usr/lib/aarch64-linu-gnu/tegra/
12. reboot the device

