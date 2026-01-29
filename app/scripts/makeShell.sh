#!/bin/bash

if [ -z "$1" ]; then
	echo "Rewrites the index.html file to use a CDN for assets."
	echo "Usage: makeShellhome.sh param = sha256 hash of the build to use"
	exit 1
fi


# set var for cdn
CDN="https://cdn.jsdelivr.net/gh/shellbros/mathlete@$1/"

# Inject JSCDN config and custom script tag after the first </script>
# Use CDN variable for the URL
echo "Injecting JSCDN config and custom script tag into ../../index.html"
awk -v CDN="$CDN" '{
  print;
  if (!done && /<\/script>/) {
    print "<script src=\"" CDN "app/build.json\"></script>";
    print "<script>window.JSCDN=\"" CDN "\";</script>";
    print "<script src=\"" CDN "app/checker.js\"></script>";
    done=1
  }
}' ../../index.html > ../../index.html.tmp && mv ../../index.html.tmp ../../index.html

echo "Rewriting paths in ../../index.html"
node cdnSearchReplace.js "$CDN"
echo "Build complete. Output available in '../..'."