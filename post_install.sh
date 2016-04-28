#!/bin/sh
DIR=/var/tmp

if [ -d "$DIR" ]; then
    cp /usr/bin/snmpext /var/tmp/snmpext
#     cat > $DIR/snmpext <<EOF
# #!/usr/bin/python -u
# from eos_snmpext.entry import main
# if __name__ == "__main__":
#     main()
# EOF
#     chmod +x $DIR/snmpext
fi
