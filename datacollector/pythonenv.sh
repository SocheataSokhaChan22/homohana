if [[ "$OSTYPE" == "linux-gnu"* || "$OSTYPE" == "darwin"* ]]; then
    source venv/bin/activate
else
    source venv/Scripts/activate
fi

export PYTHONPATH="$(pwd)/src"
