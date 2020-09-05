#!/bin/bash

for ((i=0;i<$1;i++))
do
  bazel run -c opt --copt="-mavx" benchmarks_test -- --benchmarks=benchmark_defun_matmul_2_by_2_CPU;
  bazel run -c opt --copt="-mavx" benchmarks_test -- --benchmarks=benchmark_defun_matmul_2_by_2_with_signature_CPU;
  echo "Trial $i completed.";
done
