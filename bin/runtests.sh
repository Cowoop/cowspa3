#!/bin/bash
#nosetests -vx --pdb-failures --pdb --with-coverage --cover-package be --cover-html \
nosetests -vx --pdb-failures --pdb --with-coverage --cover-package be \
tests/test_commonlib.py \
tests/test_schemas.py \
tests/test_system.py \
tests/test_be_libs.py \
tests/test_bizplace.py \
tests/test_invoicepref.py \
tests/test_member.py \
tests/test_user.py \
tests/test_access.py \
tests/test_resources.py \
tests/test_tariff.py \
tests/test_requests.py \
tests/test_usage.py \
tests/test_invoice.py \
tests/test_pricing.py \
tests/test_billingpref.py \
tests/test_membership.py \
tests/test_roles.py \
tests/test_rpc_access.py
# Add tests above this line

#nosetests -vx  --pdb-failures --pdb tests/test_schemas.py # Destroys all stores
