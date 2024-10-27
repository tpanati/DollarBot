api_token=$(grep "api_token" user.properties|cut -d'=' -f2)

echo "Checking for API Token..."
if [ -z "$api_token" ]
then
  echo "Oh no! Looks like you're missing an API token. No worries."
  echo "Please run the 'setup.sh' file first."
fi

if [ -n "$api_token" ]
then
  echo "Waking up DollarBot..."
  python3 code/code.py
fi