#!/bin/bash


##############################################################
# Testé sur 
#     - Valide pour 
#     - Ne fonctionne pas pour
##############################################################

##############################################################
# Suivi des modifications :
#     - Création du script (otd - 02/08/2012)
#     - Modification du répertoire d'archive (otd - 03/09/2012)
#     - Commentaire pour les filtres d'exeption (trt - 15/05/2013)
#     - Fonction de vérificatin (trt - 30/05/2013)
##############################################################

# CONFIGURATION
TMPDIR="/tmp/extract_linux/"
OUTFILE="/tmp/`hostname`.config.$$.tar.bz2"
NETTOYAGE=1
HOSTNAME=`hostname`
VERIFIE=1
VERSION="0.1"

OUT_FILE_LST="find.txt netstat.txt pkg_list.txt ps.txt ps-format.txt mount.txt uname.txt kernel_config.txt passwd.txt group.txt network.txt routes.txt iptables.txt kernel_modules.txt lspci.txt cpuinfo.txt version_script.txt"

erreur() {
    echo "[!] $1" > /dev/stderr
    exit 42
}

nettoyage() {
    if [ $NETTOYAGE -eq 1 ]; then
	echo "[!] nettoyage répertoire de sortie ($OUTDIR)" > /dev/stderr
	rm -rf $TMPDIR
    fi
}

verification () {
    THIS=$(pwd); cd $OUTDIR;

    for file in $OUT_FILE_LST; do
        if [ ! -f $file ]; then
            echo "[!] ATTENTION : le fichier $file manque.";
        elif which md5sum > /dev/null 2>&1; then
            md5sum $file >> $OUTDIR/check.txt;
        fi
    done
    
    cd $THIS;
}

# Got from http://fr.w3support.net/index.php?db=sf&id=3331
get_distribution_type()
{
    local dtype
    # Assume unknown
    dtype="unknown"

    # First test against Fedora / RHEL / CentOS / generic Redhat derivative
    if [ -r /etc/rc.d/init.d/functions ]; then
        . /etc/rc.d/init.d/functions
        [ zz`type -t passed 2>/dev/null` == "zzfunction" ] && dtype="redhat"

    # Then test against SUSE (must be after Redhat,
    # I've seen rc.status on Ubuntu I think? TODO: Recheck that)
    elif [ -r /etc/rc.status ]; then
        . /etc/rc.status
        [ zz`type -t rc_reset 2>/dev/null` == "zzfunction" ] && dtype="suse"

    # Then test against Debian, Ubuntu and friends
    elif [ -r /lib/lsb/init-functions ]; then
        . /lib/lsb/init-functions
        [ zz`type -t log_begin_msg 2>/dev/null` == "zzfunction" ] && dtype="debian"

    # Then test against Gentoo
    elif [ -r /etc/init.d/functions.sh ]; then
        . /etc/init.d/functions.sh
        [ zz`type -t ebegin 2>/dev/null` == "zzfunction" ] && dtype="gentoo"

    # For Slackware we currently just test if /etc/slackware-version exists
    # and isn't empty (TODO: Find a better way :)
    elif [ -s /etc/slackware-version ]; then
        dtype="slackware"
    fi

    DISTRO=$dtype
}

echo "[+] vérification des droits"
if [ ! "`id -u`" -eq 0 ]; then
    erreur "Le script doit être exécuté avec les droits « root »"
fi

echo "[+] création du repertoire de destination"
MKTEMP_BIN=`which mktemp`
if [ -n $MKTEMP_BIN -a -x $MKTEMP_BIN ]; then
    TMPDIR="`mktemp -d`"
    OUTDIR="$TMPDIR/$HOSTNAME"
    mkdir $OUTDIR
elif [ ! -d $OUTDIR ]; then
    mkdir $OUTDIR
else
    erreur "Impossible de créer le répertoire de sortie"
