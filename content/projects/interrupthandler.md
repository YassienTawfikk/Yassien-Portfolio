---
category_id: embedded_systems_iot
domain_id: embedded_systems
github_link: https://github.com/YassienTawfikk/InterruptHandler.git
highlights:
- Custom EXTI driver supporting rising, falling, and dual-edge triggers.
- Real-time counter updates via ISRs with 3-digit 7-segment display multiplexing.
- Critical section protection using __disable_irq() to prevent race conditions.
- Three-button interface for counter control (Increment/Decrement) and LED toggling.
- Designed for both Proteus simulation and hardware deployment.
order: 5
overview_image_id: 05FFdbSp/449271529-71f2e2ad-f7e6-4b17-839e-11ace7bb7ff3.png
short_description: Real-time embedded project demonstrating external interrupts (EXTI)
  to control a 7-segment display and LED using an STM32F401VE.
tags:
- Embedded Systems
- STM32
- Real-Time
- Interrupts
- Firmware
- Proteus Simulation
- C Programming
tech_stack:
- C
- STM32F401VE
- CMake
- Proteus
- GPIO
- EXTI
title: InterruptHandler
video_demo: https://github.com/user-attachments/assets/4482cfc3-b778-4457-8908-76c10578a72c
year: '2025'
---

InterruptHandler is a real-time embedded system built on the STM32F401VE microcontroller. It features a custom External Interrupt (EXTI) driver to manage hardware events from three push buttons, allowing for immediate response to user input. The system controls a multiplexed 3-digit 7-segment display and an LED indicator. Key engineering principles demonstrated include interrupt-driven input handling, race condition protection via critical sections, and efficient display multiplexing to ensure smooth visual output.