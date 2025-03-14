
# Home Assistant SIA Transmitter WIP

A custom integration that enables Home Assistant to be used as an SIA transmitter.

## Installation

### Installation using [HACS](https://www.hacs.xyz/)

**Installation via HACS is not supported yet**

### Manual installation

- Install the ```Terminal & SSH``` Home Assistant addon
- Start the add-on and enable ```Show in sidebar```
- Click on the Terminal icon in the sidebar
- Change folder to config/custom_components using:
```bash
cd ./config/custom_components
```
- If the ```custom_components``` folder does not exist, create it using ```mkdir```
- Clone the repository into the ```custom_components``` folder using:
```bash
git clone https://github.com/icilundi/ha-sia-transmitter.git
```
## TODO
- [ ] Properly handle sequence number
- [ ] Represent hosts status as binary sensors
- [ ] Add extended data field
- [ ] String keys
- [x] Let the user decide to send the timestamp in supervision message in config flow
- [x] ~~Let the user decide to send supervision message~~


## Contributing
This integration is currently in early development and may require further improvements.Due to limited documentation and references for the Home Assistant API, development was guided by the source code of the official HA SIA integration.

Contributions are always welcome!
