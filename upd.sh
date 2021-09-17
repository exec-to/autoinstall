#!/bin/bash

ip_a="10.0.224."

ip_n=74

for srv in `seq 1662 1842`; do
  mysql -e "use aidb; update servers set dhcp_addr = '${ip_a}${ip_n}' where adman_id = ${srv};";
  echo ${srv}
  echo ${ip_n}
  ip_n=$((ip_n+1))
done;
