# Facebook Messages Extractor

Sometimes we want to get our message data out of Facebook, for interfacing with
other programs, and reading outside of the Messenger application. This
repository is a collection of tooling for doing so. They work with Facebook
account data dumps.

## Usage

Once you have `facebook-<username>.zip`, apply the following.

```bash
./prepare.sh facebook-<username>.zip
# This will create messages.html, which may be passed to the other programs.
```
