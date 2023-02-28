<!-- cSpell:ignore riscv -->
# kv260

## Reproduce the execution environment like `submission/sd.img`

### Cross-compile for KV260 in your x86 host machine

```
# Install g++ for aarch64.
# You need to modify CXX and AR in Makefile if your g++ version is not 10
$ sudo apt install -y g++-10-aarch64-linux-gnu

$ cd kv260
$ make build-lib
```

Then you can copy the whole project directory into KV260.
