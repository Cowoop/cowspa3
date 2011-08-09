#!/bin/bash
nosetests -vx  --pdb-failures --pdb \
tests/test_schemas.py:test_create \
tests/test_bizplace.py \
tests/test_member.py \
tests/test_resources.py \
tests/test_plans.py \
tests/test_usage.py \
tests/test_pricing.py \
# Add tests above this line

#nosetests -vx  --pdb-failures --pdb tests/test_schemas.py # Destroys all stores