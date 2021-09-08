#!/bin/bash

export PYTHONPATH="$(pwd)/lab_1:$(pwd)/lab_2:$(pwd)/lab_3:$(pwd)/lab_4:$(pwd):${PYTHONPATH}"
echo "Running tests..."

FAILED=0
LABS=$(cat automation/labs.txt)

echo "Current scope: $LABS"

for lab in $LABS; do
	echo "Running tests for lab #${lab}"

	TARGET_SCORE=$(cat lab_"${lab}"/target_score.txt)

	TARGET_TESTS_FILE=automation/lab_"${lab}"/target_tests_"${TARGET_SCORE}".txt

	TARGET_TESTS=$(cat ${TARGET_TESTS_FILE})

	if [[ -z "${TARGET_TESTS// }" ]]; then
	  echo "No tests provided. Skipping."
	  continue
	fi

	while read test_file_name || [[ -n $test_file_name ]]
	do
	  echo "Running tests from $test_file_name"
	  if ! python3 -m unittest lab_"${lab}"/$test_file_name;  then
    	FAILED=1
	  fi
	done <<< "$(cat "$TARGET_TESTS_FILE")"

done

if [[ ${FAILED} -eq 1 ]]; then
	echo "Tests failed."
	exit 1
fi

echo "Tests passed."
