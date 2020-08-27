import pulsectl

# TODO: Write combine method
# Put more code into main or some setup file. 
# Allow for conditions where some specified devices are not available
# Make sure latency is configured properly
# Play with channel maps to put speakers in correct position to sound best
# Try with and without hdmi audio

DEFAULT_DEVICES = {
    "bluetooth_speakers": "bluez...",
    "external_speakers": "alas.generic_usb...",
    "hdmi": "nvidia_hdmi_driver...",
    "sport": "weird_sport_bluetooth...",
}

def main():
    # Combines speakers together, remapping bluetooth, sets this as default
    devices = DEFAULT_DEVICES
    
    pulse = pulsectl.Pulse()
    sources = pulse.source_list()
    
    remapped_properties = {
        "sink_properties": "device.description=RemappedLogiSpeakers",
        "sink_name": "RemappedLogiSpeakers",
    }
    bluetooth_channel_map = {
        # Dict of input_channel: output_channel
    }
    
    combined_properties = {
        "sink_properties": "device.description=CombinedSpeakers",
        "sink_name": "CombinedSpeakers",
    }
    
    remapped_bluetooth = remap(devices["bluetooth_speakers"], channel_map
                               module_properties=remapped_properties)
    
    combined_sources = list(map(lambda a: a.name, source_list
    for i in [
        remapped_bluetooth.name, 
        main_monitor_hdmi.name, 
        external_speakers.name
    ]
    
    combined_audio = combine(combined_sources, pulse_initial=pulse, 
                             module_properties=combined_properties)


def remap(source_name, pulse_initial=None, **kwargs):
    # source_name contains name identifiers for sound source 
    # sink_name contains name identifiers for sound sink 
    # kwargs: passed to load-module
    # Returns: true if successful, false if not
    if pulse_initial is None:
        pulse = pulsectl.Pulse()
    else:
        pulse = pulse_initial
    
    loop_id = pulse.module_load('module-loopback', **kwargs)
    
    
    if loop_id > 100000:
        print("Invalid loop id")
        return
    
      # Find the newly created sink-input
    loop_sink_input = None
    for si in pulse.sink_input_list():
        if si.owner_module == loop_id:
            print("Sink-input: %s" % si.index)
            loop_sink_input = si

    if loop_sink_input == None:
        print("Could not find newly created sink-input")
        return
   
  # Find the newly created source-output
    loop_source_output = None
    for so in pulse.source_output_list():
        if so.owner_module == loop_id:
            print("Source-output: %s" % so.index)
            loop_source_output = so

    if loop_source_output == None:
        print("Could not find newly created source-output")
        return

def loopback(source_name, sink_name, latency_msec=1, pulse_initial=None):
    # TODO: FIGURE OUT IF PULSEAUDIO KNOWS IF LATENCY IS IN ADDITION TO EXTERNAL SPEAKERS, OR
    #   IF I SHOULD COPY LATENCY FROM EXTERNAL SPEAKERS BEFORE LOOPBACK
    # source_name contains name identifiers for sound source 
    # sink_name contains name identifiers for sound sink 
    # latency_msec contains desired loopback latency
    # pulse_initial: instance of pulsectl.Pulse() so that it is not recreated if unnecessary
    # Returns: true if successful, false if not
    if pulse_initial is None:
        pulse = pulsectl.Pulse()
    else:
        pulse = pulse_initial
    
    loop_id = pulse.module_load('module-loopback', 'source="{0}" sink="{1}" latency_msec={2}'
        .format(source_name, sink_name, latency_msec))
    
    
    if loop_id > 100000:
        print("Invalid loop id")
        return
    
      # Find the newly created sink-input
    loop_sink_input = None
    for si in pulse.sink_input_list():
        if si.owner_module == loop_id:
            print("Sink-input: %s" % si.index)
            loop_sink_input = si

    if loop_sink_input == None:
        print("Could not find newly created sink-input")
        return
   
  # Find the newly created source-output
    loop_source_output = None
    for so in pulse.source_output_list():
        if so.owner_module == loop_id:
            print("Source-output: %s" % so.index)
            loop_source_output = so

    if loop_source_output == None:
        print("Could not find newly created source-output")
        return