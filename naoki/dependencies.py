#!/usr/bin/python

import logging
import os
import re

import architectures
import repositories
import packages

from constants import *
from exception import *

class Dependency(object):
	def __init__(self, identifier, origin=None):
		self.identifier = identifier
		self.origin = origin

	def __repr__(self):
		s = "<%s %s" % (self.__class__.__name__, self.identifier)
		if self.origin:
			s += " by %s" % self.origin.name
			s += "(%s)" % os.path.basename(self.origin.filename)
		s += ">"
		return s

	@property
	def type(self):
		if self.identifier.startswith("/"):
			return DEP_FILE
		elif ".so" in self.identifier:
			return DEP_LIBRARY
		elif re.match("^[A-Za-z0-9\-\+_]+$", self.identifier):
			return DEP_PACKAGE

		return DEP_INVALID

	def match(self, other):
		return self.type == other.type \
			and self.identifier == other.identifier

	__eq__ = match


class Provides(Dependency):
	pass


class DependencySet(object):
	def __init__(self, dependencies=[], arch=None):
		if not arch:
			arches = architectures.Architectures()
			arch = arches.get_default()
		self.arch = arch

		self.repo = repositories.BinaryRepository(self.arch)

		# initialize package lists
		self._dependencies = []
		self._items = []

		# caches
		self.__provides = {}
		self.__dependencies = {}

		# add all provided dependencies
		for dependency in dependencies:
			self.add_dependency(dependency)

		logging.debug("Successfully initialized %s" % self)

	@property
	def hash(self):
		hash = ["%s" % i for i in self._items]

		return "".join(hash)

	def __repr__(self):
		return "<%s>" % (self.__class__.__name__)

	def add_dependency(self, item):
		assert isinstance(item, Dependency)

		# If this dependency is already provided by something else
		# we skip the add
		for p in self.provides:
			if p.match(item):
				logging.debug("%s matches %s" % (p, item))
				return

		if not item in self.dependencies:
			self._dependencies.append(item)

			logging.debug("Added new dependency %s" % item)

	def add_package(self, item):
		assert isinstance(item, packages.BinaryPackage)

		if item in self._items:
			return

		# Packages conflict
		for package in self._items:
			if package.name == item.name:
				if item > package:
					logging.debug("Replacing package %s by %s" % (package, item))
					self._items.remove(package)
					break

		self._items.append(item)
		logging.debug("Added new package %s" % item)

	def resolve(self):
		logging.debug("Resolving %s" % self)

		# Safe for endless loop
		counter = 1000

		while True:
			counter -= 1
			if not counter:
				logging.debug("Maximum count of dependency loop was reached")
				break

			dependency = self.next_unresolved_dependency
			if not dependency:
				break

			logging.debug("Processing dependency: %s" % dependency.identifier)

			if dependency.type == DEP_PACKAGE:
				package = self.repo.find_package_by_name(dependency.identifier)
				if package:
					# Found a package and add this
					self.add_package(package)
					continue

			elif dependency.type == DEP_LIBRARY:
				package = self.repo.find_package_by_provides(dependency)
				if package:
					self.add_package(package)
					continue

			elif dependency.type == DEP_FILE:
				package = self.repo.find_package_by_file(dependency.identifier)
				if package:
					self.add_package(package)
					continue

				logging.warning("Cannot find a package which provides file %s" % \
					dependency.identifier)

			elif dependency.type == DEP_INVALID:
				logging.warning("Dropping invalid dependency %s" % dependency.identifier)
				continue

			# Found not solution
			logging.debug("No match found: %s" % dependency)

		if self.unresolved_dependencies:
			#logging.error("Unresolveable dependencies: %s" % self.dependencies)
			raise DependencyResolutionError, "%s" % self.unresolved_dependencies

	@property
	def unresolved_dependencies(self):
		return self.calculate_unresolved_dependencies(next=False)

	@property
	def next_unresolved_dependency(self):
		d = self.calculate_unresolved_dependencies(next=True)
		if d:
			return d[0]

	def calculate_unresolved_dependencies(self, next=False):
		dependencies = []

		# Cache provides
		provides = self.provides

		for dependency in self._dependencies + self.dependencies:
			if dependency.type == DEP_INVALID:
				continue

			found = False
			for item in self._items:
				if item.does_provide(dependency):
					found = True
					break

			if found:
				continue

			#for provide in provides:
			#	if dependency.match(provide):
			#		found = True
			#		break
			#
			#if found:
			#	continue

			dependencies.append(dependency)

			# If next is set return only one.
			if next:
				return dependencies

		return dependencies

	@property
	def dependencies(self):
		if not self.__dependencies.has_key(self.hash):
			self.__dependencies[self.hash] = self.calculate_dependencies()

		return self.__dependencies[self.hash]

	def calculate_dependencies(self):
		dependencies = []
		for item in self._items:
			dependencies += item.get_dependencies()

		return list(set(dependencies))

	@property
	def packages(self):
		return sorted(self._items)

	def calculate_provides(self):
		provides = []
		for item in self._items:
			provides += item.get_provides()

		return list(set(provides))

	@property
	def provides(self):
		if not self.__provides.has_key(self.hash):
			self.__provides[self.hash] = self.calculate_provides()

		return self.__provides[self.hash]


if __name__ == "__main__":
	import architectures
	arches = architectures.Architectures()

	ds = DependencySet(arch=arches.get("i686"))
	ds.add_dependency(Dependency("/bin/bash"))
	ds.resolve()
	print ds.packages
