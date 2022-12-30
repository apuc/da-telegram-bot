#/bin/sh

cd /home/kirill/p/da-telegram-bot/
#venv/bin/python3.7 send_exchange.py
ARGS="venv/bin/python3.7 send_exchange.py"

while getopts t:m: flag
do
    case "${flag}" in
        t) type=${OPTARG};;
        m) mode=${OPTARG};;
    esac
done

if [ $type ]
then
  ARGS="$ARGS -t $type "
fi

if [ $mode ]
then
  ARGS="$ARGS -m $mode "
fi

echo "cmd: $ARGS"

eval $ARGS