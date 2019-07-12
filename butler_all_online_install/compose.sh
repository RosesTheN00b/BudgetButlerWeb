#!/bin/bash
set -e

echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~Start  Building~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~BudgetButlerWeb~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"

echo "Löschen von alten ergebnissen"
rm -rfv butler_all_online_distribution

echo "build php api"
cd butler_all_online_api/api/
composer install
cd -

echo "build ng frontend"
cd butler_all_online/budgetbutler
npm install
ng build --prod
cd -

echo "create dist"
mkdir butler_all_online_distribution
mkdir butler_all_online_distribution/api
cp -r butler_all_online_api/api/* butler_all_online_distribution/api
cp -r butler_all_online/budgetbutler/dist/* butler_all_online_distribution
cp butler_all_online_distribution/api/robots.txt butler_all_online_distribution/
cp butler_all_online_install/.htaccess butler_all_online_distribution/
rm butler_all_online_distribution/3rdpartylicenses.txt


echo "------------------------------------------------"
echo "------------------------------------------------"
echo "~~~~~~~~~~~~~~~~~~Done Building~~~~~~~~~~~~~~~~~"
echo "~~~~~~~~~~~~~~~~~BudgetButlerWeb~~~~~~~~~~~~~~~~"
echo "------------------------------------------------"
echo "------------------------------------------------"

