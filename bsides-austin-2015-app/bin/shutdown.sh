#!/bin/sh

# A POSIX variable
OPTIND=1         # Reset in case getopts has been used previously in the shell.
KEY_PATH=/home/splunk-admin/id_rsa.pub
USER=splunk-admin

# functions 
function show_help {
echo "block a host:"
echo "shutdown.sh [-e|--endpoint]=10.122.10.44\n"
echo "for help:"
echo "shutdown.sh [-h|--help]\n"
}

if [ $# -lt 1 ]; then
        show_help
        exit 1
fi

for i in "$@"
do
case $i in
    -e=*|--endpoint=*)
    ENDPOINT="${i#*=}"
    shift
    ;;
    -h*|--help*|\?)
    show_help
    shift
    ;;
    *)
    show_help        # unknown option
    ;;
esac
done
echo $KEY_PATH
ssh $USER\@$ENDPOINT \-i $KEY_PATH 'sudo shutdown -h 0 now' 

#shift $((OPTIND-1))

#[ "$1" = "--" ] && shift


