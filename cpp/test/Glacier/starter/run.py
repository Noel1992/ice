#!/usr/bin/env python
# **********************************************************************
#
# Copyright (c) 2001
# MutableRealms, Inc.
# Huntsville, AL, USA
#
# All Rights Reserved
#
# **********************************************************************

import os, sys

for toplevel in [".", "..", "../..", "../../..", "../../../.."]:
    toplevel = os.path.normpath(toplevel)
    if os.path.exists(os.path.join(toplevel, "config", "TestUtil.py")):
        break
else:
    raise "can't find toplevel directory!"

sys.path.append(os.path.join(toplevel, "config"))
import TestUtil

starter = os.path.join(toplevel, "bin", "glacierstarter")
router = os.path.join(toplevel, "bin", "glacier")

updatedServerOptions = TestUtil.serverOptions.replace("TOPLEVELDIR", toplevel)
updatedClientOptions = TestUtil.clientOptions.replace("TOPLEVELDIR", toplevel)
updatedClientServerOptions = TestUtil.clientServerOptions.replace("TOPLEVELDIR", toplevel)

command = starter + updatedClientServerOptions + \
          r' --Glacier.Starter.RouterPath=' + router + \
          r' --Glacier.Starter.PropertiesOverwrite=Ice.ServerIdleTime=10' \
          r' --Glacier.Starter.CryptPasswords="' + toplevel + r'/test/Glacier/starter/passwords"' + \
          r' --Glacier.Starter.Endpoints="default -p 12346 -t 5000"' + \
          r' --Glacier.Router.Endpoints="default"' + \
          r' --Glacier.Client.Endpoints="default"' + \
          r' --Glacier.Server.Endpoints="tcp"'

print "starting glacier starter...",
starterPipe = os.popen(command)
TestUtil.getServerPid(starterPipe)
TestUtil.getAdapterReady(starterPipe)
print "ok"

name = os.path.join("Glacier", "starter")
TestUtil.mixedClientServerTest(toplevel, name)

print "shutting down glacier starter...",
TestUtil.killServers() # TODO: Graceful shutdown
print "ok"

starterStatus = starterPipe.close()

if starterStatus:
    TestUtil.killServers()
    sys.exit(1)

sys.exit(0)
