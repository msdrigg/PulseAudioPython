import json, os, sys
import pulsectl

FALLBACK_NULL_SINK_NAME = "FALLBACK_NULL_DEVICE_TEMP_2049"
DEFAULT_DEVICES = {
    "bluetooth_speakers": "bluez...",
    "external_speakers": "alas.generic_usb...",
    "hdmi": "nvidia_hdmi_driver...",
    "sport": "weird_sport_bluetooth...",
}

def main():
    # Combines speakers together, remapping bluetooth, sets this as default
    with open(os.path.join(os.getcwd(), "sources.json")) as f:
        devices = json.load(f)
    
    pulse = pulsectl.Pulse()
    
    remapped_properties = {
        "sink_properties": "device.description=RemappedLogiSpeakers",
        "sink_name": "RemappedLogiSpeakers",
    }

    bluetooth_channel_map = {
        "front-left": "front-right",
        "front-right": "front-left",
    }
    
    combined_properties = {
        "sink_properties": "device.description=CombinedSpeakers",
        "sink_name": "CombinedSpeakers",
    }

    device_names = [value["name"] for value in devices.values() if value.get("suspended", "no") != "yes"]
    desired_devices = [sink for sink in pulse.sink_list() if sink.name in device_names]
    
    bluetooth_speakers = devices["bluetooth_desk"]
    for device in desired_devices:
        if device.name == bluetooth_speakers["name"]:
            fallback_sink = None
            for device in desired_devices:
                if device.name != bluetooth_speakers["name"]:
                    fallback_sink = device
            if fallback_sink is None:
                fallback_sink = create_and_return_null(pulse_initial=pulse)
            pulse.default_set(fallback_sink)
            remapped_bluetooth_module_id = remap(device, bluetooth_channel_map,
                                                 pulse_initial=pulse,
                                                 **remapped_properties)
            success = False
            desired_devices.remove(device)
            for item in pulse.sink_list():
                if item.owner_module == remapped_bluetooth_module_id:
                    desired_devices.append(item)
                    success = True
                    break
            if not success:
                print("Failure finding remapped sink")
            
            if fallback_sink.name == FALLBACK_NULL_SINK_NAME:
                pulse.module_unload(fallback_sink.index)
            break
    
    combined_audio = combine(desired_devices, pulse_initial=pulse,
                             adjust_time=1, **combined_properties)
    
    for sink in pulse.sink_list():
        if sink.owner_module == combined_audio:
            print("SETTING DEFAULT")
            pulse.default_set(sink)


def create_and_return_null(pulse_initial=None):
    # Creates and returns a null sink with name "FALLBACK_NULL_SINK_NAME"
    print("CREATING NULL")
    if pulse_initial is None:
        pulse = pulsectl.Pulse()
    else:
        pulse = pulse_initial
    
    null_id = pulse.load_module('module-null-sink', f'sink_name="{FALLBACK_NULL_SINK_NAME}"')
    
    if null_id > 100000:
        print("Invalid remap id " + str(remap_id))
        return
    
    for device in pulse.sink_list():
        if device.owner_module == null_id:
            return device

    print("Null sink not found")


def remap(source, channel_map, pulse_initial=None, **kwargs):
    # source_json contains name identifiers for sound source 
    # kwargs: passed to load-module
    # Returns: remapped_module_id if successful, None if not successful
    print("REMAPPING")
    if pulse_initial is None:
        pulse = pulsectl.Pulse()
    else:
        pulse = pulse_initial
    
    output_channels = ",".join(channel_map.values())
    input_channels = ",".join(channel_map.keys())
    
    kwarg_string = " ".join(list(map(lambda kvp: f'{kvp[0]}="{kvp[1]}"', kwargs.items())))
    if kwarg_string != "":
        kwarg_string = " " + kwarg_string
    #print(f'master="{source.name}" channels={str(len(channel_map))} ' + 
    #    f'channel_map="{output_channels}" master_channel_map="{input_channels}" ' +
    #    'remix="no"' + kwarg_string
    #)

    remap_id = pulse.module_load('module-remap-sink', 
        f'master="{source.name}" channels={str(len(channel_map))} ' + 
        f'channel_map="{output_channels}" master_channel_map="{input_channels}" ' +
        'remix="no"' + kwarg_string
    )
    
    
    if remap_id > 100000:
        print("Invalid remap id " + str(remap_id))
        return
    
    return remap_id


def combine(sources, pulse_initial=None, adjust_time=10, **kwargs):
    # sink_name contains name identifiers for sound sink 
    # sources contain dict objects with information about sources to be combined
    # kwargs: passed to load-module
    # Returns: remapped_module_id if successful, None if not successful
    print("COMBINING")
    if pulse_initial is None:
        pulse = pulsectl.Pulse()
    else:
        pulse = pulse_initial
    
    source_names = ",".join(list(map(lambda a: a.name, sources)))
    channel_map_set = set()
    for source in sources:
        channel_map_set.update(source.channel_list)
    channel_map = ",".join(sorted(channel_map_set))
    channel_count = len(channel_map_set)

    kwarg_string = " ".join(list(map(lambda kvp: f'{kvp[0]}="{kvp[1]}"', kwargs.items())))
    if kwarg_string != "":
        kwarg_string = " " + kwarg_string
    #print(f'slaves="{source_names}" channels="{channel_count}" ' + 
    #    f'channel_map="{channel_map}" adjust_time="{adjust_time}"' + 
    #    kwarg_string
    #)

    combine_id = pulse.module_load('module-combine-sink', 
        f'slaves="{source_names}" channels="{channel_count}" ' + 
        f'channel_map="{channel_map}" adjust_time="{adjust_time}"' + 
        kwarg_string
    )
    if combine_id > 100000:
        print("Invalid combine id " + str(combine_id))
        return
    
    return combine_id


if __name__ == "__main__":
    main()
    if sys.argv[-1] == "-listen":
        #TODO: Add event listener that calls main() everytime list of sinks changes
        pass
