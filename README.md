# PulseAudioPython
Simple scripts to control PulseAudio through Python

## Project Overview
This project will provide two speaker configurations listed as virtual devices (VD vs sink?)
Each device will link multiple speakers
### Type 1: High Priority
This setup is for low-latency requirements for audio: movies, video games, active audio
    Default setup for hardware-only audio
    Lose speakers that will require higher latency
    Low buffer size, keep latency below 80ms total, maybe even below 20ms. We will see how this works.
    
### Type 2: Low Priority
This setup is for music, high-latency allowed
    Default for bluetooth/airplay speakers.
    Possibly default for music player like spotify? Or provide easy transition.
    This will also be used once network-audio is active
    This incorporates all speakers with up to 2s latency and plays audio accordingly.
    Larger buffers, focusing on not losing any audio at the cost of latency