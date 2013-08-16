from ceph_deploy.util.wrappers import check_call
from ceph_deploy.hosts import common


def create(distro, logger, args, monitor_keyring):
    hostname = distro.sudo_conn.modules.socket.gethostname().split('.')[0]
    common.mon_create(distro, logger, args, monitor_keyring, hostname)
    check_call(
        distro.sudo_conn,
        logger,
        [
            '/usr/lib/ceph/ceph_init.sh',
            '-c',
            '/etc/ceph/{cluster}.conf'.format(cluster=args.cluster),
            'start',
            'mon.{hostname}'.format(hostname=hostname)
        ],
        patch=False
    )
