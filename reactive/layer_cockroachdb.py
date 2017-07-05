# !/usr/bin/env python3
# Copyright (C) 2017  Qrama
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable=c0111,c0301,c0325,c0103,r0913,r0902,e0401,C0302, R0914
import os
import subprocess as sp
import shutil
from charms.reactive import when, when_not, set_state, remove_state
from charmhelpers.core.hookenv import status_set, config, unit_private_ip, open_port
from charmhelpers.core.host import service_restart, service_start
from charmhelpers.core.templating import render

COCKROACH_PATH = '/opt/cockroachdb'

@when_not('cockroachdb.installed')
def install():
    if not os.path.isdir(COCKROACH_PATH):
        os.mkdir(COCKROACH_PATH)
    sp.check_call(['wget', '--output-document={}/cockroach-v1.0.2.linux-amd64.tgz'.format(COCKROACH_PATH), 'https://binaries.cockroachdb.com/cockroach-v1.0.2.linux-amd64.tgz'])
    sp.check_call(['tar', 'xfz', '{}/cockroach-v1.0.2.linux-amd64.tgz'.format(COCKROACH_PATH), '-C', COCKROACH_PATH])
    sp.check_call(['cp', '-i', '{}/cockroach-v1.0.2.linux-amd64/cockroach'.format(COCKROACH_PATH), '/usr/local/bin'])
    shutil.copyfile('files/cockroachdb.service', '/etc/systemd/system/cockroachdb.service')
    service_start('cockroachdb')
    open_port(8080)
    open_port(26257)
    status_set('active', 'Ready')
    set_state('cockroachdb.installed')
