#!/bin/bash

. ansi_color.sh

initializeANSI
echo -e "${yellowf}This is a phrase in yellow${redb} and red${reset}"
echo -e "${boldon}This is bold${ulon} this is italics${reset}"
echo -e "bye-bye${italicson}This is italics${italicsoff} and this is not${ulon}This is ul${uloff} and this is not 42Chapter 1${invon}This is inv${invoff} and this is not
${yellowf}${redb}Warning I ${yellowb}${redf}Warning II${reset}"
