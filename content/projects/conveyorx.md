---
title: ConveyorX
short_description: Real-time conveyor belt monitoring system using STM32F401VE to
  track object speed and count via IR sensors and PWM motor control.
overview_image_id: BZkkcXF2/453623025-984412f8-db41-4e62-95c0-4b706ce76adc.png
year: '2025'
domain_id: embedded_systems
category_id: embedded_systems_iot
github_link: https://github.com/YassienTawfikk/ConveyorX.git
video_demo: https://github.com/user-attachments/assets/6a6e361f-a388-491d-9a0c-7f26c36ff87f
tech_stack:
- C
- STM32F401VE
- CMake
- Proteus
- GPIO
- PWM
- ADC
- LCD
tags:
- Embedded Systems
- STM32
- Automation
- Object Detection
- Speed Measurement
- C Programming
- Proteus Simulation
highlights:
- Precise conveyor speed measurement using Timer Input Capture.
- Reliable object counting via IR sensors and GPIO polling.
- Adjustable DC motor speed control using PWM and Potentiometer (ADC).
- Real-time visualization of Speed and Object Count on an LCD interface.
- Modular driver design including RCC, GPIO, PWM, and LCD.
---

ConveyorX is a real-time embedded system developed on the STM32F401VE microcontroller designed to simulate and monitor an industrial conveyor belt environment. It utilizes Timer Input Capture to accurately measure belt speed and employs IR sensors with GPIO polling to count objects passing through the system. The project features a dynamic motor control system where speed is regulated via PWM based on potentiometer input (ADC), with all critical metrics displayed in real-time on an LCD screen.
