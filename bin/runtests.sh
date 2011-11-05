#!/bin/bash
nosetests -vx --pdb-failures --pdb \
tests/test_schemas.py \
tests/test_system.py \
tests/test_bizplace.py \
tests/test_member.py \
tests/test_user.py \
tests/test_resources.py \
tests/test_plans.py \
tests/test_requests.py \
tests/test_usage.py \
tests/test_pricing.py \
tests/test_roles.py \
# Add tests above this line

#nosetests -vx  --pdb-failures --pdb tests/test_schemas.py # Destroys all stores
