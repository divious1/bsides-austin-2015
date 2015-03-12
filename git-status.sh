#!/bin/bash
#script to write git status to logs
cd /root/bsides-austin-2015/ 
date >> /var/log/git-status.log 
echo '-----------------' >> /var/log/git-status.log
git status >> /var/log/git-status.log
