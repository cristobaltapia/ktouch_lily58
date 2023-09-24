# KTouch layout and courses for the Lily58 keyboard

This repository contains a KTouch keyboard layout and courses for the Lily58.
The courses are generated using [ktgen](https://github.com/BarbieCue/ktgen) and [ktouch-lesson-generator](https://github.com/simgunz/ktouch-lesson-generator).

![Lily58 keyboard with noted layout](lilly58_noted.png)

## Generate lessons for KTouch

To generate the lessons use the following command

```bash
make all
```

## Generate layout for KTouch

Different layouts for the Lily58 can be created with the provided python script `layout/generate_layout.py`.
Use it as follows:

```bash
python generate_layout.py --keyboard-config=lily58_config.json --layout=noted_layout.json --name=noted
```

The file `lily58_config.json` defines general properties for the keyboard, like position of keys and fingers associated to each key.
The file `noted_layout.json` defines the layout to be generated with the different layers defined within a json array.

The noted layout can be generated with

```bash
make layout
```

## Author

- Cristóbal Tapia Camú

## Thanks

- Jan Schreiber ([German dictionary](https://sourceforge.net/projects/germandict/))
- Dario Götz ([Noted layout](https://github.com/dariogoetz/noted-layout))
