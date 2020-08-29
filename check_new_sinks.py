import pulsectl
import os, json
from combine_sink_low_latency import activate, deactivate
from threading import Thread
from time import sleep

already_running = False

def reactivate_after_delay():
    sleep(5)
    pulse = pulsectl.Pulse()
    event_sink = None
    print("Event index: " + str(event.index))
    for sink in reversed(pulse.sink_list()):
        print("Sink index: " + str(sink.index))
        if sink.index == event.index:
            event_sink = sink
            break
    
    if event_sink is None:
        target_sinks = None
    else:
        with open(os.path.join(os.getcwd(), "sources.json")) as f:
            target_sinks = json.load(f)
            target_sink_names = [value["name"] for value in target_sinks.values() if value.get("suspended", "no") != "yes"]

    print("Printing event sink: ")
    print(event_sink)
    if event_sink is None or event_sink.name in target_sink_names:
        deactivate()
        activate()


def activate_if_change_necessary(event):
    event_type = event.t._value 
    if event_type == "new" or event_type == "remove":
        already_running = True
        activate_after_delay()
        # thread = Thread(target=activate_after_delay)
        # thread.start()


def main():
    # Check for pulse events for 4 minutes
    deactivate()
    activate()
    
    with pulsectl.Pulse('event-printer') as pulse:
        pulse.event_mask_set('sink')
        pulse.event_callback_set(activate_if_change_necessary)
        pulse.event_listen(timeout=60*4)


if __name__ == "__main__":
    main()
