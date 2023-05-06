#!/usr/bin/env python3

import sys
import json
import subprocess
import publicsuffix
import os, os.path

workdir = "/tmp"
resultdir = "/mnt/result"
bindir = "/opt"

if len(sys.argv) !=2:
    print("Usage: %s <resolve json>\n" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

data = {}
with open(filename) as f:
    data = json.load(f)

t = data["t"]
list = data["list"]

nxdomains = []
for domain in list:
        if "rc" in domain and domain["rc"] == "NXDOMAIN":
                nxdomains.append(domain["d"])

psl_file = publicsuffix.fetch()
psl = publicsuffix.PublicSuffixList(psl_file)

pubdomains = {}
for domain in nxdomains:
        _domain = psl.get_public_suffix(domain.encode("utf-8").decode("idna")).encode("idna").decode("utf-8")
        pubdomains[_domain] = True

print("%d = %d\n" % (len(nxdomains), len(pubdomains)))
nxdomfile = workdir + "/%d.nxdomains.lst" % t
with open(nxdomfile, "w") as f:
        for domain in pubdomains:
                f.write("%s\n" % domain)

resultfile = resultdir + "/%d.lst" % t
resulttmp = resultfile + ".tmp"
code = subprocess.call([bindir + "/test.rb", nxdomfile, resulttmp])
if os.path.exists(nxdomfile):
    os.unlink(nxdomfile)
if os.path.exists(resulttmp):
    os.rename(resulttmp, resultfile)
code = subprocess.call(["gzip", resultfile])
