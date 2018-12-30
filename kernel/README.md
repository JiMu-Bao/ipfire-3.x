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

The following commands are available. Appending the <arch> argument allows you
to edit a specific architecture. Default is x86_64.

#### oldconfig

You can run this when updating the kernel to a new release or after changing any
options manually. All unset or updated options will be prompted for and all
configuration files for all architectures will be updated.

  (pakfire-shell)> scripts/configure oldconfig <arch>

#### olddefconfig

Like oldconfig, but automatically answers all options with the default value.

  (pakfire-shell)> scripts/configure olddefconfig

#### menuconfig

If you want to edit the configuration using the kernel's config editor. All
configuration files will be updated afterwards and potentially prompted for options
that diverge for different architectures.

  (pakfire-shell)> scripts/configure menuconfig <arch>

#### listnewconfig

This will list all unset options.

  (pakfire-shell)> scripts/configure listnewconfig <arch>
