#!/usr/bin/python

import logging
import os

import dependencies
import repositories
import util

from constants import *
from environ import _Environment


class Generator(_Environment):
	def __init__(self, type, arch=None):
		_Environment.__init__(self, arch, enable_loop=True)

		self.type = type

		self.repos = repositories.SourceRepositories(self.arch)

		for r in self.repos.all:
			if not r.completely_built:
				raise Exception, "The repo is not built completely: %s" % r

		self.build_deps = dependencies.DependencySet(arch=self.arch)
		deps = [
			"basesystem",
			"dracut",
			"e2fsprogs",
			"kernel",
			"squashfs-tools",
			"syslinux",
			"util-linux-ng",
			"zerofree",
			"/sbin/dmsetup",
			"/usr/bin/mkisofs",
		]
		for dep in deps:
			dep = dependencies.Dependency(dep)
			self.build_deps.add_dependency(dep)

		self.installer_deps = dependencies.DependencySet(arch=self.arch)
		deps = [
			"basesystem",
			"installer",
			# TODO needs to be replaced
			"xorg-x11-drv-ati",
			"xorg-x11-drv-evdev",
			"xorg-x11-drv-intel",
			"xorg-x11-drv-keyboard",
			"xorg-x11-drv-mouse",
			"xorg-x11-drv-nv",
			"xorg-x11-drv-synaptics",
			"xorg-x11-drv-vesa",
			"xorg-x11-drv-vmware",
		]
		for dep in deps:
			dep = dependencies.Dependency(dep)
			self.installer_deps.add_dependency(dep)

	def chrootPath(self, *args):
		return os.path.join(GENDIR, self.arch.name, *args)

	@property
	def logger(self):
		return logging.getLogger()

	def run(self):
		# Unpacking packages we need in this environment
		logging.info("Resolving dependencies...")
		self.build_deps.resolve()
		self.installer_deps.resolve()

		for package in self.build_deps.packages:
			self.extract(package)

		util.mkdir(self.chrootPath("installer"))
		for package in self.installer_deps.packages:
			self.extract(package, "installer")

		util.mkdir(self.chrootPath("packages"))
		for p in self.repos.packages:
			for bin in p.binary_files:
				os.link(os.path.join(PACKAGESDIR, self.arch.name, bin),
					self.chrootPath("packages", bin))

		self.doChroot("/usr/src/tools/generator %s" % self.type, shell=True)
