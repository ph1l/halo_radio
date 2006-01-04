#!/bin/sh
#

#
# this script installs daemontools.
#

VER=0.76

mkdir -p /package
chmod 1755 /package
cd /package || exit

wget http://cr.yp.to/daemontools/daemontools-${VER}.tar.gz

gunzip daemontools-${VER}.tar.gz
tar -xpf daemontools-${VER}.tar
rm daemontools-${VER}.tar
cd admin/daemontools-${VER}

package/install

mail djb-sysdeps@cr.yp.to < /package/admin/daemontools/compile/sysdeps