fi
echo "[-] répertoire de sortie : $OUTDIR"

echo "[+] détection de la distribution"
get_distribution_type
echo "[-] distribution détectée : $DISTRO"

# Nettoyage uniquement après la création du répertoire de sortie
trap "nettoyage" 0

echo "[+] Exécution de la version 0.1 du script d'extraction"
echo $VERSION > $OUTDIR/version_script.txt

echo "[+] liste des fichiers et des droits associés"
find / -ls > $OUTDIR/find.txt
### Liste des fichiers avec exclusion de répertoire (Linux)
#find / -type d \( -wholename "/directoryA" -o -wholename "/DirectoryB" \) -prune -o -ls > $OUTDIR/find.txt

echo "[+] liste des processus en écoute"
netstat -a -n -p > $OUTDIR/netstat.txt

echo "[+] liste des sockets en écoute"
ss -ltp > $OUTDIR/ss-listen.txt

echo "[+] liste de connexions établies"
ss -ptn > $OUTDIR/ss-established.txt

echo "[+] liste des processus actifs"
ps faux > $OUTDIR/ps.txt

echo "[+] liste formatées des processus"
ps -axeo pid,ppid,user,args > $OUTDIR/ps-format.txt

echo "[+] liste des paquets installés"
if [ x$DISTRO = "xdebian" ]; then
    dpkg -l > $OUTDIR/pkg_list.txt
elif [ x$DISTRO = "xredhat" ]; then
    rpm -qa --last > $OUTDIR/pkg_list.txt
else
    echo "[!] attention, distribution non reconnue"
fi

echo "[+] contenu du répertoire /etc/"
tar cjf $OUTDIR/etc.tar.bz2 -p --atime-preserve /etc
### Ignore certains fichiers sensibles (linux)
#tar cjf $OUTDIR/etc.tar.bz2 -p --atime-preserve --wildcards --exclude "/etc/passwd*" --exclude "/etc/shadow*" --exclude "/etc/group*" --exclude "/etc/krb5.conf" --exclude "/etc/sudoers*" --exclude "/etc/publickeys*" --exclude "/etc/pki*" /etc

echo "[+] liste des points de montage"
mount > $OUTDIR/mount.txt

echo "[+] version du noyau en cours de fonctionnement"
uname -a > $OUTDIR/uname.txt

echo "[+] configuration du noyau"
cp /boot/config-`uname -r` $OUTDIR/kernel_config.txt

echo "[+] liste des utilisateurs et des groupes"
getent passwd > $OUTDIR/passwd.txt
getent group > $OUTDIR/group.txt

echo "[+] configuration réseau"
ifconfig -a > $OUTDIR/network.txt

echo "[+] table de routage"
route -n -e > $OUTDIR/routes.txt

echo "[+] règles du pare-feu"
iptables-save > $OUTDIR/iptables.txt

echo "[+] liste des modules noyau"
lsmod > $OUTDIR/kernel_modules.txt

echo "[+] configuration matérielle"
lspci -vvv > $OUTDIR/lspci.txt
cat /proc/cpuinfo > $OUTDIR/cpuinfo.txt

echo "[+] liste des tâches plannifiées des utilisateurs, répertoire"
[ -d /var/spool/cron ] && tar cjf $OUTDIR/var_spool_cron.tar.bz2 -p --atime-preserve /var/spool/cron ;
[ -d /var/spool/anacron ] && tar cjf $OUTDIR/var_spool_anacron.tar.bz2  -p --atime-preserve /var/spool/anacron ;

#TODO Vérifier que ça fonctionne sur chaque distrib
echo "[+] vérification de la présence des fichiers"
[ "$VERIFIE" -eq 1 ] && verification;

echo "[+] création de l'archive finale"
cd $TMPDIR

echo "[+] compression..."
tar cjf $OUTFILE $HOSTNAME

echo "[+] Ok ! Fichier de sortie : $OUTFILE"
