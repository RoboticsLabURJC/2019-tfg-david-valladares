#!/bin/bash


# declare -a arr=("alpha01.aulas.gsyc.urjc.es"
#                 "alpha02.aulas.gsyc.urjc.es"
#                 "alpha03.aulas.gsyc.urjc.es"
#                 "alpha04.aulas.gsyc.urjc.es"
#                 "alpha05.aulas.gsyc.urjc.es"
#                 "beta01.aulas.gsyc.urjc.es"
#                 "beta02.aulas.gsyc.urjc.es"
#                 "beta03.aulas.gsyc.urjc.es"
#                 "beta04.aulas.gsyc.urjc.es"
#                 "beta05.aulas.gsyc.urjc.es"
#                 "gamma01.aulas.gsyc.urjc.es"
#                 "gamma02.aulas.gsyc.urjc.es"
#                 "gamma03.aulas.gsyc.urjc.es"
#                 "gamma04.aulas.gsyc.urjc.es"
#                 "gamma05.aulas.gsyc.urjc.es"
#                 "delta01.aulas.gsyc.urjc.es"
#                 "delta02.aulas.gsyc.urjc.es"
#                 "delta03.aulas.gsyc.urjc.es"
#                 "delta04.aulas.gsyc.urjc.es"
#                 "delta05.aulas.gsyc.urjc.es"
#                 "zeta01.aulas.gsyc.urjc.es"
#                 "zeta02.aulas.gsyc.urjc.es"
#                 "zeta03.aulas.gsyc.urjc.es"
#                 "zeta04.aulas.gsyc.urjc.es"
#                 "zeta05.aulas.gsyc.urjc.es")

declare -a arr=("epsilon01.aulas.gsyc.urjc.es"
                "epsilon02.aulas.gsyc.urjc.es"
                "epsilon03.aulas.gsyc.urjc.es"
                "epsilon04.aulas.gsyc.urjc.es"
                "epsilon05.aulas.gsyc.urjc.es"
                "epsilon06.aulas.gsyc.urjc.es"
                "epsilon07.aulas.gsyc.urjc.es"
                "epsilon08.aulas.gsyc.urjc.es"
                "epsilon09.aulas.gsyc.urjc.es"
                "epsilon10.aulas.gsyc.urjc.es"
                "epsilon11.aulas.gsyc.urjc.es"
                "epsilon12.aulas.gsyc.urjc.es"
                "epsilon13.aulas.gsyc.urjc.es"
                "epsilon14.aulas.gsyc.urjc.es"
                "epsilon15.aulas.gsyc.urjc.es"
                "epsilon16.aulas.gsyc.urjc.es"
                "epsilon17.aulas.gsyc.urjc.es"
                "epsilon118.aulas.gsyc.urjc.es")


for i in "${arr[@]}"
do
   echo "$i"
   getent hosts $i | awk '{ print $1 }' >> 'ips_fromURJC.txt'
   getent hosts $i >> 'host_fromURJC.txt'
   # or do whatever with individual element of the array
done
