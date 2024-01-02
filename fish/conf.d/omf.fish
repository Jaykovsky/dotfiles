# Path to Oh My Fish install.
set -q XDG_DATA_HOME
  and set -gx OMF_PATH "$XDG_DATA_HOME/omf"
  or set -gx OMF_PATH "$HOME/.local/share/omf"

# Load Oh My Fish configuration.
source $OMF_PATH/init.fish

set fish_greeting
set PATH /home/jay/.node_modules_global/bin $PATH
set PATH $PATH:$HOME/.config/composer/vendor/bin
set -e COLUMNS
set -e LINES
set --export ANDROID_HOME $HOME/Android/Sdk
