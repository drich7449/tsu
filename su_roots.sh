#!/system/bin/sh

suroots_fp="/sbin/.suroots"

mkdir "$suroots_fp"

# Handle LineageOS SU

sudo {
    args = "$@"
    su -c "$@"
}

mountbinder() {
    chmntdir="$1"
  #### mb - mount bindpoints and tmpfs
  echo "Mounting bindpoints";

  sudo mount -o bind /dev "$chmntdir/dev"
  sudo mount -t devpts -o rw,gid=5,mode=620 devpts "$chmntdir/dev/pts"
  sudo mount -t proc proc "$chmntdir/proc"
  sudo mount -t sysfs sys "$chmntdir/sys"
}

init_losu() {
    mkdir "$suroots_fp/losu"
    mkdir "$suroots_fp/losu/dev"
    mkdir "$suroots_fp/losu/proc"
    mkdir "$suroots_fp/losu/sys"

    mkdir "$suroots_fp/losu/system"
    mkdir "$suroots_fp/losu/etc"
    mountbinder "$suroots_fp/losu"

    mount -o bind "/system" "$suroots_fp/losu/system"
    mount -o bind "/etc" "$suroots_fp/losu/etc"
}



subcommand="$1"
super_su="$2"

sub_help {
    echo "Create a fake root to test su binaries."
}

sub_mount {
    init_losu
}

sub_umount {
    "$suroots_fp/losu"
}
case $subcommand in
    "" | "-h" | "--help")
        sub_help
        ;;
    *)
        shift
        sub_${subcommand} $@
        if [ $? = 127 ]; then
            echo "Error: '$subcommand' is not a known subcommand." >&2
            echo "       Run '$ProgName --help' for a list of known subcommands." >&2
            exit 1
        fi
        ;;
esac