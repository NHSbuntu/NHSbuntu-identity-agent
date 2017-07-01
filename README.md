# NHSbuntu-identity-agent

## Installation on Debian, Ubuntu or derivatives

add the NHSbuntu packagecloud repo and install driver packages for smart card readers on Linux

`curl -s https://packagecloud.io/install/repositories/nhsbuntu/nhs-smartcards/script.deb.sh | sudo bash`

NOTE: if you are on a version of Ubuntu other than 16.04/xenial (or an Ubuntu derivative like mint) then you need to ensure that the distro codename is added correctly in etc/apt/sources.list.d/nhsbuntu-smartcards.list (should point to 'ubuntu' and 'xenial main')

`sudo apt install python-pip python3-dev curl git pcscd swig libclassicclient libssl0.9.8 ifdokccid`

`pip install pyscard httplib2 pykcs11`

`git clone` this repo then `cd` into the cloned directory

## Usage (in testing)

`python -i authenticator.py`

`>>> auth = authenticator()`

`>>> response = auth.authenticate("1234")`

should respond with XML containing a valid ticket for NHS Spine SSO


## What works, and what doesn't...

### Working

* Series 6 and 8 Smartcards (possibly 4 & 5 - not tested)
* Omnikey 3121 and Gemalto PC Twin card readers
* Basic Spine authentication


### Not Working

* Any card management functions
* Session persistence
* Card expiry and passcode notifications







