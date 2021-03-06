#! /usr/bin/env python3

import clr
clr.AddReference("bin/distlib")
from distlib.randomvariates import MersenneTwisterVariateGenerator as MT
mt = MT.CreateMersenneTwisterVariateGenerator()
print("(0,1)")
print(mt.GenerateUniformOO())
print(mt.GenerateUniformOO())
print(mt.GenerateUniformOO())
print(mt.GenerateUniformOO())
print("(0,1]")
print(mt.GenerateUniformOC())
print(mt.GenerateUniformOC())
print(mt.GenerateUniformOC())
print(mt.GenerateUniformOC())
print("[0,1)")
print(mt.GenerateUniformCO())
print(mt.GenerateUniformCO())
print(mt.GenerateUniformCO())
print(mt.GenerateUniformCO())
print("[0,1]")
print(mt.GenerateUniformCC())
print(mt.GenerateUniformCC())
print(mt.GenerateUniformCC())
print(mt.GenerateUniformCC())
