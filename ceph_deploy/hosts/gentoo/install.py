from ceph_deploy.util.wrappers import check_call
from ceph_deploy.util.context import remote
from ceph_deploy.hosts import common


def install(distro, logger, version_kind, version):
    # TODO handle version_kind/version via keywords here
    codename = distro.codename
    machine = distro.sudo_conn.modules.platform.machine()

    with remote(distro.sudo_conn, logger, write_sources_list) as remote_func:
        remote_func(url, codename)

    # TODO use layman to add the overlay
    check_call(
        distro.sudo_conn,
        logger,
        ['emerge', '-q', 'sync'],
        )

    # TODO this does not downgrade -- should it?
    check_call(
        distro.sudo_conn,
        logger,
        [
            'emerge',
            '-q',
            '--no-replace',
            'ceph',
            # ceph only recommends gdisk, make sure we actually have
            # it; only really needed for osds, but minimal collateral
            'gdisk',
            ],
        )

    # Check the ceph version
    common.ceph_version(distro.sudo_conn, logger)
