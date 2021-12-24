#!/bin/bash

export PYTHONPATH="$(pwd)/lab_1:$(pwd)/lab_2:$(pwd)/lab_3:$(pwd)/lab_4:$(pwd):${PYTHONPATH}"

echo -e '\n'
echo 'Running lint check...'

FAILED=0
LABS=$(cat automation/labs.txt)

for lab in $LABS; do
	echo "Running lint for lab #${lab}"

  TARGET_SCORE=$(cat lab_"${lab}"/target_score.txt)

	lint_output=$(python3 -m pylint --rcfile=automation/.pylintrc lab_"${lab}")
  python3 automation/check_lint.py --lint-output "$lint_output" --target-score $TARGET_SCORE
  if [[ $? -ne 0 ]]; then
    echo "Lint check failed for lab #${lab}."
    FAILED=1
  else
    echo "Lint check passed for lab #${lab}."
  fi
done

if [[ ${FAILED} -eq 1 ]]; then
	echo "Lint check failed."
	exit ${FAILED}
fi

echo "Lint check passed."
