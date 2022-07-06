# Scorecard Autopopulater

Populates a google sheet with cricket match data

## Installation

Create the conda environment:

```
conda env create -f environment.yml
```

Activate the environment:

```
conda activate scorecard-autopopulater
```

## Usage

Use the CLI like so:

```
python cli/squad_cli.py write_squads_to_csv -u YOUR_URL -f YOUR_FILE_NAME
```

## Testing

for just unit tests:

```
pytest --cov=scorecard_autopopulater tests/unit
```

or for all tests:

```
pytest --cov=scorecard_autopopulater tests
```

## Linting

```
flake8 scorecard_autopopulater
```

### Caveats

1. Run out given to first player
2. Hat-tricks not implemented
