---
title: Press2Display
short_description: Modular embedded system interfacing a 4x3 matrix keypad with a
  2-digit 7-segment display using an STM32F401VE.
overview_image_id: HWVFyQr4/449270137-194055fe-b6da-4612-b0b3-9ff41593cdd5.png
year: '2025'
domain_id: embedded_systems
category_id: embedded_systems_iot
github_link: https://github.com/YassienTawfikk/Press2Display.git
video_demo: https://github.com/user-attachments/assets/5651b9b6-9adb-42f5-9cc9-276a65331b49
tech_stack:
- C
- STM32F401VE
- CMake
- Proteus
- GPIO
- Keypad Driver
tags:
- Embedded Systems
- STM32
- Keypad Interfacing
- Multiplexing
- C Programming
- Firmware
- Proteus Simulation
highlights:
- Flexible GPIO remapping utilizing PinConfig abstraction.
- Real-time 2-digit multiplexed 7-segment display rendering.
- Matrix keypad scanning algorithm with debounce handling.
- Lookup table-based digit rendering replacing complex switch-case logic.
- Modular driver architecture ensuring compatibility with Proteus and real hardware.
---

Press2Display is a modular embedded system that interfaces a 4x3 matrix keypad with a 2-digit 7-segment display using the STM32F401VE microcontroller. It demonstrates key principles of driver abstraction, multiplexing, and efficient GPIO remapping in embedded C. The system scans the keypad row-by-row, maps inputs via a lookup table, and updates the display using high-speed multiplexing for flicker-free output. Designed for educational simulation and hardware deployment, it highlights robust low-level software design.
