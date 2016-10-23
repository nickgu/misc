#! /bin/sh -x
#  this script automatically setup the configurations.

# backup old config.
backup=~/.config_backup
mkdir $backup

mv ~/.vimrc ~/.bash_profile ~/.vim ~/.tmux.conf $backup

cp vimrc ~/.vimrc
cp bash_profile ~/.bash_profile
cp tmux.conf ~/.tmux.conf

tar zxvf vim.tar.gz
cp -r vim ~/.vim





