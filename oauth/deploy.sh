#!/bin/bash

pip3 install -r requirements.txt --target ./package
cd package || exit
zip -r ../my_deployment_package.zip .
cd ..
zip my_deployment_package.zip lambda_function.py
aws lambda update-function-code --function-name snake-draft-oauth \
--zip-file fileb:///Users/ryanmoore/dev/projects/snake_draft_lambda/oauth/my_deployment_package.zip