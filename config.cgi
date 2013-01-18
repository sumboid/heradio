#!/bin/bash

#######################################
#                                     #
#                  ls                 #
#                                     #
#######################################

ENABLE_LS=1
DISABLE_LS_MESSAGE="<center><h1>SERVICE IS NOT AVAILABLE</h1> temporarily :3</center>"

ENABLE_ADD=1
DISABLE_ADD_MESSAGE="Добавление треков отключено в данное время"

LS_WAIT_TIME=100
LS_WIPE_FILE="../wipe/stopwipe_ls"

#######################################
#                                     #
#               playlist              #
#                                     #
#######################################

ENABLE_PLAYLIST=1
DISABLE_PLAYLIST_MESSAGE="<center><h1>SERVICE IS NOT AVAILABLE</h1> terporarily :3</center>"

#######################################
#                                     #
#               request               #
#                                     #
#######################################

ENABLE_REQUEST=1
DISABLE_REQUEST_MESSAGE="<center><h1>SERVICE IS NOT AVAILABLE</h1> terporarily :3</center>"
REQUEST_WAIT_TIME=30
REQUEST_WIPE_FILE="../wipe/stopwipe_request"
XMPP_CONF="xmpp.conf"

#######################################
#                                     #
#                 play                #
#                                     #
#######################################
ENABLE_PLAY=1
DISABLE_PLAY_MESSAGE="<h1>SERVICE IS NOT AVAILABLE</h1> temporarily :3"

#######################################
#                                     #
#                upload               #
#                                     #
#######################################

ENABLE_UPLOAD=1
UPLOAD_WIPE_FILE="../wipe/stopwipe_upload"
UPLOAD_WAIT_TIME=60
UPLOAD_DIR="/mnt/yoba/new/music/anon_upload"
UPLOAD_PATH="anon_upload"
DISABLE_UPLOAD_MESSAGE="<center><h1>SERVICE IS NOT AVAILABLE</h1> terporarily :3</center>"

#######################################
#                                     #
#                  ALL                #
#                                     #
#######################################

MPD_HOST="192.168.0.9"
MPD_PASS="nyasha"

# На будущее
# Банлист
# Уровни доступа на добавление
# загрузка и прочие фичи

# Баги:
# Говно с добавлением урлов
# Говно с регекспом 
