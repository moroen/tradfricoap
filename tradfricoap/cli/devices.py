from tradfricoap.device import get_devices, get_device
from tradfricoap.errors import HandshakeError
from tradfricoap import ApiNotFoundError

def set_state(id, state):
    device = get_device(id)
    if state not in [0,1]:
        state = 1
    device.State = state


def list_devices(groups=False):
    try:
        devices = get_devices(groups)
    except HandshakeError:
        print("Connection timed out")
        exit()

    except ApiNotFoundError as e:
        print(e.message)
        exit()

    if devices is None:
        print("Unable to get list of devices")
    else:
        ikea_devices = []
        plugs = []
        blinds = []
        groups = []
        batteries = []
        others = []

        devices = sorted(devices.items())

        for key, dev in devices:
            if dev.Type == "Light":
                ikea_devices.append(dev.Description)
            elif dev.Type == "Plug":
                plugs.append(dev.Description)
            elif dev.Type == "Blind":
                blinds.append(dev.Description)
            elif dev.Type == "Group":
                groups.append(dev.Description)
            else:
                others.append(dev.Description)

            if dev.Battery_level is not None:
                batteries.append(
                    "{}: {} - {}".format(dev.DeviceID, dev.Name, dev.Battery_level)
                )

        if len(ikea_devices):
            print("Lights:")
            print("\n".join(ikea_devices))

        if len(plugs):
            plugs.sort()
            print("\nPlugs:")
            print("\n".join(plugs))

        if len(blinds):
            blinds.sort()
            print("\nBlinds:")
            print("\n".join(blinds))

        if len(groups):
            groups.sort()
            print("\nGroups:")
            print("\n".join(groups))

        if len(others):
            others.sort()
            print("\nOthers:")
            print("\n".join(others))

        if len(batteries):
            print("\nBatteries:")
            print("\n".join(batteries))