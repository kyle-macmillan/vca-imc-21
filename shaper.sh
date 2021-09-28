#!/bin/bash
#

CMD=$1

DNLD_RATE=$2
UPLD_RATE=$3
LATENCY=$4
LOSS=$5
IFACE=$6

echo $CMD,$DNLD_RATE,$UPLD_RATE,$LATENCY,$LOSS


# Name of the traffic control command.
TC=tc
DNLD=${DNLD_RATE}mbit          # DOWNLOAD Limit
UPLD=${UPLD_RATE}mbit          # UPLOAD Limit

start() {

if [ ! "$DNLD" ]
then
  echo "DNLD rate is empty!"
  exit
fi

  modprobe ifb numifbs=1
  ip link set dev ifb0 up
  $TC qdisc add dev ifb0 root handle 1: htb default 10
  $TC filter add dev $IFACE parent ffff: protocol ip u32 match u32 0 0 action mirred egress redirect dev ifb0
  $TC filter add dev $IFACE parent ffff: protocol ipv6 u32 match u32 0 0 action mirred egress redirect dev ifb0
  
  $TC qdisc add dev $IFACE handle ffff: ingress
  $TC class add dev ifb0 parent 1: classid 1:1 htb rate $DNLD
  $TC class add dev ifb0 parent 1:1 classid 1:10 htb rate $DNLD
  $TC qdisc add dev ifb0 parent 1:10 netem delay ${LATENCY}ms loss ${LOSS}%

  # UPLINK settings
  $TC qdisc add dev $IFACE root handle 1: htb default 10
  $TC class add dev $IFACE parent 1: classid 1:1 htb rate $UPLD
  $TC class add dev $IFACE parent 1:1 classid 1:10 htb rate $UPLD 
  #$TC qdisc add dev $IFACE parent 1:10 netem delay ${LATENCY}ms loss ${LOSS}% 



}

stop() {

  # Stop the bandwidth shaping.
  $TC qdisc del dev ifb0 root
  $TC qdisc del dev $IFACE root

}

stop_all() {

    $TC qdisc del dev $IFACE root
    
}

update() {

echo $DNLD
    $TC class change dev ifb0 parent 1:1 classid 1:10 htb rate $DNLD
    $TC qdisc replace dev ifb0 parent 1:10 netem delay ${LATENCY}ms loss ${LOSS}%
    $TC class change dev $IFACE parent 1:1 classid 1:10 htb rate $UPLD
    $TC qdisc replace dev $IFACE parent 1:10 netem delay ${LATENCY}ms loss ${LOSS}%
}

show() {

    $TC -s qdisc ls dev $IFACE
    $TC class show dev $IFACE
    $TC filter show dev $IFACE

}

case "$CMD" in

  start)

    echo -n "Starting bandwidth shaping: "
    start
    echo "done"
    ;;

  stop)

    echo -n "Stopping bandwidth shaping: "
    stop
    echo "done"
    ;;

  update)

    echo -n "Updating bandwidth shaping at $DNLD: "
    update
    echo "done"
    ;;

  show)

    echo "Bandwidth shaping status for $IFACE:"
    show
    echo ""
    ;;

  *)

    pwd=$(pwd)
    echo "shaper.sh <start|show|update|stop> <dnld> <upld> <latency> <loss>"
    ;;

esac

exit 0

