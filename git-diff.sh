#!/bin/bash
#script to write git status to logs
cd /root/bsides-austin-2015/ 
date >> /var/log/git-diff.log 
echo '-----------------' >> /var/log/git-diff.log
git status >> /var/log/git-diff.log
