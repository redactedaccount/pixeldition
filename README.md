# pixeldition
A toy program for manipulating images based on conditional logic on a per-pixel basis.

# Setup

```sh
poetry env activate 
poetry env use python3.13
poetry install
poetry run pixeldition -h
```

# Example Usage

Swap green and blue in an image:

```sh
poetry run pixeldition pixeldition/test_images/test1.jpg --channel-swap g b
```

Use Image Magick to resize an image, then pipe it into `pixeldition` to swap the channels:

```sh
magick pixeldition/test_images/test1.jpg -resize 50% - | poetry run pixeldition /dev/stdin --channel-swap g b
```

Invert red, *then* swap blue and green:

```sh
poetry run pixeldition pixeldition/test_images/test1.jpg -ci r -cs b g
```

# Using the Makefile

Place any images you want to batch-convert into an `images/` directory, set the
transformation with the 'trans' variable.  For example, to invert the colour red,
invoke like this:

```sh
make -e trans='-ci r' -j batch
```
