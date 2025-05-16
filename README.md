<p align="center"><img alt="AeroPi" src="logo.png" width="400"></p>

## About
This project was developed for a hackathon to create detailed 3D terrain maps of disaster zones using advanced photogrammetry techniques. Leveraging COLMAP, the system reconstructs high-resolution 3D models from aerial imagery captured by a coordinated drone swarm. Before processing, images are enhanced using an image denoising CNN (DnCNN) model to optimize feature extraction. The denoised images are then transmitted via the AT&T network to a server equipped with CUDA GPU acceleration, where COLMAP generates the final 3D renders.

Beyond disaster response, this technology has versatile business applications, including:

- **3D Modeling of Cell Towers and Equipment:** Enabling precise asset management and inspection.
- **Small Cell Deployment in Urban Areas:** Facilitating optimal placement and planning through detailed urban terrain mapping.
- **Disaster Recovery:** Providing first responders with rapid and accurate situational awareness to improve operational decisions.
- **Real Estate and Site Acquisition:** Offering immersive 3D visualizations for better property assessment and planning.

This integrated system combines edge computing on Raspberry Pi prototypes for initial processing with high-performance GPU servers for advanced 3D reconstruction, demonstrating a scalable pipeline from drone data capture to actionable 3D outputs.

## Dependencies
**Hardware**
* [**Raspberry Pi 5**](https://www.raspberrypi.com/products/raspberry-pi-5/): The latest Raspberry Pi model featuring a quad-core Arm Cortex-A76 processor at 2.4GHz, dual 4Kp60 HDMI outputs, and PCIe Gen 3 support.
* [**Raspberry Pi AI Kit (HAT+) – 26 TOPS**](https://www.raspberrypi.com/products/ai-kit/): An add-on for the Pi 5 using the Hailo-8 accelerator, delivering up to 26 TOPS for efficient edge AI inference.
* NVIDIA Graphics Card with the CUDA SDK installed (<em>a RTX 5070 TI was used in this project and took ~2 hours to compute the 3D mesh from COLMAP</em>)
* Drone(s) with a camera (<em>note -- we did not use one in this project due to budgeting</em>)

## Resources & Notes
1. <em>[Colmap-PCD: An Open-source Tool for Fine Image-to-point cloud Registration](https://arxiv.org/abs/2310.05504)</em>
2. [ColMap Github](https://github.com/colmap/colmap)
3. 
