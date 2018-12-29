# Kernel

## Configuration

### Layout

The kernel configuration files are split into individual configuration files for
each architecture. This way, common options can be changed globally and can be
overwritten for certain architectures which gives us a more consistent configuration
across all architectures.

### How to update the configuration?

For these steps, you will have to change into a build environment and change to
the kernel directory:

  # pakfire-builder shell kernel.nm
  (pakfire-shell)> cd /usr/src/packages/kernel-x.y.z...

The following commands are available:

#### oldconfig

You can run this when updating the kernel to a new release or after changing any
options manually. All unset or updated options will be prompted for and all
configuration files for all architectures will be updated.

  (pakfire-shell)> scripts/configure oldconfig

#### olddefconfig

Like oldconfig, but automatically answers all options with the default value.

  (pakfire-shell)> scripts/configure olddefconfig

#### menuconfig

If you want to edit the configuration using the kernel's config editor, you can
do it for the main architecture (which is x86_64 right now). All other configuration
files will be updated afterwards and potentially prompted for options that diverge
for other architectures.

  (pakfire-shell)> scripts/configure menuconfig

#### listnewconfig

This will list all unset options.

  (pakfire-shell)> scripts/configure listnewconfig
