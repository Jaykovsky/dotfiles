from typing import List
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import qtile, hook, extension
import os, subprocess, socket

mod = "mod4"
terminal = "alacritty"
WebBrowser = "google-chrome-stable"
AppLauncher = "rofi -show drun"

margin_size = 4

keys = [Key(key[0], key[1], *key[2:]) for key in [
    ([mod], "j", lazy.layout.down()),
    ([mod], "k", lazy.layout.up()),
    ([mod], "h", lazy.layout.left()),
    ([mod], "l", lazy.layout.right()),

    # Change window sizes (MonadTall)
    ([mod, "shift"], "l", lazy.layout.grow()),
    ([mod, "shift"], "h", lazy.layout.shrink()),

    # Toggle floating
    ([mod, "shift"], "f", lazy.window.toggle_floating()),

    # Move windows up or down in current stack
    ([mod, "shift"], "j", lazy.layout.shuffle_down()),
    ([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Toggle between different layouts as defined below
    ([mod], "Tab", lazy.next_layout()),
    ([mod, "shift"], "Tab", lazy.prev_layout()),

    # Kill window
    ([mod], "w", lazy.window.kill()),

    # Switch focus of monitors
    ([mod], "period", lazy.next_screen()),
    ([mod], "comma", lazy.prev_screen()),

    # Restart Qtile
    ([mod, "control"], "r", lazy.restart()),

    ([mod, "control"], "q", lazy.shutdown()),
    ([mod], "r", lazy.spawncmd()),

    # ------------ App Configs ------------

    # Menu
    ([mod], "m", lazy.spawn("rofi -show drun")),

    # Window Nav
    ([mod, "shift"], "m", lazy.spawn("rofi -show")),

    # Browser
    ([mod], "b", lazy.spawn("google-chrome-stable")),

    # File Explorer
    ([mod], "e", lazy.spawn('alacritty -t ranger -e sh -c "export -n LINES; export -n COLUMNS; ranger"')),

    # VS Code
    ([mod], "c", lazy.spawn("code")),

    # Terminal
    ([mod], "Return", lazy.spawn("alacritty")),

    # Spotify
    ([mod], "s", lazy.spawn("spotify")),

    # Screenshots
    ([mod], "y", lazy.spawn("flameshot gui")),
    ([mod, "shift"], "y", lazy.spawn("scrot -s")),

    # Lock Screen
    ([mod, "shift"], "p", lazy.spawn("slock")),


    # ------------ Hardware Configs ------------

    # Volume
    ([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    ([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    ([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Multimedia keys
    ([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    ([], "XF86AudioNext", lazy.spawn("playerctl next")),
    ([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    ([], "XF86AudioStop", lazy.spawn("playerctl stop")),

    # Brightness
    ([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    ([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
]]

groups = [Group(i) for i in [
    "  ", "  ", "  ", "  ", "  ",
]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

widget_defaults = dict(
    font='Ubuntu',
    fontsize=13,
    padding=3,
)

extenstion_defaults = widget_defaults.copy()

colors = [["#282c34", "#282c34"], # panel background
          ["#3d3f4b", "#434758"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#ff5555", "#ff5555"], # border line color for current tab
          ["#74438f", "#74438f"], # border line color for 'other tabs' and color for 'odd widgets'
          ["#4f76c7", "#4f76c7"], # color for the 'even widgets'
          ["#e1acff", "#e1acff"], # window name
          ["#ecbbfb", "#ecbbfb"], # background for inactive screens
          ["#000000", "#000000"]]

layout_conf = {
    'border_focus': colors[4],
    'border_width': 3,
    'margin': 10
}

layouts = [
    layout.Max(),
    layout.MonadTall(**layout_conf),
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    foreground=colors[2],
                    background=colors[8],
                ),
                widget.GroupBox(
                    font = "Ubuntu Nerd Font",
                    fontsize = 22,
                    margin_y = 3, 
                    margin_x = 0,
                    padding_y = 0, 
                    padding_x = 0, 
                    borderwidth = 1,
                    active = colors[2],
                    inactive = colors[1],
                    rounded = False,
                    highlight_color = colors[1],
                    highlight_method = "border",
                    this_current_screen_border = colors[6],
                    this_screen_border = colors [4],
                    other_current_screen_border = colors[6],
                    other_screen_border = colors[4],
                    foreground = colors[2],
                    background = colors[8]
                ),
                widget.Prompt(
                    prompt = prompt,
                    padding = 10,
                    foreground = colors[3],
                    background = colors[1]
                ),
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    foreground=colors[2],
                    background=colors[8],
                ),
                widget.WindowName(
                    foreground = colors[6],
                    background = colors[8],
                    fontsize = 0

                ),
                widget.Systray(
                    background = colors[8],
                    padding = 5
                ),
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    size_percent=60,
                    foreground=colors[2],
                    background=colors[8],
                ),
                widget.PulseVolume(
                    foreground = colors[3],
                    background = colors[8],
                    font = "scientifica",
                    fontsize = 14,
                    #get_volume_command = "pactl get-sink-volume @DEFAULT_SINK@",
                ),
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    size_percent=60,
                    foreground=colors[2],
                    background=colors[8],
                ),
                widget.CheckUpdates(
                    foreground = colors[5],
                    background = colors[8],
                    padding = 0,
                    colour_have_updates=colors[5],
                    colour_no_updates=colors[5],
                    no_update_string='0',
                    initial_text='0',
                    display_format='{updates}',
                    update_interval=1800,
                    custom_command='checkupdates',
                    font = "scientifica",
                    fontsize = 14,
                ),
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    size_percent=60,
                    foreground=colors[2],
                    background=colors[8],
                ),
                widget.Battery(
                    foreground = colors[6],
                    background = colors[8],
                    padding = 0,
                    charge_char='!', 
                    discharge_char='-', 
                    format='{percent:2.0%}',
                    font = "scientifica",
                    fontsize = 14,
                ),
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    size_percent=60,
                    foreground=colors[2],
                    background=colors[8],
                ),
                widget.ThermalSensor(
                    foreground = colors[6],
                    background = colors[8],
                    padding = 0,
                    tag_sensor='Package id 0', 
                    update_interval=10, 
                    threshold=70, max_chars=8,
                    font = "scientifica",
                    fontsize = 14,
                ),
                widget.Sep(
                    padding=6,
                    linewidth=0,
                    size_percent=60,
                    foreground=colors[2],
                    background=colors[8],
                ),
                widget.Clock(
                    format='%H:%M',
                    foreground = colors[3],
                    font = "scientifica",
                    fontsize = 14,
                ),
            ],
            24,
            opacity=0.75, #0.75
            background=colors[8],
            margin = [0, 0, 0, 0],
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

droups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='ssh-askpass'),
    Match(title='branchdialog'),
    Match(title='pinentry'),
])

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

wmname = "qtile"

@hook.subscribe.startup
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])
